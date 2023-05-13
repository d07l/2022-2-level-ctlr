"""
Tests for POS frequency pipeline
"""
import json
import shutil
import unittest

import pytest

import core_utils.article.article as article_instance
import lab_6_pipeline.pos_frequency_pipeline as pos_freq_pipe
from config.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article.article import ArtifactType
from lab_6_pipeline.pipeline import CorpusManager
from lab_6_pipeline.pos_frequency_pipeline import (EmptyFileError,
                                                   POSFrequencyPipeline)
from lab_6_pipeline.tests.utils import pipeline_test_files_setup

UD_TAGS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM',
           'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']


class PosFrequencyPipelineTests(unittest.TestCase):
    """
    Class for testing POSFrequencyPipeline realization
    """

    @classmethod
    def setUpClass(cls) -> None:
        pipeline_test_files_setup()
        shutil.copyfile(PIPE_TEST_FILES_FOLDER /
                        "reference_score_six_test.conllu",
                        TEST_PATH /
                        f"1_{ArtifactType.MORPHOLOGICAL_CONLLU.value}.conllu")

        article_instance.ASSETS_PATH = TEST_PATH
        pos_freq_pipe.ASSETS_PATH = TEST_PATH

        cls.corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        path = cls.corpus_manager.get_articles()[1].get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            meta = json.load(meta_file)
        cls.frequencies = meta.pop('pos_frequencies')
        with open(path, 'w', encoding='utf-8') as meta_file:
            json.dump(meta,
                      meta_file,
                      sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))

        pos_pipe = POSFrequencyPipeline(cls.corpus_manager)
        pos_pipe.run()

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_meta_files_readable(self):
        """
        Ensure meta files are not corrupt
        """
        failed = False
        try:
            article = self.corpus_manager.get_articles()[1]
            path = article.get_meta_file_path()
            with open(path, 'r', encoding='utf-8') as meta_file:
                json.load(meta_file)
        except json.decoder.JSONDecodeError:
            failed = True
        finally:
            message = 'Generated meta files are corrupt: ' \
                      'check how you update .json files'
            self.assertFalse(failed, message)

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_frequencies_are_correct(self):
        """
        Ensure frequencies are counted correctly
        """
        article = self.corpus_manager.get_articles()[1]
        path = article.get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            frequencies = json.load(meta_file)['pos_frequencies']
        self.assertEqual(self.frequencies, frequencies,
                         'POS frequencies are calculated incorrectly')

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_images_are_generated(self):
        """
        Ensure images are generated
        """
        msg = 'POSFrequencyPipeline does not create image ' \
              'file for at least one of articles available'
        ids_available = set(
            map(
                lambda filename: int(str(filename.name).split('_', maxsplit=1)[0]),
                TEST_PATH.iterdir()
            )
        )
        for identifier in ids_available:
            path = TEST_PATH / f'{identifier}_image.png'
            self.assertTrue(path.is_file(), msg)

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_tags_are_ud(self):
        """
        Ensure that ud tags are used
        """
        article = self.corpus_manager.get_articles()[1]
        path = article.get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            pos_tags = json.load(meta_file)['pos_frequencies'].keys()
        for tag in pos_tags:
            self.assertTrue(tag in UD_TAGS,
                            msg=f"Tag {tag} not in list of known UD tags")

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    @pytest.mark.lab_6_pipeline
    def test_pos_throws_error(self):
        """
        Ensure that POS pipe raises EmptyFileError
        """
        with open(TEST_PATH / f"1_{ArtifactType.MORPHOLOGICAL_CONLLU.value}.conllu", 'w',
                  encoding='utf-8') as file:
            file.write('')

        new_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)

        new_pipe = POSFrequencyPipeline(new_manager)
        with self.assertRaises(EmptyFileError):
            new_pipe.run()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEST_PATH)
