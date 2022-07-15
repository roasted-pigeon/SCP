from SCPLib import models
import uuid
import hashlib
import settings
import socket
import urllib.request
from sqlalchemy import desc

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
                        if not userData.sessions.filter_by(system=self.systemName, isValid=True).count():
                            if self.checkAccessSystem(self.systemName):
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
                                errorMessage = "У вас нет доступа к данной системе.\nЕсли вы считаете, что произошла " \
                                               "ошибка, обратитесь к своему непосредственному руководителю. В " \
                                               "противном случае вам настоятельно рекомендуется воздержаться от " \
                                               "неавторизоанных попыток входа в системы Фонда, к которым вам не " \
                                               "предоставлен доступ"
                                printError(errorMessage)
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
                        if not accessCard.user.sessions.filter_by(system=self.systemName, isValid=True).count():
                            if self.checkAccessSystem(self.systemName):
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
                                errorMessage = "У вас нет доступа к данной системе.\nЕсли вы считаете, что произошла " \
                                               "ошибка, обратитесь к своему непосредственному руководителю. В " \
                                               "противном случае вам настоятельно рекомендуется воздержаться от " \
                                               "неавторизоанных попыток входа в системы Фонда, к которым вам не " \
                                               "предоставлен доступ"
                                printError(errorMessage)
                        else:
                            errorMessage = "У Вас уже есть активная сессия. " \
                                           "Завершите её, или при возникновении проблем, обратитесь в поддержку."
                            printError(errorMessage)
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

    # TODO 1: Необходимо добавить логгирование получения всех видов доступа (DONE, но нужно протестировать)
    # TODO 2: (DONE)
    # TODO 3: (DONE)
    def checkAccessRoom(self, accessCard: models.AccessCard, room: models.Room):
        try:
            self.accessCardLogin(accessCard)
            if room.roomStatus.name == "Закрыта":
                if self.currentSession.isValid:
                    URSAs = self.currentSession.loginData_user.userroomspecialaccesses.filter_by(
                        room=room,
                        isExpired=False
                    )
                    if URSAs.count():
                        self.collector.log(
                            self.systemName,
                            self.systemVersion,
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                            f"прош{'ёл' if self.currentSession.loginData_user.gender else 'ла'} через двери комнаты "
                            f"{room}, используя ID-карту {accessCard}.",
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                            f"{self.currentSession.loginData_user.surname} "
                            f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                            f"открытия дверей комнаты {room}. Доступ был предоставлен на основании наличия спеиального "
                            f"допуска.",
                            optionalFields=
                            {
                                "Сотрудник": self.currentSession.loginData_user,
                                "Комната": room,
                                "ID-карта": accessCard,
                                "Специальный допуск": URSAs.first(),
                                "Сессия": self.currentSession.id if self.currentSession else None
                            }
                        )
                        return True
                    if not room.specialAccessRequired:
                        if self.currentSession.loginData_user.clearance >= room.clearance:
                            self.collector.log(
                                self.systemName,
                                self.systemVersion,
                                f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                                f"прош{'ёл' if self.currentSession.loginData_user.gender else 'ла'} через двери "
                                f"комнаты {room}, используя ID-карту {accessCard}.",
                                f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                                f"{self.currentSession.loginData_user.surname} "
                                f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                                f"открытия дверей комнаты {room}. Доступ был предоставлен на основании наличия "
                                f"необходимого уровня допуска. ",
                                optionalFields=
                                {
                                    "Сотрудник": self.currentSession.loginData_user,
                                    "Комната": room,
                                    "ID-карта": accessCard,
                                    "Сессия": self.currentSession.id if self.currentSession else None
                                }
                            )
                            return True
                    self.collector.log(
                        self.systemName,
                        self.systemVersion,
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                        f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} пройти через двери "
                        f"комнаты {room}, используя ID-карту {accessCard}.",
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                        f"{self.currentSession.loginData_user.surname} "
                        f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                        f"открытия дверей комнаты {room}. Доступ не был предоставлен",
                        optionalFields=
                        {
                            "Сотрудник": self.currentSession.loginData_user,
                            "Комната": room,
                            "ID-карта": accessCard,
                            "Сессия": self.currentSession.id if self.currentSession else None
                        }
                    )
                    return False
                else:
                    printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                    return False
            elif room.roomStatus.name == "Открыта":
                return True
            elif room.roomStatus.name == "Изолирована":
                self.collector.log(
                    self.systemName,
                    self.systemVersion,
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                    f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} пройти через двери "
                    f"комнаты {room}, в которой введён режим изоляции, используя ID-карту {accessCard}.",
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                    f"{self.currentSession.loginData_user.surname} "
                    f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                    f"открытия дверей комнаты {room}. Доступ не был предоставлен, так как в комнате введён режим "
                    f"изоляции",
                    optionalFields=
                    {
                        "Сотрудник": self.currentSession.loginData_user,
                        "Комната": room,
                        "ID-карта": accessCard,
                        "Сессия": self.currentSession.id if self.currentSession else None
                    }
                )
                return False
            else:
                raise Exception("Неизвестный статус комнаты!")
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False
        finally:
            self.closeCurrentSession()

    def checkAccessSection(self, accessCard: models.AccessCard, facilitySection: models.FacilitySection):
        try:
            self.accessCardLogin(accessCard)
            if facilitySection.roomStatus.name == "Закрыта":
                if self.currentSession.isValid:
                    USSAs = self.currentSession.loginData_user.usersectionspecialaccesses.filter_by(
                        facilitySection=facilitySection,
                        isExpired=False
                    )
                    if USSAs.count():
                        self.collector.log(
                            self.systemName,
                            self.systemVersion,
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                            f"прош{'ёл' if self.currentSession.loginData_user.gender else 'ла'} через двери на границе "
                            f"секции {facilitySection}, используя ID-карту {accessCard}.",
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                            f"{self.currentSession.loginData_user.surname} "
                            f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                            f"открытия дверей на границах секции {facilitySection}. Доступ был предоставлен на "
                            f"основании наличия спеиального допуска.",
                            optionalFields=
                            {
                                "Сотрудник": self.currentSession.loginData_user,
                                "Секция": facilitySection,
                                "ID-карта": accessCard,
                                "Специальный допуск": USSAs.first(),
                                "Сессия": self.currentSession.id if self.currentSession else None
                            }
                        )
                        return True
                    if not facilitySection.specialAccessRequired:
                        if self.currentSession.loginData_user.clearance >= facilitySection.clearance:
                            self.collector.log(
                                self.systemName,
                                self.systemVersion,
                                f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                                f"прош{'ёл' if self.currentSession.loginData_user.gender else 'ла'} через двери на"
                                f"границе секции {facilitySection}, используя ID-карту {accessCard}.",
                                f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                                f"{self.currentSession.loginData_user.surname} "
                                f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                                f"открытия дверей на границах секции {facilitySection}. Доступ был предоставлен на "
                                f"основании наличия необходимого уровня допуска.",
                                optionalFields=
                                {
                                    "Сотрудник": self.currentSession.loginData_user,
                                    "Секция": facilitySection,
                                    "ID-карта": accessCard,
                                    "Сессия": self.currentSession.id if self.currentSession else None
                                }
                            )
                            return True
                    self.collector.log(
                        self.systemName,
                        self.systemVersion,
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                        f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} пройти через двери на "
                        f"границе секции {facilitySection}, используя ID-карту {accessCard}.",
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                        f"{self.currentSession.loginData_user.surname} "
                        f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                        f"открытия дверей на границе секции {facilitySection}. Доступ не был предоставлен",
                        optionalFields=
                        {
                            "Сотрудник": self.currentSession.loginData_user,
                            "Секция": facilitySection,
                            "ID-карта": accessCard,
                            "Сессия": self.currentSession.id if self.currentSession else None
                        }
                    )
                    return False
                else:
                    printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                    return False
            elif facilitySection.roomStatus.name == "Открыта":
                return True
            elif facilitySection.roomStatus.name == "Изолирована":
                self.collector.log(
                    self.systemName,
                    self.systemVersion,
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname}"
                    f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} пройти через двери на "
                    f"границе секции {facilitySection}, используя ID-карту {accessCard}.",
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                    f"{self.currentSession.loginData_user.surname} "
                    f"приложил{'' if self.currentSession.loginData_user.gender else 'а'} свою ID-карту для "
                    f"открытия дверей на границе секции {facilitySection}. Доступ не был предоставлен, так как в "
                    f"секции введён режим изоляции",
                    optionalFields=
                    {
                        "Сотрудник": self.currentSession.loginData_user,
                        "Секция": facilitySection,
                        "ID-карта": accessCard,
                        "Сессия": self.currentSession.id if self.currentSession else None
                    }
                )
                return False
            else:
                raise Exception("Неизвестный статус комнаты!")
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False
        finally:
            self.closeCurrentSession()

    def checkAccessObject(self, object: models.Object):
        try:
            UOSAs = self.currentSession.loginData_user.userobjectspecialaccesses.filter_by(
                object=object,
                isExpired=False
            ).orderby(
                desc(models.UserObjectSpecialAccess.clearance_id)
            )
            if self.currentSession.isValid:
                if UOSAs.count():
                    self.collector.log(
                        self.systemName,
                        self.systemVersion,
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                        f"получил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к базовой "
                        f"информации об объекте SCP-{object.id}",
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                        f"{self.currentSession.loginData_user.surname} "
                        f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам, "
                        f"содержащим базовую информацию об объекте SCP-{object.id}. Доступ был предоставлен на "
                        f"основании наличия спеиального допуска (L{UOSAs.first().clearance_id}).",
                        optionalFields=
                        {
                            "Сотрудник": self.currentSession.loginData_user,
                            "Объект": object,
                            "Специальный допуск": UOSAs.first(),
                            "Сессия": self.currentSession.id if self.currentSession else None
                        }
                    )
                    return True
                if not object.specialAccessRequired:
                    if self.currentSession.loginData_user.clearance >= object.clearance:
                        self.collector.log(
                            self.systemName,
                            self.systemVersion,
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                            f"получил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к базовой "
                            f"информации об объекте SCP-{object.id}",
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                            f"{self.currentSession.loginData_user.surname} "
                            f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам, "
                            f"содержащим базовую информацию об объекте SCP-{object.id}. Доступ был предоставлен на "
                            f"основании наличия необходимого уровня допуска "
                            f"(L{self.currentSession.loginData_user.clearance_id}).",
                            optionalFields=
                            {
                                "Сотрудник": self.currentSession.loginData_user,
                                "Объект": object,
                                "Сессия": self.currentSession.id if self.currentSession else None
                            }
                        )
                        return True
                self.collector.log(
                    self.systemName,
                    self.systemVersion,
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                    f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} получить доступ к базовой "
                    f"информации об объекте SCP-{object.id}",
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                    f"{self.currentSession.loginData_user.surname} "
                    f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам, "
                    f"содержащим базовую информацию об объекте SCP-{object.id}. Доступ не был предоставлен.",
                    optionalFields=
                    {
                        "Сотрудник": self.currentSession.loginData_user,
                        "Объект": object,
                        "Сессия": self.currentSession.id if self.currentSession else None
                    }
                )
                return False
            else:
                printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                return False
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def checkAccessObjectFile(self, objectFile: models.ObjectFile):
        try:
            UOSAs = self.currentSession.loginData_user.userobjectspecialaccesses.filter_by(
                object=objectFile.object,
                isExpired=False
            ).orderby(
                desc(models.UserObjectSpecialAccess.clearance_id)
            )
            clearance = objectFile.clearance if objectFile.clearance is not None else objectFile.object.clearance
            if self.currentSession.isValid:
                if UOSAs.count():
                    if UOSAs.first().clearance >= clearance:
                        self.collector.log(
                            self.systemName,
                            self.systemVersion,
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                            f"получил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам "
                            f"об объекте SCP-{objectFile.object.id}.",
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                            f"{self.currentSession.loginData_user.surname} "
                            f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам, "
                            f"содержащим информацию об объекте SCP-{objectFile.object.id} (\"{objectFile.name}\"). "
                            f"Доступ был предоставлен на основании наличия спеиального допуска "
                            f"(L{UOSAs.first().clearance_id}).",
                            optionalFields=
                            {
                                "Сотрудник": self.currentSession.loginData_user,
                                "Объект": objectFile.object,
                                "Документ": objectFile,
                                "Специальный допуск": UOSAs.first(),
                                "Сессия": self.currentSession.id if self.currentSession else None
                            }
                        )
                        return True
                if not objectFile.specialAccessRequired:
                    if self.currentSession.loginData_user.clearance >= clearance:
                        self.collector.log(
                            self.systemName,
                            self.systemVersion,
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                            f"получил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам "
                            f"об объекте SCP-{objectFile.object.id}",
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                            f"{self.currentSession.loginData_user.surname} "
                            f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам, "
                            f"содержащим информацию об объекте SCP-{objectFile.object.id} (\"{objectFile.name}\"). "
                            f"Доступ был предоставлен на основании наличия необходимого уровня допуска "
                            f"(L{UOSAs.first().clearance_id}).",
                            optionalFields=
                            {
                                "Сотрудник": self.currentSession.loginData_user,
                                "Объект": objectFile.object,
                                "Документ": objectFile,
                                "Сессия": self.currentSession.id if self.currentSession else None
                            }
                        )
                        return True
                self.collector.log(
                    self.systemName,
                    self.systemVersion,
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                    f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} получить доступ к базовой "
                    f"информации об объекте SCP-{objectFile.object.id}",
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                    f"{self.currentSession.loginData_user.surname} "
                    f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к материалам, "
                    f"содержащим базовую информацию об объекте SCP-{objectFile.object.id} (\"{objectFile.name}\"). "
                    f"Доступ не был предоставлен.",
                    optionalFields=
                    {
                        "Сотрудник": self.currentSession.loginData_user,
                        "Объект": objectFile.object,
                        "Документ": objectFile,
                        "Сессия": self.currentSession.id if self.currentSession else None
                    }
                )
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
            
            userFile: models.UserFile,
            fileAccessType: models.FileAccessType
    ):
        try:
            if self.currentSession.isValid:
                if fileAccessType in self.getUserToFileAccesses(self.currentSession.loginData_user, userFile):
                    self.collector.log(
                        self.systemName,
                        self.systemVersion,
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                        f"получил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к документу "
                        f"\"{userFile}\" ({fileAccessType})",
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                        f"{self.currentSession.loginData_user.surname} "
                        f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ ({fileAccessType}) "
                        f"к документу \"{userFile}\" засекреченного по уровню допуска {userFile.clearance}. "
                        f"Доступ был предоставлен.",
                        optionalFields=
                        {
                            "Сотрудник": self.currentSession.loginData_user,
                            "Документ": userFile,
                            "Сессия": self.currentSession.id if self.currentSession else None
                        }
                    )
                    return True
                self.collector.log(
                    self.systemName,
                    self.systemVersion,
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                    f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} доступ к документу "
                    f"\"{userFile}\" ({fileAccessType})",
                    f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                    f"{self.currentSession.loginData_user.surname} "
                    f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ ({fileAccessType}) "
                    f"к документу \"{userFile}\" засекреченного по уровню допуска {userFile.clearance}. "
                    f"Доступ не был предоставлен.",
                    optionalFields=
                    {
                        "Сотрудник": self.currentSession.loginData_user,
                        "Документ": userFile,
                        "Сессия": self.currentSession.id if self.currentSession else None
                    }
                )
                return False
            else:
                printError("Ваша сессия истекла или была заблокирована! Авторизуйтесь заново")
                return False
        except Exception as exception:
            self.collector.logException(exception, self.systemName, self.systemVersion)
            return False

    def checkAccessSystem(self, system: str or models.System):
        try:
            if isinstance(system, str):
                system = self.fetchRow(models.System, name=system).first()
            if system:
                if self.currentSession.isValid:
                    access = self.currentSession.loginData_user.systemaccesses.filter_by(
                        system=system,
                        isExpired=False
                    )
                    if access:
                        self.collector.log(
                            self.systemName,
                            self.systemVersion,
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                            f"получил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к системе "
                            f"\"{system}\"",
                            f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                            f"{self.currentSession.loginData_user.surname} "
                            f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к системе "
                            f"\"{system}\". Доступ был предоставлен с правами группы "
                            f"{access.first().systemAccessRole}.",
                            optionalFields=
                            {
                                "Сотрудник": self.currentSession.loginData_user,
                                "Система": system,
                                "Доступ": access.first(),
                                "Сессия": self.currentSession.id if self.currentSession else None
                            }
                        )
                        return True
                    self.collector.log(
                        self.systemName,
                        self.systemVersion,
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.surname} "
                        f"попытал{'ся' if self.currentSession.loginData_user.gender else 'ась'} получить доступ к "
                        f"системе \"{system}\"",
                        f"{self.currentSession.loginData_user.job} {self.currentSession.loginData_user.name} "
                        f"{self.currentSession.loginData_user.surname} "
                        f"запросил{'' if self.currentSession.loginData_user.gender else 'а'} доступ к системе "
                        f"\"{system}\". Доступ не был предоставлен.",
                        optionalFields=
                        {
                            "Сотрудник": self.currentSession.loginData_user,
                            "Система": system,
                            "Сессия": self.currentSession.id if self.currentSession else None
                        }
                    )
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
                if user.userfilespecialaccesses.filter_by(
                        userFile=userFile,
                        isExpired=False
                ).count():
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
