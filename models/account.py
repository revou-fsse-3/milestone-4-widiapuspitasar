from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from models.base import Base


class Account(Base):
    __tablename__ = 'account'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('user.id', ondelete="CASCADE")) 
    account_type = mapped_column(String(255))
    account_number = mapped_column(String(255), unique=True)
    balance = mapped_column(DECIMAL(10, 2))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    # user = relationship("User", back_populates="account")
    user = relationship("User", back_populates="account")

    def serialize(self, full=True):
        if full:
            return {
                'id': self.id,
                'user_id': self.user_id,
                'account_type': self.account_type,
                'account_number': self.account_number,
                'balance': self.balance,
                'created_at': self.created_at,
                'updated_at': self.updated_at
        }
        else:
            return {
                'id': self.id,
                'user_id': self.user_id,
                'account_type': self.account_type,
                'account_number': self.account_number,
            }
    

    def __repr__(self):
        return f'<Account {self.account_number}>'
