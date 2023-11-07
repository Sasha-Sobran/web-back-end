from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

db = SQLAlchemy()


class Bank(db.Model):
    __tablename__ = "bank"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    count_of_clients: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String)

    def __init__(self, title, count_of_clients, description, image, id=None):
        self.id = None if id is None else id
        self.title = title
        self.count_of_clients = count_of_clients
        self.description = description
        self.image = image
