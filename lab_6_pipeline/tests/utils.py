"""
Utils for lab_6_pipeline tests
"""
import shutil

from config.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from core_utils.constants import ASSETS_PATH
from core_utils.tests.utils import copy_student_data
from lab_6_pipeline.pipeline import (CorpusManager,
                                     MorphologicalAnalysisPipeline)


def pipeline_test_files_setup(txt=True, meta=True):
    """
    Set up TEST_PATH to work with test files
    """
    TEST_PATH.mkdir(exist_ok=True)
    if txt:
        shutil.copyfile(PIPE_TEST_FILES_FOLDER / "1_raw.txt",
                        TEST_PATH / "1_raw.txt")
    if meta:
        shutil.copyfile(PIPE_TEST_FILES_FOLDER / "1_meta.json",
                        TEST_PATH / "1_meta.json")


def pipeline_setup() -> None:
    """
    Set up TEST_PATH for MorphologicalAnalysisPipeline tests
    """
    TEST_PATH.mkdir(exist_ok=True)
    if any(ASSETS_PATH.iterdir()):
        copy_student_data()
    else:
        article.ASSETS_PATH = TEST_PATH
        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = MorphologicalAnalysisPipeline(corpus_manager)
        pipe.run()
