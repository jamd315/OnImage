import os
from unittest import TestCase

import cv2
from on_image import multi_img_find, _make_sample_image

class TestMulti_img_find(TestCase):
    # Mostly just test that the stuff runs and doesn't error, without any verification, since this is hard to set up a test.
    # TODO better testing, and also it's possible the screenshot could fail on another system
    def setUp(self) -> None:
        for i in range(3):
            _make_sample_image(i)

    def tearDown(self) -> None:
        for i in range(3):
            os.remove(f"{i}.png")

    def test_run(self):
        multi_img_find(*[f"{i}.png" for i in range(3)])
        multi_img_find(*[f"{i}.png" for i in range(3)], use_mp=True)
        multi_img_find(*[f"{i}.png" for i in range(3)], use_mp=False)
        multi_img_find(*[f"{i}.png" for i in range(3)], use_mp=True, core_count=1)
        multi_img_find(*[f"{i}.png" for i in range(3)], method=cv2.TM_CCORR_NORMED)
        multi_img_find(*[f"{i}.png" for i in range(3)], timeout=-1)
        with self.assertRaises(ValueError):
            multi_img_find(target="1.png")
        with self.assertRaises(ValueError):
            multi_img_find()
        self.assertTrue(True)
