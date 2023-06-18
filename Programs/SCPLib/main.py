import sys
import sqlalchemy as db
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

from SCPLib import gLibs, models

from SCPLib.logCollector import logCollector
from SCPLib.dbController import dbController
from sqlalchemy.orm import Session

import settings

SYSTEM_NAME: str = "SCPLibs Debugger"
SYSTEM_VERSION: str = "1.0.0"


def start():
    try:
        engine: Engine = db.create_engine(settings.SCPDatabase)
        metadata: MetaData = db.MetaData(engine)
        sessionHandler: Session = Session(engine, future=True, autoflush=True)
        collector: logCollector = logCollector()
        controller: dbController = dbController(
            SYSTEM_NAME,
            SYSTEM_VERSION,
            engine.connect(),
            sessionHandler if not settings.individualObjects else Session(engine, future=True, autoflush=True),
            collector if not settings.individualObjects else logCollector()
        )
    except Exception as exception:
        gLibs.noLogException(exception)
        sys.exit()

    try:
        login: str
        password: str
        # login, password = "rocketbunny", "0246851379tyre"
        login, password = gLibs.auth()
        currentSession: Session = controller.login(login, password)
        print(currentSession)
        currentSession = controller.accessCardLogin(
            controller.fetchRow(
                models.AccessCard,
                card_id=input("Введите номер ID-карты: ")
                # card_id="c8b410b8-4fbf-4626-a375-18720702e09c"
            ).first()
        )
        if currentSession:
            print(
                controller.checkAccessRoom(currentSession, controller.fetchRow(
                    models.Room,
                    id=1
                ).first())
            )
        print(currentSession)
    except Exception as e:
        collector.logException(e, SYSTEM_NAME, SYSTEM_VERSION)
    finally:
        controller.closeCurrentSession()
        sessionHandler.close()
