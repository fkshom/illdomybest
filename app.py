import re
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from engine import session, User, DoToday
from sqlalchemy import and_
import datetime
from logging import getLogger
from pprint import pprint as pp

from pydantic import BaseModel

logger = getLogger(__name__)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PutMembersItem(BaseModel):
    dotoday: bool


api = FastAPI(root_path="/api")
app.mount("/api", api)
@api.get('/members')
async def getMembers():
    today = datetime.date.today()
    users = session.query(User.id, User.name, DoToday.dotoday).outerjoin(DoToday, and_(User.id == DoToday.id, DoToday.date == today)).all()
    result = {
        "today": today,
        "users": [dict(zip(("id", "name", "dotoday"), user)) for user in users]
    }
    pp(result)
    return result


@api.put('/members/{id}')
async def putMembers(id, item: PutMembersItem):
    success = True
    message = ""
    pp(item)
    today = datetime.date.today()
    user = session.query(User.id).filter(User.id == id).first()
    if user == None:
        success = False
        message = "ユーザーが見つかりません"
    else:
        dotoday = session.query(DoToday).filter(DoToday.id == id, DoToday.date == today).with_for_update().first()
        if dotoday == None:
            dotoday = DoToday(id=id, date=today)
            session.add(dotoday)
        dotoday.dotoday = item.dotoday
        session.commit()

        users = session.query(User, DoToday).outerjoin(DoToday, User.id == DoToday.id).all()
        pp(users)

    return {"success": success, "message": message}


app.mount("/", StaticFiles(directory="static"), name="static")
