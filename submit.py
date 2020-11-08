from engine import session, User, DoToday
from sqlalchemy import and_
import datetime
from pprint import pprint as pp

def main():
    today = datetime.date.today()
    users = session.query(User.id, User.name, DoToday.dotoday).outerjoin(DoToday, and_(User.id == DoToday.id, DoToday.date == today)).all()
    [dict(zip(("id", "name", "dotoday"), user)) for user in users]
    usernames = '、'.join([user[1] for user in users])
    message = (
        "本日は残業します\n"
        "メンバー：" + usernames
    )
    print(message)

if __name__ == "__main__":
    main()
