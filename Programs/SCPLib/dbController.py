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
            if userData.status_id == 2:
                if userData.expire > datetime.datetime.now():
                    session = models.Session(
                        id=str(uuid.uuid4()),
                        accessStatus=self.fetchRow(models.AccessStatus, name="Active").first(),
                        loginData_user=userData
                    )
                    self.addRow(session)
                    self.currentSession = session

                    print(f"Добро пожаловать, {userData.name} {userData.surname}. Фонд желает вам продуктивной работы.")

                else:
                    print("Ваши учётные данные истекли. Обратитесь в канцелярию.")
            else:
                print(userData.status.description)
        else:
            print("Логин или пароль введены неправильно.")
        return self.currentSession

    def fetchRow(self, table, **kwargs):
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

    def modifyField(self, fieldToModify, value):
        pass

    def modifyRow(self, tableToModify, rowId):
        pass

    def deleteRow(self, rowToDelete):
        pass
