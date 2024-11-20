import unittest
from unittest.mock import MagicMock
from components.admin.sqlAlchemy_admin_repository import SqlalchemyAdminRepository
from logging import Logger as StandardLogger
from components.database.models import Sector
from sqlalchemy.exc import IntegrityError


class TestSQLAlchemyAdminRepository(unittest.TestCase):
    def setUp(self):
        self.mock_connector = MagicMock()
        self.mock_connector.get_session.return_value = MagicMock()
        self.mock_logger = MagicMock(spec=StandardLogger)
        self.admin_repository = SqlalchemyAdminRepository(
            connector=self.mock_connector,
            logger=self.mock_logger,
        )

    def test_list_sectors_success(self):
        session = self.mock_connector.get_session.return_value
        mock_sector1 = MagicMock()
        mock_sector1.name = "Technology"
        mock_sector2 = MagicMock()
        mock_sector2.name = "Healthcare"

        session.query.return_value.all.return_value = [mock_sector1, mock_sector2]

        result = self.admin_repository.list_sectors()

        self.assertEqual(result, ["Technology", "Healthcare"])
        self.mock_connector.get_session.assert_called_once()
        session.query.assert_called_once_with(Sector.name)
        session.query.return_value.all.assert_called_once()

    def test_list_sectors_failure(self):
        session = self.mock_connector.get_session.return_value
        session.query.return_value.all.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.admin_repository.list_sectors()

        self.assertEqual(str(context.exception), "Database error")
        self.mock_logger.error.assert_called_once_with(
            "Failed to list sectors. Error: Database error"
        )

    def test_create_sector_success(self):
        self.admin_repository.sector_exists = MagicMock(return_value=False)
        session = self.mock_connector.get_session.return_value
        session.add = MagicMock()
        session.commit = MagicMock()

        self.admin_repository.create_sector("New Sector")

        self.admin_repository.sector_exists.assert_called_once_with("New Sector")
        session.add.assert_called_once()
        session.commit.assert_called_once()

    def test_create_sector_already_exists(self):
        self.admin_repository.sector_exists = MagicMock(return_value=True)

        with self.assertRaises(ValueError) as context:
            self.admin_repository.create_sector("Existing Sector")

        self.assertEqual(
            str(context.exception), "Sector with name 'Existing Sector' already exists."
        )
        self.admin_repository.sector_exists.assert_called_once_with("Existing Sector")

    def test_create_sector_exception_during_commit(self):
        self.admin_repository.sector_exists = MagicMock(return_value=False)
        session = self.mock_connector.get_session.return_value
        session.add = MagicMock()
        session.commit.side_effect = Exception("Database commit error")
        session.rollback = MagicMock()
        self.mock_logger.error = MagicMock()

        with self.assertRaises(ValueError) as context:
            self.admin_repository.create_sector("New Sector")

        self.assertEqual(
            str(context.exception), "Error creating sector: 'Database commit error'"
        )
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.rollback.assert_called_once()
        self.mock_logger.error.assert_called_once_with(
            "Failed to create sector. Error: Database commit error"
        )

    def test_delete_sector_success(self):
        session = self.mock_connector.get_session.return_value
        mock_sector = MagicMock()
        session.query.return_value.filter_by.return_value.first.return_value = (
            mock_sector
        )
        session.delete = MagicMock()
        session.commit = MagicMock()

        self.admin_repository.delete_sector("Existing Sector")

        session.query.assert_called_once_with(Sector)
        session.query.return_value.filter_by.assert_called_once_with(
            name="Existing Sector"
        )
        session.query.return_value.filter_by.return_value.first.assert_called_once()
        session.delete.assert_called_once_with(mock_sector)
        session.commit.assert_called_once()

    def test_delete_sector_not_found(self):
        session = self.mock_connector.get_session.return_value
        session.query.return_value.filter_by.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            self.admin_repository.delete_sector("Nonexistent Sector")

        self.assertEqual(
            str(context.exception), "Sector 'Nonexistent Sector' does not exist."
        )

    def test_delete_sector_integrity_error(self):
        session = self.mock_connector.get_session.return_value
        mock_sector = MagicMock()
        session.query.return_value.filter_by.return_value.first.return_value = (
            mock_sector
        )
        session.delete.side_effect = IntegrityError("Mock IntegrityError", None, None)
        session.rollback = MagicMock()
        self.mock_logger.error = MagicMock()

        with self.assertRaises(ValueError) as context:
            self.admin_repository.delete_sector("Existing Sector")

        self.assertEqual(
            str(context.exception),
            "Sector 'Existing Sector' cannot be deleted as it still contains associated industries.",
        )
        session.rollback.assert_called_once()
        self.mock_logger.error.assert_called_once_with(
            "Cannot delete sector 'Existing Sector' as it still has associated industries."
        )

    def test_delete_sector_general_exception(self):
        session = self.mock_connector.get_session.return_value
        mock_sector = MagicMock()
        session.query.return_value.filter_by.return_value.first.return_value = (
            mock_sector
        )
        session.delete.side_effect = Exception("Unexpected error")
        session.rollback = MagicMock()
        self.mock_logger.error = MagicMock()

        with self.assertRaises(ValueError) as context:
            self.admin_repository.delete_sector("Existing Sector")

        self.assertEqual(
            str(context.exception),
            "An error occurred while deleting sector 'Existing Sector'. Please try again.",
        )
        session.rollback.assert_called_once()
        self.mock_logger.error.assert_called_once_with(
            "Failed to delete sector 'Existing Sector'. Error: Unexpected error"
        )

    def test_update_sector_success(self):
        self.admin_repository.sector_exists = MagicMock(return_value=False)
        session = self.mock_connector.get_session.return_value
        mock_sector = MagicMock()
        session.query.return_value.filter_by.return_value.first.return_value = (
            mock_sector
        )
        session.commit = MagicMock()

        self.admin_repository.update_sector("Old Sector", "New Sector")

        self.admin_repository.sector_exists.assert_called_once_with("New Sector")
        session.query.assert_called_once_with(Sector)
        session.query.return_value.filter_by.assert_called_once_with(name="Old Sector")
        session.query.return_value.filter_by.return_value.first.assert_called_once()
        self.assertEqual(mock_sector.name, "New Sector")
        session.commit.assert_called_once()

    def test_update_sector_new_name_exists(self):
        self.admin_repository.sector_exists = MagicMock(return_value=True)

        with self.assertRaises(ValueError) as context:
            self.admin_repository.update_sector("Old Sector", "Existing Sector")

        self.assertEqual(
            str(context.exception), "The sector 'Existing Sector' already exists."
        )
        self.admin_repository.sector_exists.assert_called_once_with("Existing Sector")

    def test_update_sector_old_sector_not_found(self):
        self.admin_repository.sector_exists = MagicMock(return_value=False)
        session = self.mock_connector.get_session.return_value
        session.query.return_value.filter_by.return_value.first.return_value = None

        with self.assertRaises(ValueError) as context:
            self.admin_repository.update_sector("Nonexistent Sector", "New Sector")

        self.assertEqual(
            str(context.exception),
            "Sector with name 'Nonexistent Sector' does not exist.",
        )
        self.admin_repository.sector_exists.assert_called_once_with("New Sector")
        session.query.assert_called_once_with(Sector)
        session.query.return_value.filter_by.assert_called_once_with(
            name="Nonexistent Sector"
        )
        session.query.return_value.filter_by.return_value.first.assert_called_once()

    def test_update_sector_exception_during_update(self):
        self.admin_repository.sector_exists = MagicMock(return_value=False)
        session = self.mock_connector.get_session.return_value
        mock_sector = MagicMock()
        session.query.return_value.filter_by.return_value.first.return_value = (
            mock_sector
        )
        session.commit.side_effect = Exception("Database commit error")
        session.rollback = MagicMock()
        self.mock_logger.error = MagicMock()

        with self.assertRaises(ValueError) as context:
            self.admin_repository.update_sector("Old Sector", "New Sector")

        self.assertEqual(
            str(context.exception),
            "Failed to update sector 'Old Sector'. Error: Database commit error",
        )
        session.rollback.assert_called_once()
        self.mock_logger.error.assert_called_once_with(
            "Failed to update sector 'Old Sector'. Error: Database commit error"
        )

    def test_sector_exists_true(self):
        session = self.mock_connector.get_session.return_value
        session.query.return_value.filter_by.return_value.first.return_value = (
            MagicMock()
        )

        result = self.admin_repository.sector_exists("Existing Sector")

        self.assertTrue(result)
        session.query.assert_called_once_with(Sector.id)
        session.query.return_value.filter_by.assert_called_once_with(
            name="Existing Sector"
        )
        session.query.return_value.filter_by.return_value.first.assert_called_once()

    def test_sector_exists_false(self):
        session = self.mock_connector.get_session.return_value
        session.query.return_value.filter_by.return_value.first.return_value = None

        result = self.admin_repository.sector_exists("Nonexistent Sector")

        self.assertFalse(result)
        session.query.assert_called_once_with(Sector.id)
        session.query.return_value.filter_by.assert_called_once_with(
            name="Nonexistent Sector"
        )
        session.query.return_value.filter_by.return_value.first.assert_called_once()
