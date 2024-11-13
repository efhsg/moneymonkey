from config import Config
from components.logger.native_logger import NativeLogger


def get_config() -> Config:
    return Config()


def get_logger(name: str = "docuchat"):
    return NativeLogger.get_logger(name)
