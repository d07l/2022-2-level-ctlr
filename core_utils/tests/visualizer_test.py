"""
Tests for Visualizer
"""
import shutil
import unittest

import pytest

try:
    from PIL import Image, ImageChops
except ImportError:
    print('No libraries installed. Failed to import.')

from config.test_params import CORE_UTILS_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article.article import Article
from core_utils.article.io import from_meta
from core_utils.visualizer import visualize


class VisualizeTest(unittest.TestCase):
    """
    Class for testing Visualize implementation
    """

    # pylint: disable=assignment-from-no-return
    def setUp(self) -> None:
        TEST_PATH.mkdir(exist_ok=True)
        self.path_to_ref_image = CORE_UTILS_TEST_FILES_FOLDER / 'reference_image.png'
        self.path_to_save = TEST_PATH / '0_image.png'

        path_to_meta = CORE_UTILS_TEST_FILES_FOLDER / '1_meta.json'
        self.article = from_meta(path_to_meta)

        visualize(self.article, self.path_to_save)

    @pytest.mark.core_utils
    def test_article_param_is_article(self):
        """
        Ensure that article param is Article instance
        """
        self.assertIsInstance(self.article, Article)

    @pytest.mark.core_utils
    def test_pos_freq_param_is_dict(self):
        """
        Ensure that pos_frequency param is dict
        """
        self.assertIsInstance(self.article.get_pos_freq(), dict)

    @pytest.mark.core_utils
    def test_statistics_param_len_not_null(self):
        """
        Ensure that length of pos_frequency param is not null
        """
        error_msg = "POS frequency dict is empty"
        self.assertIsNot(len(self.article.get_pos_freq()), 0, error_msg)

    @pytest.mark.core_utils
    def test_image_is_correct(self):
        """
        Ensure that function visualize returns the correct image
        """
        error_msg = "Image is not correct"
        reference_image = Image.open(self.path_to_ref_image)
        test_image = Image.open(self.path_to_save)
        difference = ImageChops.difference(reference_image, test_image).getbbox()
        self.assertIsInstance(difference, type(None), error_msg)

    @pytest.mark.core_utils
    def test_images_are_generated(self):
        """
        Ensure that images are generated
        """
        error_msg = "Visualizer does not create an image"
        self.assertTrue(self.path_to_save.is_file(), error_msg)

    def tearDown(self) -> None:
        shutil.rmtree(TEST_PATH)
