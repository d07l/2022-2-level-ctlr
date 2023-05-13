"""
Tests for processing reference text
"""
import re
import shutil
import unittest
from string import punctuation

import pytest

from config.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from core_utils.article.ud import extract_sentences_from_raw_conllu
from lab_6_pipeline.pipeline import (CorpusManager,
                                     MorphologicalAnalysisPipeline)
from lab_6_pipeline.tests.utils import pipeline_test_files_setup

UD_TAGS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM',
           'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']


class ReferenceTextPreprocessTestSimplified(unittest.TestCase):
    """
    Tests for simplified preprocessing of reference text
    """

    @classmethod
    def setUpClass(cls) -> None:
        pipeline_test_files_setup(meta=True)
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = MorphologicalAnalysisPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        path = PIPE_TEST_FILES_FOLDER / 'reference_score_four_test.txt'
        with path.open('r', encoding='utf-8') as reference:
            self.reference = reference.read()
        path = TEST_PATH / "1_cleaned.txt"
        with path.open("r", encoding='utf-8') as processed:
            self.processed = processed.read()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_reference_preprocessed_are_equal(self):
        """
        Ensure equal number of tags in processed and reference texts
        """
        # check number of tokens sequences
        self.assertEqual(len(self.reference.split()),
                         len(self.processed.split()),
                         msg=f"""Number of tokens sequences in reference
        {self.reference} and processed {self.processed} texts is different""")

        # check tokenization
        self.assertEqual(self.reference.split(),
                         self.processed.split(),
                         msg="""Pipe does not tokenize admin text.
        Check how you tokenize""")

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_overall_format(self):
        """
        Ensure that there is no punctuation of uppercase in clean text
        """
        self.assertTrue(self.processed.islower(),
                        'Cleaned text must be lowercase')
        self.assertFalse((set(self.processed) & set(punctuation)),
                         'Cleaned text must not have any punctuation')

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEST_PATH)


