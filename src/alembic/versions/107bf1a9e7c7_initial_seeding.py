"""Initial seeding

Revision ID: 107bf1a9e7c7
Revises: 655efaa32764
Create Date: 2024-11-07 01:40:17.783511

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from components.database.models import Sector, Industry, MetricName

# revision identifiers, used by Alembic.
revision: str = "107bf1a9e7c7"
down_revision: Union[str, None] = "57f88376bd92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    with Session(bind=bind) as session:
        try:
            sectors_data = {
                "Communication Services": [
                    "Diversified Telecommunication Services",
                    "Entertainment",
                    "Interactive Media & Services",
                    "Media",
                    "Wireless Telecommunication Services",
                ],
                "Consumer Discretionary": [
                    "Auto Components",
                    "Automobiles",
                    "Distributors",
                    "Diversified Consumer Services",
                    "Hotels, Restaurants & Leisure",
                    "Household Durables",
                    "Internet & Direct Marketing Retail",
                    "Leisure Products",
                    "Multiline Retail",
                    "Specialty Retail",
                    "Textiles, Apparel & Luxury Goods",
                ],
                "Consumer Staples": [
                    "Beverages",
                    "Food & Staples Retailing",
                    "Food Products",
                    "Household Products",
                    "Personal Products",
                    "Tobacco",
                ],
                "Energy": [
                    "Energy Equipment & Services",
                    "Oil, Gas & Consumable Fuels",
                ],
                "Financials": [
                    "Banks",
                    "Capital Markets",
                    "Consumer Finance",
                    "Diversified Financial Services",
                    "Insurance",
                    "Mortgage Real Estate Investment Trusts (REITs)",
                    "Thrifts & Mortgage Finance",
                ],
                "Health Care": [
                    "Biotechnology",
                    "Health Care Equipment & Supplies",
                    "Health Care Providers & Services",
                    "Health Care Technology",
                    "Life Sciences Tools & Services",
                    "Pharmaceuticals",
                ],
                "Industrials": [
                    "Aerospace & Defense",
                    "Air Freight & Logistics",
                    "Airlines",
                    "Building Products",
                    "Commercial Services & Supplies",
                    "Construction & Engineering",
                    "Electrical Equipment",
                    "Industrial Conglomerates",
                    "Machinery",
                    "Marine",
                    "Professional Services",
                    "Road & Rail",
                    "Trading Companies & Distributors",
                    "Transportation Infrastructure",
                ],
                "Information Technology": [
                    "Communications Equipment",
                    "Electronic Equipment, Instruments & Components",
                    "IT Services",
                    "Semiconductors & Semiconductor Equipment",
                    "Software",
                    "Technology Hardware, Storage & Peripherals",
                ],
                "Materials": [
                    "Chemicals",
                    "Construction Materials",
                    "Containers & Packaging",
                    "Metals & Mining",
                    "Paper & Forest Products",
                ],
                "Real Estate": [
                    "Equity Real Estate Investment Trusts (REITs)",
                    "Real Estate Management & Development",
                ],
                "Utilities": [
                    "Electric Utilities",
                    "Gas Utilities",
                    "Independent Power and Renewable Electricity Producers",
                    "Multi-Utilities",
                    "Water Utilities",
                ],
            }

            metric_names = [
                "PE Ratio",
                "EPS",
                "Debt to Equity",
                "Current Ratio",
                "Return on Equity",
                "Return on Assets",
            ]

            sectors = []
            for sector_name, industries in sectors_data.items():
                sector = Sector(name=sector_name)
                session.add(sector)
                sectors.append((sector, industries))

            session.flush()  # Ensure sector IDs are available

            for sector, industries in sectors:
                for industry_name in industries:
                    industry = Industry(name=industry_name, sector_id=sector.id)
                    session.add(industry)

            for metric_name in metric_names:
                metric = MetricName(name=metric_name)
                session.add(metric)

            session.commit()
        except (sa.exc.SQLAlchemyError, ValueError) as e:
            session.rollback()
            raise e


def downgrade() -> None:
    bind = op.get_bind()
    with Session(bind=bind) as session:
        try:
            session.query(MetricName).delete()
            session.query(Industry).delete()
            session.query(Sector).delete()
            session.commit()
        except (sa.exc.SQLAlchemyError, ValueError) as e:
            session.rollback()
            raise e
