from pickle import dumps, loads

import sqlalchemy as db

import models
from logCollector import logCollector
from dbController import dbController
from sqlalchemy.orm import Session

import settings

SYSTEM_NAME = "SCPLibs Debugger"
SYSTEM_VERSION = "1.0.0"

engine = db.create_engine(settings.SCPDatabase)
metadata = db.MetaData(engine)
session = Session(engine, future=True, autoflush=True)
collector = logCollector()
controller = dbController(
    SYSTEM_NAME,
    SYSTEM_VERSION,
    engine.connect(),
    session if not settings.individualObjects else Session(engine, future=True, autoflush=True),
    collector if not settings.individualObjects else logCollector()
)


def main():
    currentSession = controller.login("rocketbunny", "0246851379tyre")


if __name__ == '__main__':
    try:
        main()
        engine = db.create_engine(settings.SCPLogs)
        metadata = db.MetaData(engine)
        sessionHandler = Session(engine, future=True, autoflush=True)
        print(sessionHandler.query(models.Log).filter_by(id=1).first())
    except Exception as e:
        collector.logException(e, SYSTEM_NAME, SYSTEM_VERSION)
    finally:
        controller.closeCurrentSession()
        session.close()
