from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import BaseOrm


class ProductsPoizonLinksOrm(BaseOrm):
    __tablename__ = "products_poizon"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
