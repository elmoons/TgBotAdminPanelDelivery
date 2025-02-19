from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import BaseOrm


class ProductsPoizonLinksOrm(BaseOrm):
    __tablename__ = "products_poizon"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()


class DataForFinalPrice(BaseOrm):
    __tablename__ = "data_final_price"

    id: Mapped[int] = mapped_column(primary_key=True)
    redemption_price_in_yuan: Mapped[float]
    yuan_to_ruble_exchange_rate: Mapped[float]
    delivery_price: Mapped[float]
    markup_coefficient: Mapped[float]
    additional_services_price: Mapped[float]
