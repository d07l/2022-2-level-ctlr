"""
Tests for Article
"""
import datetime
import json
import shutil
import unittest
from pathlib import Path

import pytest

from config.test_params import (CORE_UTILS_TEST_FILES_FOLDER, PROJECT_ROOT,
                                TEST_PATH)
from core_utils.article import article
from core_utils.article.article import (Article, ArtifactType, date_from_meta,
                                        get_article_id_from_filepath,
                                        split_by_sentence)
from core_utils.article.io import (from_meta, from_raw, to_cleaned, to_conllu,
                                   to_meta, to_raw)
from core_utils.article.ud import (TagConverter,
                                   extract_sentences_from_raw_conllu)
from core_utils.tests.utils import universal_setup


class ArticleSupplementalTest(unittest.TestCase):
    """
    Class for testing supplemental functions in article.py
    """

    def setUp(self) -> None:
        article.ASSETS_PATH = TEST_PATH
        universal_setup()
        self.text = "Мама красиво мыла раму. Мама красиво мыла раму... " \
                    "Мама красиво мыла раму! Мама красиво мыла раму!!! " \
                    "Мама красиво мыла раму? Мама красиво мыла раму?! " \
                    "Мама мыла раму... красиво. Мама сказала: \"Помой раму!\""

    @pytest.mark.core_utils
    def test_date_from_meta_ideal(self):
        """
        Ideal date_from_meta scenario
        """
        date_time = '2022-11-06 16:30:00'
        expected = datetime.datetime(2022, 11, 6, 16, 30)
        actual = date_from_meta(date_time)
        self.assertEqual(expected, actual)

    @pytest.mark.core_utils
    def test_get_article_id_return_int(self):
        """
        Ensure that get_article_id_from_filepath() function
        returns article id
        """
        for file in TEST_PATH.iterdir():
            self.assertIsInstance(get_article_id_from_filepath(file), int)

    @pytest.mark.core_utils
    def test_split_by_sentence_return_list(self):
        """
        Ensure that split_by_sentence() function returns a list
        """
        self.assertIsInstance(split_by_sentence(self.text), list)

    @pytest.mark.core_utils
    def test_split_by_sentence_return_separated_sentences(self):
        """
        Ensure that split_by_sentence() function
        returns correctly separated sentences
        """
        sentences = ["Мама красиво мыла раму.", "Мама красиво мыла раму...",
                     "Мама красиво мыла раму!", "Мама красиво мыла раму!!!",
                     "Мама красиво мыла раму?", "Мама красиво мыла раму?!",
                     "Мама мыла раму... красиво.", "Мама сказала: \"Помой раму!\""]

        error_msg = "Function doesn't return correctly separated sentences"
        self.assertEqual(split_by_sentence(self.text), sentences, error_msg)

    def tearDown(self) -> None:
        shutil.rmtree(TEST_PATH)


