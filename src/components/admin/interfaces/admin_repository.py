from abc import ABC, abstractmethod
from typing import List


class AdminRepository(ABC):

    @abstractmethod
    def create_sector(self, name: str) -> None:
        pass

    @abstractmethod
    def list_sectors(self) -> List[str]:
        pass

    @abstractmethod
    def delete_sector(self, name: str) -> None:
        pass

    @abstractmethod
    def update_sector(self, old_name: str, new_name: str) -> None:
        pass

    @abstractmethod
    def sector_exists(self, name: str) -> bool:
        pass    