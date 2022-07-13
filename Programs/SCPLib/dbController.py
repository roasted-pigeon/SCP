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
            sessionHandler: Session,
            collector: logCollector
    ):
        self.systemName: str = systemName
        self.systemVersion: str = systemVersion
        self.connection: Connection = connection
        self.sessionHandler: Session = sessionHandler
        self.currentSession: models.Session or None = None
        self.collector: logCollector = collector

    def login(self, login: str, pwd: str):
        try:
            errorMessage: str or None = None
            if self.currentSession is not None:
                self.closeCurrentSession()
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
                            errorMessage = "У Вас уже есть активная сессия. " \
                                           "Завершите её, или при возникновении проблем, обратитесь в поддержку."
                            printError(errorMessage)
                    else:
                        errorMessage = "Ваши учётные данные истекли. Обратитесь в канцелярию."
                        printError(errorMessage)
                else:
                    errorMessage = userData.status.description
                    printError(errorMessage)
            else:
                errorMessage = "Логин или пароль введены неправильно."
                printError(errorMessage)
            if userData:
                self.collector.log(
                    self.systemName,
                    "Auth",
                    f"Пользователь {login} попытался войти в аккаунт. "
                    f"Результат: {'успешно' if self.currentSession else 'безуспешно'}",
                    f"{userData.job} {userData.name} {userData.surname}, обладающ{'ий' if userData.gender else 'ая'} "
                    f"уровнем допуска {userData.clearance} совершил{'' if userData.gender else 'а'} попытку войти в "
                    f"аккаунт с узла: {socket.gethostname()}, IP адрес: {socket.gethostbyname(socket.gethostname())}. "
                    f"Попытка {'не ' if not self.currentSession else ''}удалась.",
                    optionalFields=
                    {
                        "Учётная запись": login,
                        "Имя узла": socket.gethostbyname(socket.gethostname()),
                        "IP": socket.gethostname(),
                        "Внешний IP": urllib.request.urlopen('https://ident.me').read().decode('utf8')
                        if gLibs.has_connection('https://ident.me') else None,
                        "Сессия": self.currentSession.id if self.currentSession else None,
                        "Сообщение об ошибке": errorMessage
                    }
                )
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
        finally:
            return self.currentSession

    def accessCardLogin(self, accessCard: models.AccessCard):
        try:
            errorMessage: str or None = None
            if self.currentSession is not None:
                self.closeCurrentSession()
            if accessCard:
                if accessCard.status.name == "Active":
                    if not accessCard.isExpired:
                        session = models.Session(
                            id=str(uuid.uuid4()),
                            accessStatus=self.fetchRow(models.AccessStatus, name="Active").first(),
                            loginData_user=accessCard.user.loginData.first()
                        )
                        self.addRow(session)
                        self.currentSession = session
                        print(f"Добро пожаловать, {accessCard.user.name} {accessCard.user.surname}. "
                              f"Фонд желает вам продуктивной работы.")
                    else:
                        errorMessage = "Срок действия карты истёк. Обратитесь в канцелярию."
                        printError(errorMessage)
                else:
                    errorMessage = accessCard.status.description
                    printError(errorMessage)
                self.collector.log(
                    self.systemName,
                    "Auth",
                    f"Пользователь {accessCard.user.loginData.first().login} прошёл аутентификацию в системе при "
                    f"помощи ID-карты. Результат: {'успешно' if self.currentSession else 'безуспешно'}",
                    f"{accessCard.user.job} {accessCard.user.name} {accessCard.user.surname}, "
                    f"обладающ{'ий' if accessCard.user.gender else 'ая'} уровнем допуска {accessCard.user.clearance} "
                    f"совершил{'' if accessCard.user.gender else 'а'} попытку аутентификации, используя свою ID-карту "
                    f"с номером {accessCard.card_id}. Попытка аутентификации совершена на узле: "
                    f"{socket.gethostname()}, IP адрес: {socket.gethostbyname(socket.gethostname())}. Попытка "
                    f"{'не ' if not self.currentSession else ''}удалась.",
                    optionalFields=
                    {
                        "Номер ID-карты": accessCard.card_id,
                        "Учётная запись": accessCard.user.loginData.first().login,
                        "Имя узла": socket.gethostbyname(socket.gethostname()),
                        "IP": socket.gethostname(),
                        "Внешний IP": urllib.request.urlopen('https://ident.me').read().decode('utf8')
                        if gLibs.has_connection('https://ident.me') else None,
                        "Сессия": self.currentSession.id if self.currentSession else None,
                        "Сообщение об ошибке": errorMessage
                    }
                )
            else:
                errorMessage = "Карта не найдена в базе данных. Обратитсь в канцелярию."
                printError(errorMessage)
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
        finally:
            return self.currentSession

    # TODO 1: Необходимо добавить логгирование получения всех видов доступа
    # TODO 2: Есть смысл избавиться от параметров session и брать self.currentSession, так как не предполагается работа
    #         с "чужими" сессиями, и метод не должен использоваться как статический, так как это позволит брать сессию
    #         без непосредственной авторизации
    # TODO 3: Нужно подумать над тем, чтобы доступ в комнаты проверять не по сессии, а просто по карте, а саму сессию
    #         для проерки прав создавать непосредственно внутри метода
    def checkAccessRoom(self, session: models.Session, room: models.Room):
        try:
            if room.roomStatus.name == "Закрыта":
                if session.isValid:
                    if session.loginData_user.userroomspecialaccesses.filter_by(room=room).count():
                        # self.collector.log(
                        #     self.systemName,
                        #     self.systemVersion,
                        #     f"{session.loginData_user.job} {session.loginData_user.surname} прошёл через двери "
                        #     "комнаты {room}",
                        #     f"",
                        #     optionalFields=
                        #     {
                        #
                        #     }
                        # )
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
                    if session.loginData_user.usersectionspecialaccesses.filter_by(
                            facilitySection=facilitySection
                    ).count():
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
                if session.loginData_user.userobjectspecialaccesses.filter_by(object=object).count():
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

    # TODO: Это нужно оттестировать
    def checkAccessUserFile(
            self,
            session: models.Session,
            userFile: models.UserFile,
            fileAccessType: models.FileAccessType
    ):
        try:
            if session.isValid:
                if fileAccessType in self.getUserToFileAccesses(session.loginData_user, userFile):
                    return True
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

    def logout(self):
        try:
            self.closeCurrentSession()
            print("Вы вышли из системы. Для дальнейшей работы потребуется повторная аутентификация.")
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return None

    # TODO: Это нужно оттестировать
    def getUserToFileAccesses(self, user: models.User, userFile: models.UserFile):
        try:
            if user and userFile:
                accesses: list or set = []
                blank_accesses = self.fetchRow(
                    models.FileAccess,
                    filyType=userFile.fileType,
                    fileRequesterType=self.fetchRow(
                        models.FileRequesterType,
                        name="User"
                    ),
                    fileRequester_id=user.fullID
                )
                if user.userfilespecialaccesses.filter_by(userFile=userFile).count():
                    blank_accesses.union(
                        self.fetchRow(
                            models.FileAccess,
                            filyType=userFile.fileType,
                            fileRequesterType=self.fetchRow(
                                models.FileRequesterType,
                                name="Special Access"
                            )
                        )
                    )

                blank_accesses.union(
                    self.fetchRow(
                        models.FileAccess,
                        filyType=userFile.fileType,
                        fileRequesterType=self.fetchRow(
                            models.FileRequesterType,
                            name="Department"
                        ),
                        fileRequester_id=user.department_id
                    )
                )
                blank_accesses.union(
                    self.fetchRow(
                        models.FileAccess,
                        filyType=userFile.fileType,
                        fileRequesterType=self.fetchRow(
                            models.FileRequesterType,
                            name="Job"
                        ),
                        fileRequester_id=user.job_id
                    )
                )
                blank_accesses.union(
                    self.fetchRow(
                        models.FileAccess,
                        filyType=userFile.fileType,
                        fileRequesterType=self.fetchRow(
                            models.FileRequesterType,
                            name="Class"
                        ),
                        fileRequester_id=user.employeeClass_id
                    )
                )
                blank_accesses.union(
                    self.fetchRow(
                        models.FileAccess,
                        filyType=userFile.fileType,
                        fileRequesterType=self.fetchRow(
                            models.FileRequesterType,
                            name="Facility"
                        ),
                        fileRequester_id=user.facility_id
                    )
                )
                blank_accesses.union(
                    self.fetchRow(
                        models.FileAccess,
                        filyType=userFile.fileType,
                        fileRequesterType=self.fetchRow(
                            models.FileRequesterType,
                            name="Supervisor"
                        ),
                        fileRequester_id=user.supervisor.fullID
                    )
                )
                for unit in user.usertounits.all():
                    blank_accesses.union(
                        self.fetchRow(
                            models.FileAccess,
                            filyType=userFile.fileType,
                            fileRequesterType=self.fetchRow(
                                models.FileRequesterType,
                                name="Unit"
                            ),
                            fileRequester_id=unit.id
                        )
                    )
                blank_accesses.union(
                    self.fetchRow(
                        models.FileAccess,
                        filyType=userFile.fileType,
                        fileRequesterType=self.fetchRow(
                            models.FileRequesterType,
                            name="Everyone"
                        )
                    )
                )
                for access in blank_accesses.all():
                    accesses.append(access.fileAccessType)
                accesses = set(accesses)
                return accesses
            else:
                return None
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return None