class ArticleTest(unittest.TestCase):
    """
    Class for testing Article implementation
    """

    def setUp(self) -> None:
        article.ASSETS_PATH = TEST_PATH
        universal_setup()
        self.article = Article(url='test', article_id=1)

    @pytest.mark.core_utils
    def test_article_instantiation(self):
        """
        Ensure that Article instance is instantiated correctly
        """
        attrs = ['url', 'title', 'date', 'author', 'topics', 'pos_frequencies', '_conllu_sentences']
        error_msg = f"Article instance must possess the following arguments: {', '.join(attrs)}"

        self.assertTrue(all((
            hasattr(self.article, attrs[0]),
            hasattr(self.article, attrs[1]),
            hasattr(self.article, attrs[2]),
            hasattr(self.article, attrs[3]),
            hasattr(self.article, attrs[4]),
            hasattr(self.article, attrs[5]),
            hasattr(self.article, attrs[6]))), error_msg)

    @pytest.mark.core_utils
    def test_article_instances_type(self):
        """
        Ensure that Article constructor is filled with correct instances types
        """
        self.article = from_meta(self.article.get_meta_file_path(), self.article)

        error_msg = 'Check Article constructor: field "url"' \
                    'is supposed to be a string or None'
        self.assertIsInstance(self.article.url, (str, type(None)), error_msg)

        error_msg = 'Check Article constructor: field "title"' \
                    'is supposed to be a string'
        self.assertIsInstance(self.article.title, str, error_msg)

        error_msg = 'Check Article constructor: field "author"' \
                    'is supposed to be a list'
        self.assertIsInstance(self.article.author, list, error_msg)

        error_msg = 'Check Article constructor: field "topics"' \
                    'is supposed to be a list'
        self.assertIsInstance(self.article.topics, list, error_msg)

        error_msg = 'Check Article constructor: field "pos_frequencies"' \
                    'is supposed to be a dict'
        self.assertIsInstance(self.article.pos_frequencies, dict, error_msg)

        error_msg = 'Check Article constructor: field "_conllu_sentences"' \
                    'is supposed to be a list'
        self.assertIsInstance(self.article.get_conllu_sentences(), list, error_msg)

    @pytest.mark.core_utils
    def test_article_get_raw_text_return_str(self):
        """
        Ensure that Article.get_raw_text() method returns a string
        """
        self.assertIsInstance(self.article.get_raw_text(), str)

    @pytest.mark.core_utils
    def test_article_get_conllu_text_return_str(self):
        """
        Ensure that Article.get_conllu_text() method returns a string
        """
        self.assertIsInstance(self.article.get_conllu_text(include_morphological_tags=False), str)

    @pytest.mark.core_utils
    def test_article_sets_conllu_sentences(self):
        """
        Ensure that Article sets the conllu_sentences_attribute
        and returns the sentences from ConlluArticle
        """
        test_sentence = "мама красиво мыла раму"
        self.article.set_conllu_sentences(test_sentence)
        self.assertEqual(test_sentence, self.article.get_conllu_sentences())

    @pytest.mark.core_utils
    def test_article_get_cleaned_text_return_str(self):
        """
        Ensure that Article.get_cleaned_text() method returns a string
        """
        self.assertIsInstance(self.article.get_cleaned_text(), str)

    @pytest.mark.core_utils
    def test_raw_text_file_is_not_empty(self):
        """
        Ensure that a file with raw text is not empty
        """
        error_msg = "File for article raw text is empty"
        self.assertIsNot(self.article.get_raw_text_path().stat().st_size, 0, error_msg)

    @pytest.mark.core_utils
    def test_meta_file_is_not_empty(self):
        """
        Ensure that a metafile is not empty
        """
        error_msg = "File for article meta info is empty"
        self.assertIsNot(self.article.get_meta_file_path().stat().st_size, 0, error_msg)

    @pytest.mark.core_utils
    def test_article_get_file_path(self):
        """
        Ensure that Article.get_file_path() method gets the correct path
        """
        kind = ArtifactType.MORPHOLOGICAL_CONLLU
        self.assertTrue(isinstance(self.article.get_file_path(kind), Path))

    @pytest.mark.core_utils
    def test_article_get_file_path_raise_error(self):
        """
        Ensure that Article.get_file_path() method raises ValueError
        if kind param is not in accepted kinds
        """
        kind = 'some text'
        with self.assertRaises(AttributeError):
            self.article.get_file_path(kind)

    # pylint: disable=protected-access
    @pytest.mark.core_utils
    def test_article_sets_pos_info(self):
        """
        Ensure that Article adds POS information in metafile
        """
        test_statistics = {'test': 0, 'test1': 1}
        self.article.set_pos_info(test_statistics)

        self.assertEqual(test_statistics, self.article.get_pos_freq())

    @pytest.mark.core_utils
    def test_article_saves_meta_file(self):
        """
        Ensure that Article saves metafile
        """
        self.article = from_meta(self.article.get_meta_file_path(), self.article)
        to_meta(self.article)
        self.assertTrue(self.article.get_meta_file_path().is_file())

        with open(self.article.get_meta_file_path(), encoding='utf-8') as file:
            meta_file = json.load(file)

        self.article = from_meta(self.article.get_meta_file_path(), self.article)
        self.assertEqual(meta_file, self.article.get_meta())

    def tearDown(self) -> None:
        shutil.rmtree(TEST_PATH)


