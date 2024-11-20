import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    _current_file_path = Path(__file__).resolve()

    def __init__(self):
        load_dotenv(self.project_root / ".env")

    @property
    def project_root(self):
        return self._current_file_path.parent.parent

    @property
    def data_dir(self):
        data_dir = os.getenv("DATA_DIR", "data")
        return self.project_root / data_dir

    @property
    def logo_path(self):
        return str(self.project_root / "src/img/logo_4_trans.png")

    @property
    def icon_path(self):
        return str(self.project_root / "src/img/logo_3_trans.png")

    @property
    def latest_migration_version(self):
        return "107bf1a9e7c7"
