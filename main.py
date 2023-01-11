import os
import sys
import uuid
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from crud import add_user_to_db, verify_name
from db_models import UserOrm
from fast_api_project.user_management import UserManager
from user import UserCreate, UserOut, UserIn

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from jose import JWTError, jwt
from ws_manage import ConnectionManager
from ws_request_model import *
from fastapi import FastAPI, WebSocketDisconnect, Depends, Form, status, Security, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, RedirectResponse  # , ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db_config import SessionLocal, engine, Base
import json
import logging
from fastapi import HTTPException, WebSocket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

# :TODO replace tokens with database
tokens = {"01835c3a-fb3d-b4e2-a43e-1682dc0be131",
          "01835c3a-fb3d-3520-3d79-6534542003b1",
          "01835c3a-fb3d-1c2e-8375-a475a429ca89",
          "01835c3a-fb3d-3520-3d79-6534542003b1"}


def check_query_token(token: str = Query()):
    if token not in tokens:
        raise HTTPException(status_code=400, detail="Query token invalid")
    else:
        return


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    debug=True,
    version="0.85",
    dependencies=[Depends(check_query_token)]
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
manager = ConnectionManager()


@app.get("/wschat")
async def get():
    return FileResponse("wschat.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query()):
    #  :TODO add user authentication using by token
    if token_certification(token):
        raise HTTPException(status_code=status.WS_1008_POLICY_VIOLATION)
    user = UserManager(uuid.UUID(token), websocket, debug=True)
    await user.user_event_loop()


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


def create_access_token(ulid_: str, expire: datetime = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)):
    return jwt.encode({"sub": ulid_, "exp": expire}, SECRET_KEY)


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


def get_current_user(ulid_: str, db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(tokens)
        jwt_ulid: str = payload.get("sub")
        if ulid_ is None:
            raise credentials_exception
        logger.debug(ulid_)
    except JWTError:
        raise credentials_exception
    user: UserOut = db.query(UserOrm).filter(UserOrm.ulid == jwt_ulid).first()
    if user is None or token not in tokens:
        raise credentials_exception
    return user


@app.post("/token_login")
def token_authenticate(ulid_: str, token: str, db: Session = Depends(get_db)):
    return get_current_user(ulid_, db, token)


def token_certification(token: str) -> bool:
    # Test用
    if token in tokens:
        return True
    return False
