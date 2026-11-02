import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

import agreement  # noqa: E402
from lib import key, load, reading  # noqa: E402


class TestData(unittest.TestCase):
    def test_reading_covers_every_number_word(self):
        words = [v for p, k, v in load() if k == 'c']
        self.assertEqual(len(words), len(reading()))

    def test_key_covers_every_sign(self):
        K = key()
        signs = {s for p, k, v in load() if k == 'c' for s in v}
        self.assertEqual(signs - set(K), set())

    def test_known_words(self):
        K = key()
        self.assertEqual(''.join(K[s] for s in ['99', '89', '65', '51', '54', '70', '37', '90']), 'bvchanan')

    def test_agreement_thresholds(self):
        self.assertGreaterEqual(agreement.main('sonnet'), 90)
        self.assertGreaterEqual(agreement.main('codex'), 90)
        self.assertGreaterEqual(agreement.main('codex', 'tr1_before_corrections.txt'), 90)


if __name__ == '__main__':
    unittest.main()
