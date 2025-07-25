import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Scores(SqlAlchemyBase):
    __tablename__ = 'scores'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    gamesid = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("games.id"))
    bestscore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
