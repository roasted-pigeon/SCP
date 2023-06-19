# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accesscard(models.Model):
    card_id = models.CharField(primary_key=True, max_length=255)
    status = models.ForeignKey('Accessstatus', models.DO_NOTHING)
    datetime = models.DateTimeField()
    expire = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    user_employeeclass = models.ForeignKey('User', models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='accesscard_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accesscard'
        db_table_comment = 'This table stores records of all cards (passes)'


class Accessstatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'accessstatus'
        db_table_comment = 'This table stores records of possible access statuses'


class Clearance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'clearance'
        db_table_comment = 'This table stores records of possible clearance levels'


class Containmentclass(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'containmentclass'
        db_table_comment = 'This table stores records of possible containment classes'


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'department'
        db_table_comment = 'This table stores records of all departments of the Foundation'


class Disruptionclass(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'disruptionclass'
        db_table_comment = 'This table stores records of possible disruption classes'


class Doctype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.IntegerField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'doctype'
        db_table_comment = 'This table stores records of possible document types'


class Employeeclass(models.Model):
    id = models.IntegerField(primary_key=True)
    letter = models.CharField(unique=True, max_length=1)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'employeeclass'
        db_table_comment = 'This table stores records of possible staff classes'


class Facility(models.Model):
    id = models.IntegerField(primary_key=True)
    width = models.FloatField()
    length = models.FloatField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    facilitytype = models.ForeignKey('Facilitytype', models.DO_NOTHING, db_column='facilityType_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facility'
        db_table_comment = "This table stores records of all the Foundation''s facilities"


class Facilitysection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    sectiontype = models.ForeignKey('Sectiontype', models.DO_NOTHING, db_column='sectionType_id')  # Field name made lowercase.
    safetyrequirements = models.TextField(db_column='safetyRequirements')  # Field name made lowercase.
    facility = models.ForeignKey(Facility, models.DO_NOTHING)
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING)
    sectionstatus = models.ForeignKey('Roomstatus', models.DO_NOTHING, db_column='sectionStatus_id')  # Field name made lowercase.
    specialaccessrequired = models.IntegerField(db_column='specialAccessRequired')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'facilitysection'
        db_table_comment = 'This table stores records of all sections within the facilities'


class Facilitytype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'facilitytype'
        db_table_comment = 'This table stores records of possible facility types'


class Fileaccess(models.Model):
    filetype = models.OneToOneField('Filetype', models.DO_NOTHING, db_column='fileType_id', primary_key=True)  # Field name made lowercase. The composite primary key (fileType_id, fileAccessType_id, fileRequester_fileRequesterType_id, fileRequester_fileRequester_id) found, that is not supported. The first column is selected.
    fileaccesstype = models.ForeignKey('Fileaccesstype', models.DO_NOTHING, db_column='fileAccessType_id')  # Field name made lowercase.
    filerequester_filerequestertype = models.ForeignKey('Filerequester', models.DO_NOTHING, db_column='fileRequester_fileRequesterType_id')  # Field name made lowercase.
    filerequester_filerequester = models.ForeignKey('Filerequester', models.DO_NOTHING, db_column='fileRequester_fileRequester_id', to_field='fileRequester_id', related_name='fileaccess_filerequester_filerequester_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fileaccess'
        unique_together = (('filetype', 'fileaccesstype', 'filerequester_filerequestertype', 'filerequester_filerequester'),)
        db_table_comment = 'This table stores records of all file permissions'


class Fileaccesstype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'fileaccesstype'
        db_table_comment = 'This table stores records of possible file access types'


class Filerequester(models.Model):
    filerequestertype = models.OneToOneField('Filerequestertype', models.DO_NOTHING, db_column='fileRequesterType_id', primary_key=True)  # Field name made lowercase. The composite primary key (fileRequesterType_id, fileRequester_id) found, that is not supported. The first column is selected.
    filerequester_id = models.CharField(db_column='fileRequester_id', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'filerequester'
        unique_together = (('filerequestertype', 'filerequester_id'),)


class Filerequestertype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'filerequestertype'
        db_table_comment = 'This table stores records of possible types of user-to-file relationships'


class Filetype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'filetype'
        db_table_comment = 'This table stores records of possible file types'


class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job'
        db_table_comment = 'This table stores records of all positions in all departments of the Foundation'


class Logindata(models.Model):
    login = models.CharField(unique=True, max_length=40)
    password = models.CharField(max_length=255)
    status = models.ForeignKey(Accessstatus, models.DO_NOTHING)
    expire = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    user_employeeclass = models.OneToOneField('User', models.DO_NOTHING, db_column='user_employeeClass_id', primary_key=True, related_name='logindata_user_employeeclass_set')  # Field name made lowercase. The composite primary key (user_employeeClass_id, user_id) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'logindata'
        unique_together = (('user_employeeclass', 'user'),)
        db_table_comment = 'This table stores records of all employee credentials'


class Object(models.Model):
    id = models.IntegerField(primary_key=True)
    nickname = models.CharField(max_length=100)
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING)
    containmentclass = models.ForeignKey(Containmentclass, models.DO_NOTHING, db_column='containmentClass_id')  # Field name made lowercase.
    disruptionclass = models.ForeignKey(Disruptionclass, models.DO_NOTHING, db_column='disruptionClass_id', blank=True, null=True)  # Field name made lowercase.
    riskclass = models.ForeignKey('Riskclass', models.DO_NOTHING, db_column='riskClass_id', blank=True, null=True)  # Field name made lowercase.
    secondaryclass = models.ForeignKey('Secondaryclass', models.DO_NOTHING, db_column='secondaryClass_id', blank=True, null=True)  # Field name made lowercase.
    facility = models.ForeignKey(Facility, models.DO_NOTHING, blank=True, null=True)
    specialaccessrequired = models.IntegerField(db_column='specialAccessRequired')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'object'
        db_table_comment = 'This table stores records of all objects contained by the Foundation'


class Objectfile(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=255)
    doclink = models.CharField(db_column='docLink', primary_key=True, max_length=200)  # Field name made lowercase. The composite primary key (docLink, id) found, that is not supported. The first column is selected.
    createddatetime = models.DateTimeField(db_column='createdDateTime')  # Field name made lowercase.
    object = models.ForeignKey(Object, models.DO_NOTHING)
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING, blank=True, null=True)
    doctype = models.ForeignKey(Doctype, models.DO_NOTHING, db_column='docType_id')  # Field name made lowercase.
    specialaccessrequired = models.IntegerField(db_column='specialAccessRequired')  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING)
    user_employeeclass = models.ForeignKey('User', models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='objectfile_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'objectfile'
        unique_together = (('doclink', 'id'),)
        db_table_comment = 'This table stores records of all files directly related to objects'


class Riskclass(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'riskclass'
        db_table_comment = 'This table stores records of possible risk classes'


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING)
    roomstatus = models.ForeignKey('Roomstatus', models.DO_NOTHING, db_column='roomStatus_id')  # Field name made lowercase.
    roomtype = models.ForeignKey('Roomtype', models.DO_NOTHING, db_column='roomType_id')  # Field name made lowercase.
    parentroom = models.ForeignKey('self', models.DO_NOTHING, db_column='parentRoom_id', blank=True, null=True)  # Field name made lowercase.
    facilitysection = models.ForeignKey(Facilitysection, models.DO_NOTHING, db_column='facilitySection_id')  # Field name made lowercase.
    specialaccessrequired = models.IntegerField(db_column='specialAccessRequired')  # Field name made lowercase.
    plan = models.ForeignKey('Userfile', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room'
        db_table_comment = 'This table stores records of all rooms in all sections of all facilities of the Foundation'


class Roomstatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'roomstatus'
        db_table_comment = 'This table stores records of possible room statuses'


class Roomtype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'roomtype'
        db_table_comment = 'This table stores records of possible room types'


class Secondaryclass(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'secondaryclass'
        db_table_comment = 'This table stores records of possible secondary classes'


class Sectiontype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'sectiontype'
        db_table_comment = 'This table stores records of possible section types'


class Session(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    accessstatus = models.ForeignKey(Accessstatus, models.DO_NOTHING, db_column='accessStatus_id')  # Field name made lowercase.
    datetime = models.DateTimeField()
    expire = models.DateTimeField()
    logindata_user_employeeclass = models.ForeignKey(Logindata, models.DO_NOTHING, db_column='loginData_user_employeeClass_id')  # Field name made lowercase.
    logindata_user = models.ForeignKey(Logindata, models.DO_NOTHING, db_column='loginData_user_id', to_field='user_id', related_name='session_logindata_user_set')  # Field name made lowercase.
    system = models.ForeignKey('System', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'session'
        db_table_comment = "This table stores records of all authorization sessions of the Foundation''s employees"


class System(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    purpose = models.TextField()
    description = models.TextField(blank=True, null=True)
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING)
    documentation = models.ForeignKey('Userfile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system'
        db_table_comment = 'This table stores records of all internal information systems of the Foundation'


class Systemaccess(models.Model):
    systems = models.OneToOneField(System, models.DO_NOTHING, primary_key=True)  # The composite primary key (systems_id, user_employeeClass_id, user_id, systemAccessRole_id) found, that is not supported. The first column is selected.
    systemaccessrole = models.ForeignKey('Systemaccessrole', models.DO_NOTHING, db_column='systemAccessRole_id')  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING)
    user_employeeclass = models.ForeignKey('User', models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='systemaccess_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'systemaccess'
        unique_together = (('systems', 'user_employeeclass', 'user', 'systemaccessrole'),)
        db_table_comment = 'This table stores records of all `system` permissions'


class Systemaccessrole(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'systemaccessrole'
        db_table_comment = 'This table stores records about possible user roles in the `system` (for example: user or administrator)'


class Unit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'unit'
        db_table_comment = 'This table stores records of possible divisions, groups, units, etc. in which the employees of the Foundation are members'


class User(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, employeeClass_id) found, that is not supported. The first column is selected.
    gender = models.IntegerField()
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dateofbirth = models.DateField(db_column='dateOfBirth')  # Field name made lowercase.
    rotationdate = models.DateField(db_column='rotationDate', blank=True, null=True)  # Field name made lowercase.
    photolink = models.CharField(db_column='photoLink', max_length=200, blank=True, null=True)  # Field name made lowercase.
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING)
    job = models.ForeignKey(Job, models.DO_NOTHING)
    facility = models.ForeignKey(Facility, models.DO_NOTHING)
    employeeclass = models.ForeignKey(Employeeclass, models.DO_NOTHING, db_column='employeeClass_id')  # Field name made lowercase.
    decree = models.ForeignKey('Userfile', models.DO_NOTHING, blank=True, null=True)
    supervisor = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    supervisor_employeeclass = models.ForeignKey('self', models.DO_NOTHING, db_column='supervisor_employeeClass_id', to_field='employeeClass_id', related_name='user_supervisor_employeeclass_set', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('id', 'employeeclass'),)
        db_table_comment = "This table stores records of all the Foundation''s staff"


class Userfile(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.IntegerField()
    clearance = models.ForeignKey(Clearance, models.DO_NOTHING)
    createddatetime = models.DateTimeField(db_column='createdDateTime')  # Field name made lowercase.
    doclink = models.IntegerField(db_column='docLink')  # Field name made lowercase.
    filetype = models.ForeignKey(Filetype, models.DO_NOTHING, db_column='fileType_id')  # Field name made lowercase.
    creator = models.ForeignKey(User, models.DO_NOTHING)
    creator_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='creator_employeeClass_id', to_field='employeeClass_id', related_name='userfile_creator_employeeclass_set')  # Field name made lowercase.
    associated_with = models.ForeignKey(User, models.DO_NOTHING, related_name='userfile_associated_with_set', blank=True, null=True)
    associated_with_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='associated_with_employeeClass_id', to_field='employeeClass_id', related_name='userfile_associated_with_employeeclass_set', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userfile'
        db_table_comment = 'This table stores records of all user files of the Foundation'


class Userfilespecialaccess(models.Model):
    userfile = models.OneToOneField(Userfile, models.DO_NOTHING, db_column='userFile_id', primary_key=True)  # Field name made lowercase. The composite primary key (userFile_id, user_id, user_employeeClass_id) found, that is not supported. The first column is selected.
    createddatetime = models.DateTimeField(db_column='createdDateTime')  # Field name made lowercase.
    expirydatetime = models.DateTimeField(db_column='expiryDateTime')  # Field name made lowercase.
    decree = models.ForeignKey(Userfile, models.DO_NOTHING, related_name='userfilespecialaccess_decree_set')
    user = models.ForeignKey(User, models.DO_NOTHING)
    user_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='userfilespecialaccess_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userfilespecialaccess'
        unique_together = (('userfile', 'user', 'user_employeeclass'),)
        db_table_comment = 'This table stores records of all special access permissions of employees to files'


class Userobjectspecialaccess(models.Model):
    object = models.ForeignKey(Object, models.DO_NOTHING)
    clearance = models.OneToOneField(Clearance, models.DO_NOTHING, primary_key=True)  # The composite primary key (clearance_id, object_id, user_id, user_employeeClass_id) found, that is not supported. The first column is selected.
    createddatetime = models.DateTimeField(db_column='createdDateTime')  # Field name made lowercase.
    expirydatetime = models.DateTimeField(db_column='expiryDateTime')  # Field name made lowercase.
    decree = models.ForeignKey(Userfile, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    user_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='userobjectspecialaccess_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userobjectspecialaccess'
        unique_together = (('clearance', 'object', 'user', 'user_employeeclass'),)
        db_table_comment = 'This table stores records of all special access permissions of employees to objects'


class Userroomspecialaccess(models.Model):
    room = models.OneToOneField(Room, models.DO_NOTHING, primary_key=True)  # The composite primary key (room_id, user_employeeClass_id, user_id) found, that is not supported. The first column is selected.
    createddatetime = models.DateTimeField(db_column='createdDateTime')  # Field name made lowercase.
    expirydatetime = models.DateTimeField(db_column='expiryDateTime')  # Field name made lowercase.
    decree = models.ForeignKey(Userfile, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    user_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='userroomspecialaccess_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userroomspecialaccess'
        unique_together = (('room', 'user_employeeclass', 'user'),)
        db_table_comment = 'This table stores records of all special access permissions of employees to rooms'


class Usersectionspecialaccess(models.Model):
    facilitysection = models.OneToOneField(Facilitysection, models.DO_NOTHING, db_column='facilitySection_id', primary_key=True)  # Field name made lowercase. The composite primary key (facilitySection_id, user_id, user_employeeClass_id) found, that is not supported. The first column is selected.
    createddatetime = models.DateTimeField(db_column='createdDateTime')  # Field name made lowercase.
    expirydatetime = models.DateTimeField(db_column='expiryDateTime')  # Field name made lowercase.
    decree = models.ForeignKey(Userfile, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    user_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='usersectionspecialaccess_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usersectionspecialaccess'
        unique_together = (('facilitysection', 'user', 'user_employeeclass'),)
        db_table_comment = 'This table stores records of all special access permissions of employees to rooms'


class Usertoobject(models.Model):
    object = models.OneToOneField(Object, models.DO_NOTHING, primary_key=True)  # The composite primary key (object_id, user_id, user_employeeClass_id) found, that is not supported. The first column is selected.
    usertoobjectrole = models.ForeignKey('Usertoobjectrole', models.DO_NOTHING, db_column='userToObjectRole_id')  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING)
    user_employeeclass = models.ForeignKey(User, models.DO_NOTHING, db_column='user_employeeClass_id', to_field='employeeClass_id', related_name='usertoobject_user_employeeclass_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usertoobject'
        unique_together = (('object', 'user', 'user_employeeclass'),)
        db_table_comment = 'This table stores records of all user-to-object relationships'


class Usertoobjectrole(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'usertoobjectrole'
        db_table_comment = 'This table stores records about possible employees roles in relation to the objects (for example: researcher or curator)'


class Usertounit(models.Model):
        db_table = 'usertounit'
        unique_together = (('unit', 'user_employeeclass', 'user'),)
        db_table_comment = 'This table stores records about possible employees roles in relation to the units (divisions, groups, etc.)(for example: Commander, Deputy Commander or Officer)'
