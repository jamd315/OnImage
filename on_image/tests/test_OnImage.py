import os
import threading
from unittest import TestCase

import on_image


class TestOnImage(TestCase):
    n_sample_images = 5

    def setUp(self) -> None:
        self.img_handler = on_image.OnImage()
        for i in range(self.n_sample_images):
            on_image._make_sample_image(i)

    def tearDown(self) -> None:
        for i in range(self.n_sample_images):
            os.remove(f"{i}.png")

    def test_on_image(self):
        resolved = [on_image.resolve_image(f"./{i}.png") for i in range(self.n_sample_images)]

        @self.img_handler.on_image(resolved[0])  # Standard expected use
        @self.img_handler.on_image(resolved[4])  # Multiple "and"s
        @self.img_handler.not_on_image(resolved[1])  # Partials
        @self.img_handler.or_on_image(resolved[2], resolved[3])  # The other partial
        def some_function():
            return "Yes"

        # Make sure the img_find_results dict was set up right
        for r in resolved:
            self.assertIn(r, self.img_handler.img_find_results)
            self.assertFalse(self.img_handler.img_find_results[r])

        # Make sure the function got a key
        self.assertIn(some_function, self.img_handler.func_match_types)

        # Then check that the values for the match types is all set up
        self.assertIn(resolved[0], self.img_handler.func_match_types[some_function]["and"])
        self.assertIn(resolved[4], self.img_handler.func_match_types[some_function]["and"])

        self.assertIn(resolved[1], self.img_handler.func_match_types[some_function]["not"])

        self.assertIn(resolved[2], self.img_handler.func_match_types[some_function]["or"][0])
        self.assertIn(resolved[3], self.img_handler.func_match_types[some_function]["or"][0])

        # Check the input validation
        with self.assertRaises(ValueError):
            @self.img_handler.on_image(resolved[0], resolved[1])
            def other_func():
                return "No"

        with self.assertRaises(ValueError):
            @self.img_handler.on_image(resolved[0], "garbage")
            def another_func():
                return "Maybe?"

        with self.assertRaises(ValueError):
            @self.img_handler.on_image()
            def the_last_func():
                return "Oui"

    def test_run_stop(self):
        self.img_handler.run(blocking=False)  # Not sure there's a practical way to test the blocking method so it's ignored for now
        self.assertTrue(self.img_handler._running)
        self.assertIsInstance(self.img_handler._thread, threading.Thread)
        self.assertTrue(self.img_handler._thread.isAlive())
        self.img_handler.stop()
        self.assertFalse(self.img_handler._running)
        self.assertFalse(self.img_handler._thread.isAlive())
