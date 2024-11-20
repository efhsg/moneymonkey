from typing import List
from components.admin.interfaces.admin_repository import AdminRepository
from logging import Logger as StandardLogger
from components.database.interfaces.connector import Connector
from components.database.models import Sector
from sqlalchemy.exc import IntegrityError


class SqlalchemyAdminRepository(AdminRepository):

    def __init__(
        self,
        config=None,
        connector: Connector = None,
        logger: StandardLogger = None,
    ):
        self.config = config
        self.session = connector.get_session()
        self.logger = logger

    def list_sectors(self) -> List[str]:
        try:
            return [sector.name for sector in self.session.query(Sector.name).all()]
        except Exception as e:
            self.logger.error(f"Failed to list sectors. Error: {e}")
            raise

    def create_sector(self, name: str) -> None:
        if self.sector_exists(name):
            raise ValueError(f"Sector with name '{name}' already exists.")
        try:
            new_sector = Sector(name=name)
            self.session.add(new_sector)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Failed to create sector. Error: {e}")
            raise ValueError(f"Error creating sector: '{e}'")

    def delete_sector(self, name: str) -> None:
        try:
            sector = self.session.query(Sector).filter_by(name=name).first()
            if not sector:
                raise ValueError(f"Sector '{name}' does not exist.")
            self.session.delete(sector)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            self.logger.error(
                f"Cannot delete sector '{name}' as it still has associated industries."
            )
            raise ValueError(
                f"Sector '{name}' cannot be deleted as it still contains associated industries."
            )
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Failed to delete sector '{name}'. Error: {e}")
            if not isinstance(e, ValueError):
                raise ValueError(
                    f"An error occurred while deleting sector '{name}'. Please try again."
                ) from e
            else:
                raise

    def update_sector(self, old_name: str, new_name: str) -> None:
        if self.sector_exists(new_name):
            raise ValueError(f"The sector '{new_name}' already exists.")
        try:
            sector = self.session.query(Sector).filter_by(name=old_name).first()
            if sector:
                sector.name = new_name
                self.session.commit()
            else:
                raise ValueError(f"Sector with name '{old_name}' does not exist.")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Failed to update sector '{old_name}'. Error: {e}")
            if not isinstance(e, ValueError):
                raise ValueError(
                    f"Failed to update sector '{old_name}'. Error: {e}"
                ) from e
            else:
                raise

    def sector_exists(self, name: str) -> bool:
        result = self.session.query(Sector.id).filter_by(name=name).first()
        return result is not None
