"""
Test for CorpusManager abstraction realization
"""
import shutil
import unittest

import pytest

from config.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article.article import Article
from lab_6_pipeline.pipeline import CorpusManager
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


class ArticleInstanceCreationBasicTest(unittest.TestCase):
    """
    Tests for basic aspects of CorpusManager realization
    """

    @classmethod
    def setUpClass(cls) -> None:
        pipeline_test_files_setup(meta=True)

    def setUp(self) -> None:
        self.corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    @pytest.mark.lab_6_pipeline
    def test_corpus_manager_instantiation(self):
        """
        Ensure that CorpusManager instances are instantiated correctly
        """
        self.assertTrue(hasattr(self.corpus_manager, '_storage'),
                        'CorpusManager instance must have _storage field')
        message = 'CorpusManager attribute _storage must be dict object'
        self.assertIsInstance(self.corpus_manager.get_articles(), dict,
                              message)
        message = 'CorpusManager attribute _storage must be ' \
                  'filled right away during initialisation'
        self.assertTrue(self.corpus_manager.get_articles(), message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    @pytest.mark.lab_6_pipeline
    def test_raw_files_are_found(self):
        """
        Ensure that CorpusManager finds all saved raw files
        """
        message = "Corpus Manager does not create " \
                  "article instances given raw files only"
        self.assertIn(1, self.corpus_manager.get_articles(), message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    @pytest.mark.lab_6_pipeline
    def test_corrupted_file_names(self):
        """
        Ensure that CorpusManager does not work with files with corrupted names.
        """
        shutil.copyfile(PIPE_TEST_FILES_FOLDER / "1_raw.txt",
                        TEST_PATH / "None.txt")
        new_corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        self.assertEqual(len(new_corpus_manager.get_articles()), 1)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    @pytest.mark.lab_6_pipeline
    def test_article_instance_is_created(self):
        """
        Ensure CorpusManager creates Article instances
        """
        message = "CorpusManager _storage values must be Article instances"
        self.assertIsInstance(self.corpus_manager.get_articles()[1],
                              Article, message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    @pytest.mark.lab_6_pipeline
    def test_article_instance_is_filled(self):
        """
        Ensure CorpusManager creates Article instances with text
        """
        message = "CorpusManager must store filled Article instances"
        text = 'Красивая - мама красиво, училась в ПДД и ' \
               'ЖКУ по адресу Львовская 10 лет с почтой test .'
        self.assertEqual(self.corpus_manager.get_articles()[1].text,
                         text, message)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEST_PATH)


class ArticleInstanceCreationAdvancedTest(unittest.TestCase):
    """
    Tests for extended aspects of CorpusManager realization
    """

    @classmethod
    def setUpClass(cls) -> None:
        pipeline_test_files_setup()

    def setUp(self) -> None:
        self.corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    @pytest.mark.lab_6_pipeline
    def test_meta_files_are_found(self):
        """
        Ensure CorpusManager finds all saved meta files
        """
        message = "Corpus Manager does not create article " \
                  "instances given both raw and meta files"
        self.assertIn(1, self.corpus_manager.get_articles(), message)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEST_PATH)
