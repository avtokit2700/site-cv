from peewee import *

db = SqliteDatabase('users.db')


class User(Model):
    id = PrimaryKeyField()
    login = CharField()
    password = CharField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_table(User, safe=True)
