import sys
import sqlalchemy as db

from SCPLib import gLibs, models


from SCPLib.logCollector import logCollector
from SCPLib.dbController import dbController
from sqlalchemy.orm import Session

import settings

SYSTEM_NAME = "SCPLibs Debugger"
SYSTEM_VERSION = "1.0.0"

try:
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
except Exception as exception:
    gLibs.noLogException(exception)
    sys.exit()

try:
    # login, password = "rocketbunny", "0246851379tyre"
    login, password = gLibs.auth()
    currentSession = controller.login(login, password)
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
    session.close()
