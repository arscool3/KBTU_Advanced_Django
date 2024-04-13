from datetime import datetime
from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class CryptoTrade(Base):
    __tablename__ = "crypto_trade"

    id: Mapped[_id]

    timestamp: Mapped[datetime]
    currency: Mapped[str]
    k_to_usd: Mapped[float]

