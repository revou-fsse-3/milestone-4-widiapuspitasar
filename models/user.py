from models.base import Base
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    username = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    account = relationship("Account", cascade="all,delete-orphan")

    def serialize(self, full=True):
        if full:
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'password': self.password,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        else:
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email
            }
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = bcrypt.hashpw( password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    