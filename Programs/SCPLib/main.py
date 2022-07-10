import sqlalchemy as db
from dbController import dbController
from sqlalchemy.orm import Session


engine = db.create_engine("sqlite:///..\\SCPDatabase.db")
metadata = db.MetaData(engine)
session = Session(engine)
controller = dbController(engine.connect(), session)

# controller.login("admin", "admin")
currentSession = controller.login("rocketbunny", "0246851379tyre")

if currentSession:
    input("Введите команду: ")
