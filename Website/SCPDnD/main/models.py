from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Audio(models.Model):
    audio_id = models.AutoField(primary_key=True)
    uploader = models.ForeignKey('User', models.DO_NOTHING)
    upload_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    file_link = models.CharField(max_length=255)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'audio'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Character(models.Model):
    character_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey('User', models.DO_NOTHING)
    game = models.ForeignKey('Game', models.DO_NOTHING)
    title = models.CharField(max_length=100)
    content = models.JSONField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'character'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    next_session_date = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey('User', models.DO_NOTHING)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'game'


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    uploader = models.ForeignKey('User', models.DO_NOTHING)
    upload_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    file_link = models.CharField(max_length=255)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'image'


class Participant(models.Model):
    game = models.OneToOneField(Game, models.DO_NOTHING, primary_key=True)  # The composite primary key (game_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey('User', models.DO_NOTHING)
    isgm = models.IntegerField(db_column='isGM')  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'participant'
        unique_together = (('game', 'user'),)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=255)
    registration_date = models.DateTimeField()
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'user'

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    uploader = models.ForeignKey('User', models.DO_NOTHING)
    upload_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    file_link = models.CharField(max_length=255)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'document'