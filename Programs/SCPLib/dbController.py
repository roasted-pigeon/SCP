import datetime
import models
import uuid
import hashlib
_SALT = "_sqlscp-rth5614"


class dbController:
    def __init__(self, connection, session):
        self.connection = connection
        self.sessionHandler = session
        self.currentSession = None

    def login(self, login, pwd):
        userData = self.fetchRow(models.LoginData, login=login).first()
        loginAttemptOutcome = (login.__len__() != 0) and\
                              (pwd.__len__() != 0) and\
                              (hashlib.sha256((pwd + _SALT).encode('utf-8')).hexdigest() == userData.password)
        if loginAttemptOutcome:
            if userData.status.name == "Active":
                if not userData.isExpired():
                    if not userData.sessions.filter_by(
                            accessStatus=self.fetchRow(models.AccessStatus, name="Active").first()
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
        return self.currentSession

    def fetchRow(self, table: models.Base, **kwargs):
        try:
            return self.sessionHandler.query(table).filter_by(**kwargs)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return None

    def addRow(self, object):
        try:
            self.sessionHandler.add(object)
            self.sessionHandler.commit()
            self.sessionHandler.refresh(object)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return None

    def updateRow(self, rows, updaters: dict, synchronize_session='fetch'):
        rows.update(updaters, synchronize_session=synchronize_session)

    def deleteRow(self, rows, synchronize_session='fetch'):
        rows.delete(synchronize_session=synchronize_session)

    def closeCurrentSession(self):
        if self.currentSession:
            self.currentSession.accessStatus = self.fetchRow(models.AccessStatus, name="Blocked").first()
            self.sessionHandler.commit()
