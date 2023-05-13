"""
Utils for core_utils tests
"""
import shutil

from config.test_params import CORE_UTILS_TEST_FILES_FOLDER, TEST_PATH
from core_utils.constants import ASSETS_PATH


def universal_setup() -> None:
    """
    Creation of required assets for the core_utils unit tests
    """
    TEST_PATH.mkdir(exist_ok=True)
    shutil.copyfile(CORE_UTILS_TEST_FILES_FOLDER / "1_raw.txt",
                    TEST_PATH / "1_raw.txt")
    shutil.copyfile(CORE_UTILS_TEST_FILES_FOLDER / "1_meta.json",
                    TEST_PATH / "1_meta.json")


def copy_student_data() -> None:
    """
    Copy student data to safe place for tests needs
    """
    TEST_PATH.mkdir(exist_ok=True)
    for file in ASSETS_PATH.iterdir():
        shutil.copyfile(ASSETS_PATH / file.name, TEST_PATH / file.name)
