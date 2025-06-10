import sqlalchemy
from .db_session import SqlAlchemyBase


class Investment(SqlAlchemyBase):
    __tablename__ = 'investments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
