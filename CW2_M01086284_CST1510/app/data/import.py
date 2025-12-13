from pathlib import Path

#------------------------------creating path manager class--------------------------------

class PathManager:
    def __init__(self, data_dir="DATA", db_name="intelligence_platform02.db"):
        """Initialize the PathManager with a data folder and database file name."""

        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / db_name
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create the data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_data_dir(self):
        """Return the resolved path of the data directory."""
        return self.data_dir.resolve()

    def get_db_path(self):
        """Return the resolved path of the database file."""
        return self.db_path.resolve()

    def print_paths(self):
        """Print info about the data folder and database path."""
        print("Imports successful!")
        print(f"DATA folder: {self.get_data_dir()}")
        print(f"Database will be created at: {self.get_db_path()}")