from components.admin.interfaces.admin_repository import AdminRepository
from components.admin.sqlAlchemy_admin_repository import SqlalchemyAdminRepository
from components.database.interfaces.connector import Connector
from components.database.mysql_connector import MySQLConnector
from config import Config
from components.logger.native_logger import NativeLogger


def get_config() -> Config:
    return Config()


def get_logger(name: str = "moneymonkey"):
    return NativeLogger.get_logger(name)


def get_connector() -> Connector:
    return MySQLConnector()


def get_admin_repository() -> AdminRepository:
    return SqlalchemyAdminRepository(
        connector=MySQLConnector(),
        logger=NativeLogger.get_logger(),
    )