class ReferenceTextPreprocessAdvancedTest(unittest.TestCase):
    """
    Tests for preprocessing of reference texts for 8 mark and higher
    """

    @classmethod
    def setUpClass(cls) -> None:
        pipeline_test_files_setup()
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = MorphologicalAnalysisPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        path = PIPE_TEST_FILES_FOLDER / 'reference_score_eight_test.conllu'
        with path.open('r', encoding='utf-8') as ref:
            self.conllu_reference = ref.read()
        self.ref_sentences = extract_sentences_from_raw_conllu(self.conllu_reference)
        path = TEST_PATH / '1_morphological_conllu.conllu'
        with path.open('r', encoding='utf-8') as proc:
            self.conllu_processed = proc.read()
        self.proc_sentences = extract_sentences_from_raw_conllu(self.conllu_processed)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_reference_preprocessed_are_equal(self):
        """
        Ensure that there are equal number of lines
        in reference and processed conllu files
        after medium level processing
        """
        # check number of token word<tag> sequences
        message = f"Number of lines in reference " \
                  f"{self.conllu_reference} and processed " \
                  f"{self.conllu_processed} texts is different"
        self.assertEqual(len(self.conllu_reference.split('\n')),
                         len(self.conllu_processed.split('\n')),
                         msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_tokens_are_formatted(self):
        """
        Ensure correct formatting of conllu sequences
        """
        msg = 'In conllu files, all tokens must be accompanied ' \
              'by a single set of tags in angle brackets'
        tokens = ['Красивая', 'мама', 'красиво', 'училась', 'в',
                  'ПДД', 'и', 'ЖКУ', 'по', 'адресу', 'Львовская', '10',
                  'лет', 'с', 'почтой', 'test', '.']

        formatted_lines_number = list(
            i for i in self.conllu_processed.split('\n') if i.split('\t')[0].isnumeric()
        )
        self.assertEqual(len(tokens),
                         len(formatted_lines_number), msg=msg)

        for token_id, token in enumerate(tokens):
            msg = f'In conllu files, all tokens must be in lines' \
                  f'{token} is not in {formatted_lines_number[token_id]} at the second place'
            self.assertEqual(token, formatted_lines_number[token_id].split('\t')[1], msg=msg)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_overall_format(self):
        """
        Ensure that overall formatting
        of conllu texts
        is appropriate
        """
        for id_sentence, proc_sentence in enumerate(self.proc_sentences):
            message = f"In {id_sentence} sentence--- " \
                      f"You have wrong number of sent_id---" \
                      f"You have {proc_sentence.get('position')}, " \
                      f"but you must have {self.ref_sentences[id_sentence].get('position')}"
            self.assertEqual(
                self.ref_sentences[id_sentence].get('position'),
                proc_sentence.get('position'),
                msg=message)

            message = f"In {id_sentence} sentence --- " \
                      f"You have wrong text in # text " \
                      f"You have {proc_sentence.get('text')}, " \
                      f"but you must have {self.ref_sentences[id_sentence].get('text')}"
            self.assertEqual(
                self.ref_sentences[id_sentence].get('text'),
                proc_sentence.get('text'),
                msg=message)

            message = f"In {id_sentence} sentence --- " \
                      f"You have wrong tokens "
            self.assertEqual(
                self.ref_sentences[id_sentence].get('tokens'),
                proc_sentence.get('tokens'),
                msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_ud_tag_format(self):
        """
        Ensure that UD tags are correct
        """
        # check TAGS after each sequence:
        tags_pattern = re.compile(r"\t([A-Z]+)\t")
        reference_tags = re.findall(tags_pattern, self.conllu_processed)
        processed_tags = re.findall(tags_pattern, self.conllu_reference)

        # check tag correctness.
        # Optional, but should be the same across each tagger,
        # as reference example is too simple
        for tag in processed_tags:
            message = f"Tag {tag} is an unknown UD " \
                      f"tag. Is it in required tags list?"
            self.assertTrue(tag in UD_TAGS, msg=message)
        message = f"UD tag sequence from reference text {reference_tags} " \
                  f"differs from processed text {processed_tags}"
        self.assertEqual(reference_tags, processed_tags, msg=message)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEST_PATH)


class ReferenceTextPreprocessBasicTest(unittest.TestCase):
    """
    Tests for preprocessing of reference texts for 6 marks
    """

    @classmethod
    def setUpClass(cls) -> None:
        pipeline_test_files_setup()
        article.ASSETS_PATH = TEST_PATH

        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = MorphologicalAnalysisPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        path = PIPE_TEST_FILES_FOLDER / 'reference_score_six_test.conllu'
        with path.open('r', encoding='utf-8') as ref:
            self.conllu_reference = ref.read()
        self.ref_sentences = extract_sentences_from_raw_conllu(self.conllu_reference)
        path = TEST_PATH / '1_pos_conllu.conllu'
        with path.open('r', encoding='utf-8') as proc:
            self.conllu_processed = proc.read()
        self.proc_sentences = extract_sentences_from_raw_conllu(self.conllu_processed)

    @pytest.mark.mark6
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_reference_preprocessed_are_equal(self):
        """
        Ensure that there are equal number of lines
        in reference and processed conllu files
        after medium level processing
        """
        # check number of token word<tag> sequences
        message = f"Number of lines in reference " \
                  f"{self.conllu_reference} and processed " \
                  f"{self.conllu_processed} texts is different"
        self.assertEqual(len(self.conllu_reference.split('\n')),
                         len(self.conllu_processed.split('\n')),
                         msg=message)

    @pytest.mark.mark6
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_tokens_are_formatted(self):
        """
        Ensure correct formatting of conllu sequences
        """
        msg = 'In conllu files, all tokens must be accompanied ' \
              'by a single set of tags in angle brackets'
        tokens = ['Красивая', 'мама', 'красиво', 'училась', 'в',
                  'ПДД', 'и', 'ЖКУ', 'по', 'адресу', 'Львовская', '10',
                  'лет', 'с', 'почтой', 'test', '.']

        formatted_lines_number = list(
            i for i in self.conllu_processed.split('\n') if i.split('\t')[0].isnumeric()
        )
        self.assertEqual(len(tokens),
                         len(formatted_lines_number), msg=msg)

        for token_id, token in enumerate(tokens):
            msg = f'In conllu files, all tokens must be in lines' \
                  f'{token} is not in {formatted_lines_number[token_id]} at the second place'
            self.assertEqual(token, formatted_lines_number[token_id].split('\t')[1], msg=msg)

    @pytest.mark.mark6
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_overall_format(self):
        """
        Ensure that overall formatting
        of conllu texts
        is appropriate
        """
        for id_sentence, proc_sentence in enumerate(self.proc_sentences):
            message = f"In {id_sentence} sentence--- " \
                      f"You have wrong number of sent_id---" \
                      f"You have {proc_sentence.get('position')}, " \
                      f"but you must have {self.ref_sentences[id_sentence].get('position')}"
            self.assertEqual(
                proc_sentence.get('position'),
                self.ref_sentences[id_sentence].get('position'),
                msg=message)

            message = f"In {id_sentence} sentence --- " \
                      f"You have wrong text in # text " \
                      f"You have {proc_sentence.get('text')}, " \
                      f"but you must have {self.ref_sentences[id_sentence].get('text')}"
            self.assertEqual(
                proc_sentence.get('text'),
                self.ref_sentences[id_sentence].get('text'),
                msg=message)

            message = f"In {id_sentence} sentence --- " \
                      f"You have wrong tokens "
            self.assertEqual(
                proc_sentence.get('tokens'),
                self.ref_sentences[id_sentence].get('tokens'),
                msg=message)

    @pytest.mark.mark6
    @pytest.mark.stage_3_4_admin_data_processing
    @pytest.mark.lab_6_pipeline
    def test_conllu_ud_tag_format(self):
        """
        Ensure that UD tags are correct
        """
        # check TAGS after each sequence:
        tags_pattern = re.compile(r"\t([A-Z]+)\t")
        reference_tags = re.findall(tags_pattern, self.conllu_processed)
        processed_tags = re.findall(tags_pattern, self.conllu_reference)

        # check tag correctness.
        # Optional, but should be the same across each tagger,
        # as reference example is too simple
        for tag in processed_tags:
            message = f"Tag {tag} is an unknown UD " \
                      f"tag. Is it in required tags list?"
            self.assertTrue(tag in UD_TAGS, msg=message)
        message = f"UD tag sequence from reference text {reference_tags} " \
                  f"differs from processed text {processed_tags}"
        self.assertEqual(reference_tags, processed_tags, msg=message)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(TEST_PATH)
