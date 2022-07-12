import traceback
from pickle import dumps

import settings
from SCPLib import gLibs
from SCPLib.models import LogType, Log, Metalog
import sqlalchemy as db
from sqlalchemy.orm import Session
from SCPLib.gLibs import printError


class logCollector:
    def __init__(self):
        engine = db.create_engine(settings.SCPLogs)
        metadata = db.MetaData(engine)
        self.sessionHandler = Session(engine, future=True, autoflush=True)
        self.connection = engine.connect()

    def log(
            self,
            system: str,
            logType: str,
            summary: str,
            description: str,
            comment: str = None,
            optionalFields: dict = None
    ):
        self.sessionHandler.add(
            Log(
                system=system,
                logType=self.sessionHandler.query(LogType).filter_by(name=logType).first(),
                summary=summary,
                description=description,
                comment=comment,
                optionalFields=dumps(optionalFields) if optionalFields else None
            )
        )
        self.sessionHandler.commit()

    def metalog(self, logType: str, summary: str, description: str, comment: str = None, optionalFields: dict = None):
        self.sessionHandler.add(
            Metalog(
                logType=self.sessionHandler.query(LogType).filter_by(name=logType),
                summary=summary,
                description=description,
                comment=comment,
                optionalFields=dumps(optionalFields) if optionalFields else None
            )
        )
        self.sessionHandler.commit()

    def logException(self, exception: Exception, systemName, systemVersion):
        printError("Произошла ошибка!")
        if hasattr(exception, 'message'):
            printError((exception.message if settings.debug else settings.veiledError))
            try:
                self.log(
                    systemName,
                    "Exception",
                    f"A {type(exception).__name__} exception occurred in the {systemName} v. {systemVersion} system",
                    str(traceback.format_exception(exception))
                )
            except Exception as exc:
                gLibs.noLogException(exc)
        else:
            printError((exception if settings.debug else settings.veiledError))
            try:
                self.log(
                    systemName,
                    "Exception",
                    f"A {type(exception).__name__} exception occurred in the {systemName} v. {systemVersion} system",
                    str(traceback.format_exception(exception))
                )
            except Exception as exc:
                gLibs.noLogException(exc)
