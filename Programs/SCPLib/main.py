import sys
import sqlalchemy as db
from logCollector import logCollector
from dbController import dbController
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
    print("Произошла ошибка!")
    if hasattr(exception, 'message'):
        print(exception.message if settings.debug else settings.veiledError)
    sys.exit()


def main():
    currentSession = controller.login("rocketbunny", "0246851379tyre")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        collector.logException(e, SYSTEM_NAME, SYSTEM_VERSION)
    finally:
        controller.closeCurrentSession()
        session.close()
