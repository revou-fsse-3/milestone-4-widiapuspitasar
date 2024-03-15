from models.base import Base
from sqlalchemy import Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import func
from models.account import Account

class Transaction(Base):
    __tablename__ = "transaction"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("account.id", ondelete="CASCADE"))
    to_account_id = mapped_column(Integer, ForeignKey("account.id", ondelete="CASCADE"))
    amount = mapped_column(DECIMAL(precision=10, scale=2))
    type = mapped_column(String(255), nullable= False)
    description = mapped_column(String(255), nullable= False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship to Account model for the 'from_account'
    from_account = relationship("Account", foreign_keys=[from_account_id])

    # Relationship to Account model for the 'to_account'
    to_account = relationship("Account", foreign_keys=[to_account_id])

    def serialize(self, full=True):
        if full:
            return {
                'id': self.id,
                'from_account_id': self.from_account_id,
                'to_account_id': self.to_account_id,
                'amount': self.amount,
                'type': self.type,
                'created_at': self.created_at,
            }
        else:
            return {
                'id': self.id,
                'to_account_id': self.to_account_id,
                'amount': self.amount,
                'type': self.type,
            }