import datetime
import sqlalchemy as db
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
        userData = self.sessionHandler.query(models.LoginData).filter_by(login=login).first()
        loginAttemptOutcome = (login.__len__() != 0) and\
                              (pwd.__len__() != 0) and\
                              (hashlib.sha256((pwd + _SALT).encode('utf-8')).hexdigest() == userData.password)
        if loginAttemptOutcome:
            if userData.status_id == 2:
                if userData.expire > datetime.datetime.now():
                    session = models.Session(
                        id=str(uuid.uuid4()),
                        accessStatus=self.sessionHandler.query(models.AccessStatus).filter_by(name="Active").first(),
                        loginData_user=userData
                    )
                    self.sessionHandler.add(session)
                    self.sessionHandler.commit()
                    self.sessionHandler.refresh(session)
                    self.currentSession = session

                    print(f"Добро пожаловать, {userData.name} {userData.surname}. Фонд желает вам продуктивной работы.")

                else:
                    print("Ваши учётные данные истекли. Обратитесь в канцелярию.")
            else:
                print(userData.status.description)
        else:
            print("Логин или пароль введены неправильно.")
        return self.currentSession

    def fetchRow(self, objectToReturn, attribute, value):
        return self.connection.execute(db.select(objectToReturn).where(attribute == value))

    def fetchFieldValue(self, fieldToReturn, attribute, value):
        try:
            return self.connection.execute(db.select(fieldToReturn).where(attribute == value)).fetchone()[0]
        except TypeError:
            return False

    def addRow(self, tableToModify, *notNullFields):
        pass

    def modifyField(self, fieldToModify, value):
        pass

    def modifyRow(self, tableToModify, rowId):
        pass

    def deleteRow(self, rowToDelete):
        pass
