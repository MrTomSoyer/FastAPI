# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Integer, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        """Вспомогательный метод для преобразования ORM-объекта в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description if self.description else "",
            "price": self.price,
            "author": self.author,
            "created_at": self.created_at,
        }