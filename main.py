import os
import sys

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from crud import add_user_to_db, verify_name
from db_models import UserOrm
from user_base import UserCreate, UserOut, UserIn

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ws_manage import Manager, WebSocket
from fastapi import FastAPI, WebSocketDisconnect, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse  # , ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db_config import SessionLocal, engine, Base
import json

from fastapi import HTTPException

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    debug=True,
    version="0.83",
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


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            received_msg = await websocket.receive_text()
            json_msg = json.loads(received_msg)
            print(json_msg)
            # data = await websocket.receive_json()
            reply_dict = {
                "client": websocket.headers.get('sec-websocket-key'),
                "status": json_msg["status"],
                "date": json_msg["date"],
                "message": json_msg["message"]
            }
            # for key in websocket.headers.keys():
            #     print(key, websocket.headers.get(key))
            print("client:{} {}".format(
                websocket.headers.get('sec-websocket-key'),
                json_msg['message']
            ))
            # await manager.send_personal_message(f"You wrote: {json_msg['message']}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
            await manager.broadcast(json.dumps(reply_dict))
            reply_dict = {
                "client": websocket.headers.get('sec-websocket-key'),
                "status": "connecting",
                "date": json_msg["date"],
                "message": f"Matching cueue.. in {len(manager.active_connections)}"
            }
            await manager.send_personal_message(json.dumps(reply_dict), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        reply_dict = {
            "client": websocket.headers.get('sec-websocket-key'),
            "status": "disconnected",
            "message": "Client #{} left the chat".format(client_id)
        }
        await manager.broadcast(json.dumps(reply_dict))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    # データベースにアカウントを追加する
    print(user.json(), "by post")

    return user


@app.post("/login/", response_model=UserOut)
async def login(user: UserIn, db: Session = Depends(get_db)):
    signed_user_orm = verify_name(db, user.name)
    if signed_user_orm is not None and user.verify_password(signed_user_orm.password):
        return signed_user_orm
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.post("/create", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user_to_db(db, UserOrm.from_pymodel(user))
