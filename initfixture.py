from engine import session, User, DoToday
import datetime
from pprint import pprint as pp

def main():
    today = datetime.date.today()
    users = [
        {"name": '田中太郎', "enable": True, "dotodays": [
            [datetime.date(2020, 1, 1), False],
            [today, True]
        ]},
        {"name": '鈴木次郎', "enable": True, "dotodays": [
            [datetime.date(2020, 1, 1), False]
        ]},
    ]

    for user in users:
        user_a=User(name=user['name'], enable=user['enable'])
        session.add(user_a)
        session.flush()
        for dotoday in user["dotodays"]:
            dotoday_a = DoToday(date=dotoday[0], id=user_a.id, dotoday=dotoday[1])
            session.add(dotoday_a)
        
    session.commit()
    users = session.query(User, DoToday).outerjoin(DoToday, User.id == DoToday.id).all()
    pp(users)

if __name__ == "__main__":
    main()
