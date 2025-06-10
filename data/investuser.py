import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class InvestUser(SqlAlchemyBase):
    __tablename__ = 'investments_users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    investmentsid = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey("investments.id"))
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
