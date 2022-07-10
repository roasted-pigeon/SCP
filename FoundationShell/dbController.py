import sqlalchemy as db
class dbController:
    def __init__(self, connection):
        self.connection=connection

    def login(self, loginField, pwdField, login, pwd):
        loginAttemptOutcome = (login.__len__() != 0) and (pwd.__len__() != 0) and (self.fetchFieldValue(pwdField, loginField, login) == pwd)
        if(loginAttemptOutcome):
            print("Авторизация пользователя "+login+" прошла успешно. Фонд желает вам продуктивной работы.")
        else:
            print("Логин или пароль введены неправильно.")
        return (loginAttemptOutcome)

    def fetchRow(self, objectToReturn, attribute, value):
        return self.connection.execute(db.select(objectToReturn).where(attribute==value))

    def fetchFieldValue(self, fieldToReturn, attribute, value):
        try:
            return self.connection.execute(db.select(fieldToReturn).where(attribute==value)).fetchone()[0]
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
