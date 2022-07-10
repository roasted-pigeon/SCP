import sqlalchemy as db
from dbController import dbController
from sqlalchemy.orm import Session


engine = db.create_engine("sqlite:///..\\SCPDatabase.db")
metadata = db.MetaData(engine)
session = Session(engine, future=True, autoflush=True)
controller = dbController(engine.connect(), session)


def main():
    currentSession = controller.login("rocketbunny", "0246851379tyre")


if __name__ == '__main__':
    try:
        main()
    finally:
        controller.closeCurrentSession()
        session.close()
