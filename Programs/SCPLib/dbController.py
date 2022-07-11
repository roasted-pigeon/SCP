import models
import uuid
import hashlib
import settings
import socket
import urllib.request
import gLibs

from logCollector import logCollector
from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection


class dbController:
    def __init__(
            self,
            systemName: str,
            systemVersion: str,
            connection: Connection,
            session: Session,
            collector: logCollector
    ):
        self.systemName = systemName
        self.systemVersion = systemVersion
        self.connection = connection
        self.sessionHandler = session
        self.currentSession = None
        self.collector = collector

    def login(self, login, pwd):
        userData = self.fetchRow(models.LoginData, login=login).first()
        loginAttemptOutcome = userData and \
                              (login.__len__() != 0) and \
                              (pwd.__len__() != 0) and \
                              (
                                      hashlib.sha256(
                                          (pwd + settings.passwordSalt).encode('utf-8')
                                      ).hexdigest() == userData.password
                              )
        if loginAttemptOutcome:
            if userData.status.name == "Active":
                if not userData.isExpired:
                    if not userData.sessions.filter_by(
                            accessStatus=self.fetchRow(models.AccessStatus, name="Active").first(),
                            isExpired=False
                    ).count():
                        session = models.Session(
                            id=str(uuid.uuid4()),
                            accessStatus=self.fetchRow(models.AccessStatus, name="Active").first(),
                            loginData_user=userData
                        )
                        self.addRow(session)
                        self.currentSession = session

                        print(f"Добро пожаловать, {userData.name} {userData.surname}. "
                              f"Фонд желает вам продуктивной работы.")

                    else:
                        print("У Вас уже есть активная сессия. "
                              "Завершите её, или при возникновении проблем, обратитесь в поддержку.")
                else:
                    print("Ваши учётные данные истекли. Обратитесь в канцелярию.")
            else:
                print(userData.status.description)
        else:
            print("Логин или пароль введены неправильно.")
        if userData:
            self.collector.log(
                self.systemName,
                "Auth",
                f"Пользователь {login} попытался войти в аккаунт. "
                f"Результат: {'успешно' if self.currentSession else 'безуспешно'}",
                f"{userData.job} {userData.name} {userData.surname}, обладающ{'ий' if userData.gender else 'ая'} "
                f"уровнем допуска {userData.clearance} совершил{'' if userData.gender else 'а'} попытку войти в "
                f"аккаунт с узла: {socket.gethostname()} с IP адреса: {socket.gethostbyname(socket.gethostname())}. "
                f"Попытка {'не' if not self.currentSession else ''} удалась.",
                optionalFields=
                {
                    "Учётная запись": login,
                    "Имя узла": socket.gethostbyname(socket.gethostname()),
                    "IP": socket.gethostname(),
                    "Внешний IP": urllib.request.urlopen('https://ident.me').read().decode('utf8')
                    if gLibs.has_connection('https://ident.me') else None,
                    "Сессия": self.currentSession.id if self.currentSession else None
                }
            )
        return self.currentSession

    def fetchRow(self, table: models.Base, **kwargs):
        try:
            return self.sessionHandler.query(table).filter_by(**kwargs)
        except Exception as e:
            self.collector.logException(e, self.systemName, self.systemVersion)
            return None

    def addRow(self, object):
        try:
            self.sessionHandler.add(object)
            self.sessionHandler.commit()
            self.sessionHandler.refresh(object)
        except Exception as e:
            self.collector.logException(e, self.systemName, self.systemVersion)
            return None

    def deleteRow(self, rows, synchronize_session='fetch'):
        try:
            rows.delete(synchronize_session=synchronize_session)
            self.sessionHandler.commit()
        except Exception as e:
            self.collector.logException(e, self.systemName, self.systemVersion)
            return None

    def closeCurrentSession(self):
        try:
            if self.currentSession:
                self.currentSession.accessStatus = self.fetchRow(models.AccessStatus, name="Blocked").first()
                self.sessionHandler.commit()
                self.currentSession = None
        except Exception as e:
            self.collector.logException(e, self.systemName, self.systemVersion)
            return None
