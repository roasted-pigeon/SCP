import datetime
from pickle import loads

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, ForeignKeyConstraint, Integer, String, Text, text, BLOB
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AccessStatus(Base):
    __tablename__ = 'accessStatus'

    id = Column(Integer, primary_key=True)
    name = Column(Text(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class Clearance(Base):
    __tablename__ = 'clearance'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return f"{self.id} ({self.name})"

    def __eq__(self, other):
        if isinstance(other, Clearance):
            return self.id == other.id

    def __ne__(self, other):
        if isinstance(other, Clearance):
            return self.id != other.id

    def __lt__(self, other):
        if isinstance(other, Clearance):
            return self.id < other.id

    def __le__(self, other):
        if isinstance(other, Clearance):
            return self.id <= other.id

    def __gt__(self, other):
        if isinstance(other, Clearance):
            return self.id > other.id

    def __ge__(self, other):
        if isinstance(other, Clearance):
            return self.id >= other.id


class ContainmentClass(Base):
    __tablename__ = 'containmentClass'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class DisruptionClass(Base):
    __tablename__ = 'disruptionClass'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class DocType(Base):
    __tablename__ = 'docType'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class EmployeeClass(Base):
    __tablename__ = 'employeeClass'

    id = Column(Integer, primary_key=True)
    letter = Column(String(1), primary_key=True)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.letter


class FacilityType(Base):
    __tablename__ = 'facilityType'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class FileAccessType(Base):
    __tablename__ = 'fileAccessType'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class FileType(Base):
    __tablename__ = 'fileType'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class FileUserType(Base):
    __tablename__ = 'fileUserType'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class RiskClass(Base):
    __tablename__ = 'riskClass'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class RoomStatus(Base):
    __tablename__ = 'roomStatus'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class RoomType(Base):
    __tablename__ = 'roomType'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class SecondaryClass(Base):
    __tablename__ = 'secondaryClass'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class SectionType(Base):
    __tablename__ = 'sectionType'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class SystemAccessRole(Base):
    __tablename__ = 'systemAccessRole'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(('supervisor_id', 'supervisor_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    gender = Column(Boolean, nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    dateOfBirth = Column(Date, nullable=False)
    rotationDate = Column(Date)
    photoLink = Column(String(200))
    clearance_id = Column(ForeignKey('clearance.id'), nullable=False)
    job_id = Column(ForeignKey('job.id'), nullable=False)
    facility_id = Column(ForeignKey('facility.id'), nullable=False)
    employeeClass_id = Column(ForeignKey('employeeClass.id'), primary_key=True, nullable=False)
    decree_id = Column(ForeignKey('userFile.id'))
    supervisor_id = Column(Integer)
    supervisor_employeeClass_id = Column(Integer)

    clearance = relationship('Clearance', backref=backref("users", lazy='dynamic'))
    decree = relationship('UserFile', primaryjoin='User.decree_id == UserFile.id')
    employeeClass = relationship('EmployeeClass', backref=backref("users", lazy='dynamic'))
    facility = relationship('Facility', backref=backref("users", lazy='dynamic'))
    job = relationship('Job', backref=backref("users", lazy='dynamic'))
    supervisor = relationship('User', remote_side=[id, employeeClass_id], backref=backref("subordinates", lazy='dynamic'))

    def __str__(self):
        return f"[{self.employeeClass}-{self.id}] {self.job} {self.name} {self.surname} (L{self.clearance_id})"


class LoginData(User):
    __tablename__ = 'loginData'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    login = Column(Text(40), nullable=False)
    password = Column(Text(256), nullable=False)
    status_id = Column(ForeignKey('accessStatus.id'), nullable=False)
    expire = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now', '+1 month')"))
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    status = relationship('AccessStatus', backref=backref("logindata", lazy='dynamic'))

    def __str__(self):
        return self.login

    @property
    def isExpired(self):
        return self.expire <= datetime.datetime.now()


class UserFile(Base):
    __tablename__ = 'userFile'
    __table_args__ = (
        ForeignKeyConstraint(('associated_with_id', 'associated_with_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
        ForeignKeyConstraint(('creator_id', 'creator_employeeClass_id'), ['user.id', 'user.employeeClass_id'])
    )

    id = Column(Integer, primary_key=True)
    clearance_id = Column(ForeignKey('clearance.id'), nullable=False)
    createdDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    docLink = Column(Integer, nullable=False)
    fileType_id = Column(ForeignKey('fileType.id'), nullable=False)
    creator_id = Column(Integer, nullable=False)
    creator_employeeClass_id = Column(Integer, nullable=False)
    associated_with_id = Column(Integer)
    associated_with_employeeClass_id = Column(String)

    associated_with = relationship('User', primaryjoin='UserFile.associated_with_id == User.id')
    clearance = relationship('Clearance', backref=backref("userfiles", lazy='dynamic'))
    creator = relationship('User', primaryjoin='UserFile.creator_id == User.id', backref=backref("userfiles", lazy='dynamic'))
    fileType = relationship('FileType', backref=backref("userfiles", lazy='dynamic'))

    def __str__(self):
        return self.docLink


class UserToObjectRole(Base):
    __tablename__ = 'userToObjectRole'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class AccessCard(Base):
    __tablename__ = 'accessCard'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    card_id = Column(String(256), primary_key=True)
    status_id = Column(ForeignKey('accessStatus.id'), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    expire = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now', '+1 year')"))
    user_id = Column(Integer, nullable=False)
    user_employeeClass_id = Column(Integer, nullable=False)

    status = relationship('AccessStatus', backref=backref("accesscards", lazy='dynamic'))
    user = relationship('User', backref=backref("accesscards", lazy='dynamic'))

    def __str__(self):
        return f"{self.card_id} (L{self.user.clearance_id})"

    @property
    def isExpired(self):
        return self.expire <= datetime.datetime.now()


class Facility(Base):
    __tablename__ = 'facility'

    id = Column(Integer, primary_key=True)
    width = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    name = Column(Text(256), nullable=False)
    description = Column(Text, nullable=False)
    facilityType_id = Column(ForeignKey('facilityType.id'), nullable=False)

    facilityType = relationship('FacilityType', backref=backref("facilities", lazy='dynamic'))

    def __str__(self):
        return self.name


class FileAccess(Base):
    __tablename__ = 'fileAccess'

    fileType_id = Column(ForeignKey('fileType.id'), primary_key=True, nullable=False)
    fileUserType_id = Column(ForeignKey('fileUserType.id'), primary_key=True, nullable=False)
    fileAccessType_id = Column(ForeignKey('fileAccessType.id'), primary_key=True, nullable=False)

    fileAccessType = relationship('FileAccessType', backref=backref("fileaccesses", lazy='dynamic'))
    fileType = relationship('FileType', backref=backref("fileaccesses", lazy='dynamic'))
    fileUserType = relationship('FileUserType', backref=backref("fileaccesses", lazy='dynamic'))

    def __str__(self):
        return f"[{self.fileType}] {self.fileUserType} - {self.fileType}"


class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    department_id = Column(ForeignKey('department.id'), nullable=False)

    department = relationship('Department', backref=backref("jobs", lazy='dynamic'))

    def __str__(self):
        return self.name


class System(Base):
    __tablename__ = 'system'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    purpose = Column(Text, nullable=False)
    description = Column(Text)
    clearance_id = Column(ForeignKey('clearance.id'), nullable=False)
    documentation_id = Column(ForeignKey('userFile.id'), nullable=False)

    clearance = relationship('Clearance', backref=backref("systems", lazy='dynamic'))
    documentation = relationship('UserFile')

    def __str__(self):
        return self.name


class UserFileSpecialAccess(Base):
    __tablename__ = 'userFileSpecialAccess'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    userFile_id = Column(ForeignKey('userFile.id'), primary_key=True, nullable=False)
    createdDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    expiryDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now', '+1 year')"))
    decree_id = Column(ForeignKey('userFile.id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    decree = relationship('UserFile', primaryjoin='UserFileSpecialAccess.decree_id == UserFile.id', backref=backref("userfilespecialaccesses", lazy='dynamic'))
    userFile = relationship('UserFile', primaryjoin='UserFileSpecialAccess.userFile_id == UserFile.id', backref=backref("userfilespecialaccesses", lazy='dynamic'))
    user = relationship('User', backref=backref("userfilespecialaccesses", lazy='dynamic'))

    def __str__(self):
        return f"{self.user} - {self.userFile}"

    @property
    def isExpired(self):
        return self.expiryDateTime <= datetime.datetime.now()


class UserToUnit(Base):
    __tablename__ = 'userToUnit'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    unit_id = Column(ForeignKey('unit.id'), primary_key=True, nullable=False)
    position = Column(String(256), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    unit = relationship('Unit', backref=backref("usertounits", lazy='dynamic'))
    user = relationship('User', backref=backref("usertounits", lazy='dynamic'))

    def __str__(self):
        return f"{self.user} - {self.unit}"


class FacilitySection(Base):
    __tablename__ = 'facilitySection'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    sectionType_id = Column(ForeignKey('sectionType.id'), nullable=False)
    safetyRequirements = Column(Text, nullable=False)
    facility_id = Column(ForeignKey('facility.id'), nullable=False)
    clearance_id = Column(ForeignKey('clearance.id'), nullable=False)
    sectionStatus_id = Column(ForeignKey('roomStatus.id'), nullable=False)
    specialAccessRequired = Column(Boolean, nullable=False)

    clearance = relationship('Clearance', backref=backref("facilitysections", lazy='dynamic'))
    facility = relationship('Facility', backref=backref("facilitysections", lazy='dynamic'))
    sectionStatus = relationship('RoomStatus', backref=backref("facilitysections", lazy='dynamic'))
    sectionType = relationship('SectionType', backref=backref("facilitysections", lazy='dynamic'))

    def __str__(self):
        return self.name


class Object(Base):
    __tablename__ = 'object'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(100), nullable=False)
    clearance_id = Column(ForeignKey('clearance.id'), nullable=False)
    containmentClass_id = Column(ForeignKey('containmentClass.id'), nullable=False)
    disruptionClass_id = Column(ForeignKey('disruptionClass.id'))
    riskClass_id = Column(ForeignKey('riskClass.id'))
    secondaryClass_id = Column(ForeignKey('secondaryClass.id'))
    facility_id = Column(ForeignKey('facility.id'))
    specialAccessRequired = Column(Boolean, nullable=False)

    clearance = relationship('Clearance', backref=backref("objects", lazy='dynamic'))
    containmentClass = relationship('ContainmentClass', backref=backref("objects", lazy='dynamic'))
    disruptionClass = relationship('DisruptionClass', backref=backref("objects", lazy='dynamic'))
    facility = relationship('Facility', backref=backref("objects", lazy='dynamic'))
    riskClass = relationship('RiskClass', backref=backref("objects", lazy='dynamic'))
    secondaryClass = relationship('SecondaryClass', backref=backref("objects", lazy='dynamic'))

    def __str__(self):
        return f"SCP-{self.id} {self.nickname}"


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = (
        ForeignKeyConstraint(('loginData_user_employeeClass_id', 'loginData_user_id'), ['loginData.user_employeeClass_id', 'loginData.user_id']),
    )

    id = Column(String(256), primary_key=True)
    accessStatus_id = Column(ForeignKey('accessStatus.id'), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    expire = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now', '+2 hour')"))
    loginData_user_employeeClass_id = Column(Integer, nullable=False)
    loginData_user_id = Column(Integer, nullable=False)

    accessStatus = relationship('AccessStatus', backref=backref("sessions", lazy='dynamic'))
    loginData_user = relationship('LoginData', backref=backref("sessions", lazy='dynamic'))

    def __str__(self):
        str = f"[{self.datetime}] {self.loginData_user}: {self.id}"
        if self.isExpired:
            str += " (expired)"
        return str

    @property
    def isExpired(self):
        return self.expire <= datetime.datetime.now()

    @property
    def isValid(self):
        return (not self.isExpired) and self.accessStatus.name == "Active"


class SystemAccess(Base):
    __tablename__ = 'systemAccess'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    systems_id = Column(ForeignKey('system.id'), primary_key=True, nullable=False)
    systemAccessRole_id = Column(ForeignKey('systemAccessRole.id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    systemAccessRole = relationship('SystemAccessRole', backref=backref("systemaccesses", lazy='dynamic'))
    system = relationship('System', backref=backref("systemaccesses", lazy='dynamic'))
    user = relationship('User', backref=backref("systemaccesses", lazy='dynamic'))

    def __str__(self):
        return f"[{self.system}] {self.user} - {self.systemAccessRole}"


class ObjectFile(Base):
    __tablename__ = 'objectFile'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(256), nullable=False)
    docLink = Column(String(200), primary_key=True, nullable=False)
    createdDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    object_id = Column(ForeignKey('object.id'), nullable=False)
    clearance_id = Column(ForeignKey('clearance.id'))
    docType_id = Column(ForeignKey('docType.id'), nullable=False)
    specialAccessRequired = Column(Boolean, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_employeeClass_id = Column(Integer, nullable=False)

    clearance = relationship('Clearance', backref=backref("objectfiles", lazy='dynamic'))
    docType = relationship('DocType', backref=backref("objectfiles", lazy='dynamic'))
    object = relationship('Object', backref=backref("objectfiles", lazy='dynamic'))
    user = relationship('User', backref=backref("objectfiles", lazy='dynamic'))

    def __str__(self):
        return f"[SCP-{self.object_id}] {self.name} (L{self.clearance_id})"


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    clearance_id = Column(ForeignKey('clearance.id'), nullable=False)
    roomStatus_id = Column(ForeignKey('roomStatus.id'), nullable=False)
    roomType_id = Column(ForeignKey('roomType.id'), nullable=False)
    parentRoom_id = Column(ForeignKey('room.id'))
    facilitySection_id = Column(ForeignKey('facilitySection.id'), nullable=False)
    specialAccessRequired = Column(Boolean, nullable=False)
    plan_id = Column(ForeignKey('userFile.id'))

    clearance = relationship('Clearance', backref=backref("rooms", lazy='dynamic'))
    facilitySection = relationship('FacilitySection', backref=backref("rooms", lazy='dynamic'))
    parentRoom = relationship('Room', remote_side=[id], backref=backref("childrooms", lazy='dynamic'))
    plan = relationship('UserFile')
    roomStatus = relationship('RoomStatus', backref=backref("rooms", lazy='dynamic'))
    roomType = relationship('RoomType', backref=backref("rooms", lazy='dynamic'))

    def __str__(self):
        return self.name


class UserObjectSpecialAccess(Base):
    __tablename__ = 'userObjectSpecialAccess'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    object_id = Column(ForeignKey('object.id'), primary_key=True, nullable=False)
    clearance_id = Column(ForeignKey('clearance.id'), primary_key=True, nullable=False)
    createdDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    expiryDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now', '+1 year')"))
    decree_id = Column(ForeignKey('userFile.id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    clearance = relationship('Clearance', backref=backref("userobjectspecialaccesses", lazy='dynamic'))
    decree = relationship('UserFile', backref=backref("userobjectspecialaccesses", lazy='dynamic'))
    object = relationship('Object', backref=backref("userobjectspecialaccesses", lazy='dynamic'))
    user = relationship('User', backref=backref("userobjectspecialaccesses", lazy='dynamic'))

    def __str__(self):
        return f"[SCP-{self.object_id}] {self.user} - {self.clearance_id}"

    @property
    def isExpired(self):
        return self.expiryDateTime <= datetime.datetime.now()


class UserToObject(Base):
    __tablename__ = 'userToObject'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    object_id = Column(ForeignKey('object.id'), primary_key=True, nullable=False)
    userToObjectRole_id = Column(ForeignKey('userToObjectRole.id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    object = relationship('Object', backref=backref("usertoobjects", lazy='dynamic'))
    userToObjectRole = relationship('UserToObjectRole', backref=backref("usertoobjects", lazy='dynamic'))
    user = relationship('User', backref=backref("usertoobjects", lazy='dynamic'))

    def __str__(self):
        return f"[SCP-{self.object_id}] {self.user} - {self.userToObjectRole}"


class UserRoomSpecialAccess(Base):
    __tablename__ = 'userRoomSpecialAccess'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    room_id = Column(ForeignKey('room.id'), primary_key=True, nullable=False)
    createdDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now')"))
    expiryDateTime = Column(DateTime(timezone=True), nullable=False, server_default=text("datetime('now', '+1 year')"))
    decree_id = Column(ForeignKey('userFile.id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    decree = relationship('UserFile', backref=backref("userroomspecialaccesses", lazy='dynamic'))
    room = relationship('Room', backref=backref("userroomspecialaccesses", lazy='dynamic'))
    user = relationship('User', backref=backref("userroomspecialaccesses", lazy='dynamic'))

    def __str__(self):
        return f"{self.user} - {self.room}"

    @property
    def isExpired(self):
        return self.expiryDateTime <= datetime.datetime.now()


class UserSectionSpecialAccess(Base):
    __tablename__ = 'userSectionSpecialAccess'
    __table_args__ = (
        ForeignKeyConstraint(('user_id', 'user_employeeClass_id'), ['user.id', 'user.employeeClass_id']),
    )

    facilitySection_id = Column(ForeignKey('facilitySection.id'), primary_key=True, nullable=False)
    createdDateTime = Column(DateTime, nullable=False, server_default=text("datetime('now')"))
    expiryDateTime = Column(DateTime, nullable=False, server_default=text("datetime('now', '+1 year')"))
    decree_id = Column(ForeignKey('userFile.id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_employeeClass_id = Column(Integer, primary_key=True, nullable=False)

    decree = relationship('UserFile', backref=backref("usersectionspecialaccesses", lazy='dynamic'))
    facilitySection = relationship('FacilitySection', backref=backref("usersectionspecialaccesses", lazy='dynamic'))
    user = relationship('User', backref=backref("usersectionspecialaccesses", lazy='dynamic'))

    def __str__(self):
        return f"{self.user} - {self.facilitySection}"

    @property
    def isExpired(self):
        return self.expiryDateTime <= datetime.datetime.now()


# Models for logCollector
class LogType(Base):
    __tablename__ = 'logType'

    id = Column(Integer, primary_key=True)
    name = Column(Text(256), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return self.name


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    system = Column(Text(256), nullable=False)
    logType_id = Column(ForeignKey('logType.id'), nullable=False)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    comment = Column(Text)
    datetime = Column(DateTime, nullable=False, server_default=text("datetime('now', 'localtime')"))
    optionalFields = Column(BLOB)

    logType = relationship('LogType')

    def __str__(self):
        optionalFields = ""
        if self.optionalFields:
            for key, value in loads(bytes(self.optionalFields)).items():
                if value is not None:
                    optionalFields += f"{key}: {value}\n"
        return f"[{self.datetime} {self.system}]\n" \
               f"Тип события: {self.logType}\n" \
               f"Резюме: {self.summary}\n" \
               f"Описание: {self.description}\n" \
               + (optionalFields if optionalFields else "") \
               + f"Комментарий: {self.comment if self.comment else ''}"


class Metalog(Base):
    __tablename__ = 'metalogs'

    id = Column(Integer, primary_key=True)
    logType_id = Column(ForeignKey('logType.id'), nullable=False)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    comment = Column(Text)
    datetime = Column(DateTime, nullable=False, server_default=text("datetime('now', 'localtime')"))
    optionalFields = Column(BLOB)

    logType = relationship('LogType')

    def __str__(self):
        optionalFields = ""
        if self.optionalFields:
            for key, value in loads(bytes(self.optionalFields)).items():
                optionalFields += f"{key}: {value}\n"
        return f"[{self.datetime}]\n" \
               f"Тип события: {self.logType}\n" \
               f"Резюме: {self.summary}\n" \
               f"Описание: {self.description}\n" \
               + (optionalFields if optionalFields else "") \
               + f"Комментарий: {self.comment if self.comment else ''}"