class IOTest(unittest.TestCase):
    """
    Class for testing I/O operations for Article
    """

    def setUp(self) -> None:
        article.ASSETS_PATH = TEST_PATH
        universal_setup()
        self.article = Article(url='test', article_id=1)

    @pytest.mark.core_utils
    def test_raw_text_file_is_created(self):
        """
        Ensure that a file with raw text is created
        """
        error_msg = "File for article raw text is not created"
        to_raw(self.article)
        self.assertTrue(self.article.get_raw_text_path().is_file(), error_msg)

    @pytest.mark.core_utils
    def test_from_raw_return_article(self):
        """
        Ensure that from_raw() function returns Article object
        """
        path = TEST_PATH / '1_raw.txt'
        self.assertIsInstance(from_raw(path), Article)

    @pytest.mark.core_utils
    def test_cleaned_file_is_created(self):
        """
        Ensure that to_cleaned() function creates a file with cleaned text
        """
        error_msg = "File for article cleaned text is not created"
        to_cleaned(self.article)
        self.assertTrue(self.article.get_file_path(ArtifactType.CLEANED).is_file(), error_msg)

    @pytest.mark.core_utils
    def test_meta_file_is_created(self):
        """
        Ensure that metafile is created
        """
        error_msg = "File for article meta info is not created"
        to_meta(self.article)
        self.assertTrue(self.article.get_meta_file_path().is_file(), error_msg)

    @pytest.mark.core_utils
    def test_full_conllu_file_is_created(self):
        """
        Ensure that to_conllu() function saves pymorphy conllu info
        """
        error_msg = "File for article morphological conllu info is not created"
        to_conllu(self.article, include_morphological_tags=True, include_pymorphy_tags=True)
        self.assertTrue(self.article.get_file_path(ArtifactType.FULL_CONLLU).is_file(),
                        error_msg)

    @pytest.mark.core_utils
    def test_conllu_file_is_created(self):
        """
        Ensure that to_conllu() function saves morphological conllu info
        """
        error_msg = "File for article morphological conllu info is not created"
        to_conllu(self.article, include_morphological_tags=True)
        self.assertTrue(self.article.get_file_path(ArtifactType.MORPHOLOGICAL_CONLLU).is_file(),
                        error_msg)

    @pytest.mark.core_utils
    def test_pos_conllu_file_is_created(self):
        """
        Ensure that to_conllu() function saves POS-only conllu info
        """
        error_msg = "File for article full conllu info is not created"
        to_conllu(self.article, include_morphological_tags=False)
        self.assertTrue(self.article.get_file_path(ArtifactType.POS_CONLLU).is_file(), error_msg)

    def tearDown(self) -> None:
        shutil.rmtree(TEST_PATH)


class UDTest(unittest.TestCase):
    """
    Class for testing parsers for CONLL-U
    """

    def setUp(self) -> None:
        self.path = CORE_UTILS_TEST_FILES_FOLDER / "reference_score_six_test.conllu"
        self.path_to_reference = CORE_UTILS_TEST_FILES_FOLDER / "reference_output_article_test.json"
        self.tag_mapping_path = (
                PROJECT_ROOT / "lab_6_pipeline" / "data" / "mystem_tags_mapping.json"
        )
        self.converter = TagConverter(self.tag_mapping_path)

    @pytest.mark.core_utils
    def test_extract_sentences_from_raw_conllu_return_list(self):
        """
        Ensure that extract_sentences_from_raw_conllu() function returns list
        """
        with open(file=self.path,
                  mode='r',
                  encoding='utf-8') as conllu_file:
            self.assertIsInstance(extract_sentences_from_raw_conllu(conllu_file.read()), list)

    @pytest.mark.core_utils
    def test_extracted_sentences_stores_correctly(self):
        """
        Ensure that extract_sentences_from_raw_conllu() function
        extracts and stores sentences correctly
        """
        error_msg = "Function stores sentences from the CONLL-U-formatted article incorrectly"

        expected = []
        with open(self.path_to_reference, "r", encoding="utf-8") as f:
            extracted_sentences_from_conllu = json.load(f)
        expected.append(extracted_sentences_from_conllu)

        with open(file=self.path,
                  mode='r',
                  encoding='utf-8') as conllu_file:
            actual = extract_sentences_from_raw_conllu(conllu_file.read())

        self.assertEqual(expected, actual, error_msg)

    @pytest.mark.core_utils
    def test_tag_converter_instantiation(self):
        """
        Ensure that TagConverter instance is instantiated correctly
        """
        attrs = ['pos', 'case', 'number', 'gender', 'animacy', 'tense', 'tags']
        error_msg = f"Article instance must possess the following arguments: {', '.join(attrs)}"

        self.assertTrue(all((
            hasattr(self.converter, attrs[0]),
            hasattr(self.converter, attrs[1]),
            hasattr(self.converter, attrs[2]),
            hasattr(self.converter, attrs[3]),
            hasattr(self.converter, attrs[4]),
            hasattr(self.converter, attrs[5]),
            hasattr(self.converter, attrs[6]))), error_msg)

    @pytest.mark.core_utils
    def test_convert_morphological_tags_raise_error(self):
        """
        Ensure that TagConverter.convert_morphological_tags() method raises NotImplementedError
        """
        tag = "вин"
        with self.assertRaises(NotImplementedError):
            self.converter.convert_morphological_tags(tag)

    @pytest.mark.core_utils
    def test_convert_pos_raise_error(self):
        """
        Ensure that TagConverter.convert_pos() method raises NotImplementedError
        """
        pos_tag = "S"
        with self.assertRaises(NotImplementedError):
            self.converter.convert_pos(pos_tag)
