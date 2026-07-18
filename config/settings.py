from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


class Settings:
    """
    Framework and application settings.
    Browser selection is intentionally NOT defined here and should be
    supplied through pytest command-line options.
    """

    # ------------------------------------------------------------------
    # Application URLs
    # ------------------------------------------------------------------
    BASE_URL = "https://practicesoftwaretesting.com"
    LOGIN_URL = f"{BASE_URL}/auth/login"
    ACCOUNTS_URL = f"{BASE_URL}/account"
    API_BASE_URL = "https://api.practicesoftwaretesting.com"

    # ------------------------------------------------------------------
    # Browser Launch Settings
    # ------------------------------------------------------------------
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))

    VIEWPORT = {
        "width": 1920,
        "height": 1080
    }

    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
    AUTH_RETRY_COUNT = int(os.getenv("AUTH_RETRY_COUNT", "3"))

    # ------------------------------------------------------------------
    # Artifacts
    # ------------------------------------------------------------------
    ARTIFACT_DIR = os.path.join(Path(__file__).resolve().parent.parent, "artifacts")
    SCREENSHOT_DIR = os.path.join(ARTIFACT_DIR, "screenshots")
    TRACE_DIR = os.path.join(ARTIFACT_DIR, "traces")
    VIDEO_DIR = os.path.join(ARTIFACT_DIR, "videos")

    # ------------------------------------------------------------------
    # Optional Features
    # ------------------------------------------------------------------
    ENABLE_TRACE = os.getenv("ENABLE_TRACE", "true").lower() == "true"
    ENABLE_VIDEO = os.getenv("ENABLE_VIDEO", "false").lower() == "true"

    # ------------------------------------------------------------------
    # Worker Credentials
    # ------------------------------------------------------------------
    @staticmethod
    def get_worker_credentials(worker_id: str) -> dict:
        """
        Returns credentials assigned to a pytest-xdist worker.

        Example:
            WORKER_gw0_USER
            WORKER_gw0_PASS
            WORKER_gw0_NAME
        """

        credentials = {
            "username": os.getenv(f"WORKER_{worker_id}_USER"),
            "password": os.getenv(f"WORKER_{worker_id}_PASS"),
            "name": os.getenv(f"WORKER_{worker_id}_NAME"),
        }

        missing = [key for key, value in credentials.items() if not value]

        if missing:
            raise RuntimeError(
                f"Missing environment variables for worker "
                f"'{worker_id}': {', '.join(missing)}"
            )

        return credentials

    @staticmethod
    def _get_artifact_path( root_dir: str, browser_name: str, worker_id: str,
                           test_name: str, extension: str) -> Path:
        artifact_dir = Path(os.path.join(root_dir, browser_name))
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return os.path.join(artifact_dir, f"{test_name}_{worker_id}.{extension}")

    @staticmethod
    def get_screenshot_path(browser_name: str, worker_id: str, test_name: str) -> Path:
        return Settings._get_artifact_path(Settings.SCREENSHOT_DIR, browser_name, worker_id, test_name , "png")

    @staticmethod
    def get_trace_path(browser_name: str, worker_id: str, test_name: str) -> Path:
        return Settings._get_artifact_path(Settings.TRACE_DIR, browser_name, worker_id, test_name , "zip")
