import os
from unittest import TestCase

from on_image import resolve_image, _make_sample_image, HashingArray


class TestResolve_image(TestCase):
    def setUp(self) -> None:
        _make_sample_image(1)

    def tearDown(self) -> None:
        os.remove("1.png")

    def test_from_HashingArray(self):
        ha = HashingArray("1.png")
        self.assertEqual(ha, resolve_image(ha))
