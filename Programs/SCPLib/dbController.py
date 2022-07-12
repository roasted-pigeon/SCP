import sys

from SCPLib import models
import uuid
import hashlib
import settings
import socket
import urllib.request
from SCPLib import gLibs
from SCPLib.gLibs import printError

from SCPLib.logCollector import logCollector
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

    def login(self, login: str, pwd: str):
        try:
            userData = self.fetchRow(models.LoginData, login=login).first()
            loginAttemptOutcome = bool(userData) and \
                                  (login.__len__() != 0) and \
                                  (pwd.__len__() != 0) and \
                                  (
                                          hashlib.sha256(
                                              (pwd + settings.passwordSalt).encode(settings.encoding)
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

                            gLibs.cls()
                            print(f"Добро пожаловать, {userData.name} {userData.surname}. "
                                  f"Фонд желает вам продуктивной работы.")

                        else:
                            printError("У Вас уже есть активная сессия. "
                                       "Завершите её, или при возникновении проблем, обратитесь в поддержку.")
                    else:
                        printError("Ваши учётные данные истекли. Обратитесь в канцелярию.")
                else:
                    printError(userData.status.description)
            else:
                printError("Логин или пароль введены неправильно.")
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
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
        finally:
            return self.currentSession

    # TODO: Необходимо добавить логгирование получения всех видов доступа
    def checkAccessRoom(self, session: models.Session, room: models.Room):
        try:
            if room.roomStatus.name == "Закрыта":
                if session.isValid:
                    if session.loginData_user.userroomspecialaccesses.filter_by(room=room):
                        return True
                    if not room.specialAccessRequired:
                        if session.loginData_user.clearance >= room.clearance:
                            return True
                    return False
                else:
                    printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                    return False
            elif room.roomStatus.name == "Открыта":
                return True
            elif room.roomStatus.name == "Изолирована":
                return False
            else:
                raise Exception("Неизвестный статус комнаты!")
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def checkAccessSection(self, session: models.Session, facilitySection: models.FacilitySection):
        try:
            if facilitySection.roomStatus.name == "Закрыта":
                if session.isValid:
                    if session.loginData_user.usersectionspecialaccesses.filter_by(facilitySection=facilitySection):
                        return True
                    if not facilitySection.specialAccessRequired:
                        if session.loginData_user.clearance >= facilitySection.clearance:
                            return True
                    return False
                else:
                    printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                    return False
            elif facilitySection.roomStatus.name == "Открыта":
                return True
            elif facilitySection.roomStatus.name == "Изолирована":
                return False
            else:
                raise Exception("Неизвестный статус сектора!")
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def checkAccessObject(self, session: models.Session, object: models.Object):
        try:
            if session.isValid:
                if session.loginData_user.userobjectspecialaccesses.filter_by(object=object):
                    return True
                if not object.specialAccessRequired:
                    if session.loginData_user.clearance >= object.clearance:
                        return True
                return False
            else:
                printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                return False
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def checkAccessUserFile(
            self,
            session: models.Session,
            userFile: models.UserFile,
            fileAccessType: models.FileAccessType
    ):
        try:
            if session.isValid:
                if session.loginData_user.userobjectspecialaccesses.filter_by(userFile=userFile):
                    return True
                if not userFile.specialAccessRequired:
                    pass
                    # TODO: Необходимо реализовать проверку на то, к какому типу отношения пользователя к файлу
                    #       относится пользователь. Потом в зависимости от типа отношения необходимо выполнить запрос на
                    #       то, имеет ли пользователь с таким типом отношений запрошенный доступ к файлу
                return False
            else:
                printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                return False
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def checkAccessSystem(self, session: models.Session, system: models.System):
        try:
            if isinstance(system, str):
                system = self.fetchRow(models.System, name=system).first()
            if system:
                if session.isValid:
                    if session.loginData_user.systemaccesses.filter_by(system=system):
                        return True
                    return False
                else:
                    printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                    return False
            else:
                printError("Система указана неверно!")
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def fetchRow(self, table: models.Base, **kwargs):
        try:
            return self.sessionHandler.query(table).filter_by(**kwargs)
        except Exception as e:
            self.collector.logException(e, self.systemName, self.systemVersion)
            return None

    def addRow(self, object: models.Base):
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
