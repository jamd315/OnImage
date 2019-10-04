from unittest import TestCase

import numpy as np
from on_image.HashingArray import HashingArray


class TestHashingArray(TestCase):
    def setUp(self) -> None:
        self.sample_np_array = np.zeros((100, 100))
        self.sample_hashing_array = HashingArray(self.sample_np_array)

    def test_hash(self):
        self.assertEqual(hash(self.sample_hashing_array), 1608203990122525651)

    def test_eq(self):
        self.assertTrue(np.all(self.sample_hashing_array == self.sample_np_array))
        self.assertFalse(np.all(self.sample_hashing_array == np.ones((100, 100))))
        self.assertFalse(np.all(self.sample_hashing_array == HashingArray(self.sample_np_array, filename="something")))

    def test_numpy_function(self):
        new_arr = np.reshape(self.sample_hashing_array, (1, 100 * 100))
        self.assertTrue(np.all(new_arr == np.zeros((1, 100*100))))
