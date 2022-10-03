import os
import sys
import uuid

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from crud import add_user_to_db, verify_name
from db_models import UserOrm
from user import UserCreate, UserOut, UserIn

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ws_manage import Manager, WebSocket
from fastapi import FastAPI, WebSocketDisconnect, Depends, Form, status, Security, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, RedirectResponse  # , ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db_config import SessionLocal, engine, Base
import json
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

# :TODO replace tokens with database
tokens = {"01835c3a-fb3d-b4e2-a43e-1682dc0be131"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    debug=True,
    version="0.85",
    # default_response_class=ORJSONResponse
)
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
manager = Manager()


@app.get("/")
async def get():
    return FileResponse("index.html")
    # return HTMLResponse(html)


@app.get("/style.css")
async def get():
    return FileResponse("style.css")


@app.get("/main.js")
async def get():
    return FileResponse("main.js")


@app.get("/wschat/")
def websocket_endpoint(token: str = Query()):
    return FileResponse("wschat.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query()):
    #  :TODO add user authentication using by token
    if token not in tokens:
        raise HTTPException(status_code=status.WS_1008_POLICY_VIOLATION)
    await manager.connect(websocket)
    try:
        while True:
            received_msg = await websocket.receive_text()
            logger.debug(received_msg)
            await manager.send_personal_message(received_msg, websocket)

            # :TODO This code is going to replace as Pydantic model class
            # json_msg = json.loads(received_msg)
            # print(json_msg)
            # # data = await websocket.receive_json()
            # reply_dict = {
            #     "client": websocket.headers.get('sec-websocket-key'),
            #     "status": json_msg["status"],
            #     "date": json_msg["date"],
            #     "message": json_msg["message"]
            # }
            # # for key in websocket.headers.keys():
            # #     print(key, websocket.headers.get(key))
            # print("client:{} {}".format(
            #     websocket.headers.get('sec-websocket-key'),
            #     json_msg['message']
            # ))
            # # await manager.send_personal_message(f"You wrote: {json_msg['message']}", websocket)
            # # await manager.broadcast(f"Client #{client_id} says: {data}")
            # await manager.broadcast(json.dumps(reply_dict))
            # reply_dict = {
            #     "client": websocket.headers.get('sec-websocket-key'),
            #     "status": "connecting",
            #     "date": json_msg["date"],
            #     "message": f"Matching cueue.. in {len(manager.active_connections)}"
            # }
            # await manager.send_personal_message(json.dumps(reply_dict), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        reply_dict = {
            "client": websocket.headers.get('sec-websocket-key'),
            "status": "disconnected",
            "message": "Client #{} left the chat".format(token)
        }
        await manager.broadcast(json.dumps(reply_dict))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/login/", response_model=UserOut)
async def login(name: str = Form(None), password: str = Form(None), db: Session = Depends(get_db)):
    user = UserIn(name=name, password=password)
    signed_user_orm = verify_name(db, user.name)
    if signed_user_orm is None or not user.verify_password(signed_user_orm.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(str(signed_user_orm.ulid))
    return RedirectResponse("/wschat?token=" + token, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/create", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user_to_db(db, UserOrm.from_pymodel(user))



class Token(BaseModel):
    token: str
    token_type: str


def create_access_token(ulid: str, expire: datetime = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)):
    return jwt.encode({"sub": ulid, "exp": expire}, SECRET_KEY)


@app.post("/token", response_model=Token)
def create_token(user: UserIn, db: Session = Depends(get_db)):
    signed_user_orm = verify_name(db, user.name)
    if signed_user_orm is None or not user.verify_password(signed_user_orm.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(str(signed_user_orm.ulid))
    tokens.add(token)  # temporary
    return {"token": token, "token_type": "bearer"}


def get_current_user(ulid: str, db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(tokens)
        jwt_ulid: str = payload.get("sub")
        if ulid is None:
            raise credentials_exception
        logger.debug(ulid)
    except JWTError:
        raise credentials_exception
    user: UserOut = db.query(UserOrm).filter(UserOrm.ulid == jwt_ulid).first()
    if user is None or token not in tokens:
        raise credentials_exception
    return user


@app.post("/token_login")
def token_authenticate(ulid: str, token: str, db: Session = Depends(get_db)):
    return get_current_user(ulid, db, token)
