import datetime
import decimal
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    func,
    Index,
    CheckConstraint,
    Numeric,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship, validates
import re

Base = declarative_base()


class Validatable:
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 100
    NAME_PATTERN = r"^[a-zA-Z0-9 `~!@#$%^&*()\-_+=\[\]{\}|\\:;\"'<>,\.\?/]+$"
    NAME_REGEX = re.compile(NAME_PATTERN)

    @validates("name")
    def validate_name(self, key, name):
        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Name exceeds maximum length of {self.MAX_NAME_LENGTH} characters: {name}"
            )
        if len(name) < self.MIN_NAME_LENGTH:
            raise ValueError(
                f"Name must be have a minimal length of {self.MIN_NAME_LENGTH} characters: {name}"
            )
        if not self.NAME_REGEX.match(name):
            raise ValueError(
                "Invalid name. Allowed characters include letters, digits, and most special characters found on a standard US keyboard. Received: "
                + name
            )
        return name


class Sector(Base, Validatable):
    __tablename__ = "sectors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    industries = relationship("Industry", back_populates="sector")


class Industry(Base, Validatable):
    __tablename__ = "industries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=False)
    sector = relationship("Sector", back_populates="industries")
    stocks = relationship("Stock", back_populates="industry")


class MetricName(Base, Validatable):
    __tablename__ = "metric_names"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    financial_metrics = relationship("FinancialMetric", back_populates="metric_name")


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), unique=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    industry_id = Column(Integer, ForeignKey("industries.id"), nullable=False)
    market_cap = Column(Numeric(precision=20, scale=2), nullable=True)
    price = Column(Numeric(precision=15, scale=4), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=func.now(),
        nullable=False,
    )
    stock_data = relationship("StockData", back_populates="stock")
    financial_metrics = relationship("FinancialMetric", back_populates="stock")
    dividend_yields = relationship("DividendYield", back_populates="stock")
    price_history = relationship("StockPriceHistory", back_populates="stock")
    industry = relationship("Industry", back_populates="stocks")

    __table_args__ = (
        Index("ix_ticker", "ticker", unique=True),
        Index("ix_created_at", "created_at"),
        Index("ix_updated_at", "updated_at"),
        CheckConstraint("price >= 0", name="check_price_non_negative"),
    )


class FinancialMetric(Base):
    __tablename__ = "financial_metrics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    metric_name_id = Column(Integer, ForeignKey("metric_names.id"), nullable=False)
    metric_value = Column(Numeric(precision=15, scale=2), nullable=False)
    date_recorded = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
    stock = relationship("Stock", back_populates="financial_metrics")
    metric_name = relationship("MetricName", back_populates="financial_metrics")

    __table_args__ = (
        CheckConstraint("metric_value >= 0", name="check_metric_value_non_negative"),
    )

    @validates("metric_value")
    def validate_metric_value(self, key, metric_value):
        try:
            rounded_value = round(decimal.Decimal(metric_value), 2)
        except decimal.InvalidOperation:
            raise ValueError(f"Invalid metric value: {metric_value}")
        if rounded_value < 0:
            raise ValueError(f"Metric value must be non-negative: {metric_value}")
        return rounded_value


class DividendYield(Base):
    __tablename__ = "dividend_yields"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    yield_value = Column(Numeric(precision=10, scale=4), nullable=False)
    date_recorded = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
    stock = relationship("Stock", back_populates="dividend_yields")

    __table_args__ = (
        CheckConstraint("yield_value >= 0", name="check_yield_value_non_negative"),
    )


class StockPriceHistory(Base):
    __tablename__ = "stock_price_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    price = Column(Numeric(precision=15, scale=4), nullable=False)
    date_recorded = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
    stock = relationship("Stock", back_populates="price_history")


class DataSource(Base, Validatable):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    website = Column(String(255), nullable=True)
    stock_data = relationship("StockData", back_populates="source")

    from sqlalchemy import JSON


class StockData(Base):
    __tablename__ = "stock_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    date_recorded = Column(DateTime(timezone=True), nullable=False)
    data = Column(JSON, nullable=False)
    stock = relationship("Stock", back_populates="stock_data")
    source = relationship("DataSource", back_populates="stock_data")

    __table_args__ = (
        Index("ix_stock_source_date", "stock_id", "source_id", "date_recorded"),
    )
