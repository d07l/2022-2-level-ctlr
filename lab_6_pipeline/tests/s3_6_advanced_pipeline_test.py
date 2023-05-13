# pylint: disable=protected-access
"""
Tests for advances morphological analysis pipeline
"""
import shutil
import unittest
from pathlib import Path

import pytest
from pymorphy2 import MorphAnalyzer

from config.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from core_utils.article.ud import TagConverter
from lab_6_pipeline.pipeline import (AdvancedMorphologicalAnalysisPipeline,
                                     CorpusManager, OpenCorporaTagConverter)
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


class OpenCorporaTagConverterTest(unittest.TestCase):
    """
    Class for checking Open Corpora tag converted
    """

    def setUp(self) -> None:
        mapping_dir_path = Path(__file__).parent.parent / 'data'
        self.mapping_file_path = mapping_dir_path / 'opencorpora_tags_mapping.json'
        self._backup_analyzer = MorphAnalyzer()

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_inheritance(self):
        """
        Test that OpenCorporaTagConverter is inherited
        from correct parent class
        """
        converter = OpenCorporaTagConverter(self.mapping_file_path)
        self.assertIsInstance(converter, TagConverter)

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_convert_pos(self):
        """
        Test correctness of part-of-speech tags conversion
        """
        converter = OpenCorporaTagConverter(self.mapping_file_path)
        backup_tag_sets = self._backup_analyzer.tag('спектакль')
        converted_tag_sets = [
            converter.convert_pos(analysis) for analysis in backup_tag_sets
        ]
        self.assertTrue(all(tag == 'NOUN' for tag in converted_tag_sets))

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_convert_morphological_tags(self):
        """
        Test correctness of morphological tags conversion
        """
        converter = OpenCorporaTagConverter(self.mapping_file_path)
        backup_tag_sets = self._backup_analyzer.tag('спектакль')
        converted_analysis = [
            converter.convert_morphological_tags(analysis)
            for analysis in backup_tag_sets
        ]
        expected = [
            'Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing',
            'Animacy=Inan|Case=Acc|Gender=Masc|Number=Sing',
        ]
        self.assertEqual(expected, converted_analysis)


class AdvancedMorphologicalAnalysisPipelineTest(unittest.TestCase):
    """
    Class for checking advanced morphological pipeline
    """

    def setUp(self) -> None:
        pipeline_test_files_setup()
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        self.pipeline = AdvancedMorphologicalAnalysisPipeline(corpus_manager)
        self.pipeline.run()
        self.raw_text = corpus_manager.get_articles()[1].get_raw_text()

        path = PIPE_TEST_FILES_FOLDER / 'reference_score_ten_test.conllu'
        with path.open('r', encoding='utf-8') as ref:
            self.conllu_reference = ref.read()
        self.expected_text_w_morph = self.conllu_reference

        path = PIPE_TEST_FILES_FOLDER / 'reference_score_ten_wo_morph_test.conllu'
        with path.open('r', encoding='utf-8') as ref:
            self.conllu_reference = ref.read()
        self.expected_text_wo_morph = self.conllu_reference

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_processing_with_morph_tags(self):
        """
        Test advanced processing with morphological tags
        """
        conllu_sentences = self.pipeline._process(self.raw_text)
        expected_sentences = conllu_sentences[0].get_conllu_text(
            include_morphological_tags=True
        )
        self.assertEqual(self.expected_text_w_morph, f"{expected_sentences}\n")

    @pytest.mark.mark10
    @pytest.mark.stage_3_6_advanced_morphological_processing
    @pytest.mark.lab_6_pipeline
    def test_processing_without_morph_tags(self):
        """
        Test advanced processing without morphological tags
        """
        conllu_sentences = self.pipeline._process(self.raw_text)
        expected_sentences = conllu_sentences[0].get_conllu_text(
            include_morphological_tags=False
        )
        self.assertEqual(self.expected_text_wo_morph, f"{expected_sentences}\n")

    def tearDown(self) -> None:
        shutil.rmtree(TEST_PATH)
