# test_fibonacci.py

import unittest
from fibonacci import generate_fibonacci_sequence  # ✅ Import the function from `fibonacci.py`

class TestGenerateFibonacciSequence(unittest.TestCase):

    def test_generate_fibonacci_sequence_with_n_0(self):
        self.assertEqual(generate_fibonacci_sequence(0), [])

    def test_generate_fibonacci_sequence_with_n_1(self):
        self.assertEqual(generate_fibonacci_sequence(1), [0])

    def test_generate_fibonacci_sequence_with_n_2(self):
        self.assertEqual(generate_fibonacci_sequence(2), [0, 1])

    def test_generate_fibonacci_sequence_with_n_5(self):
        self.assertEqual(generate_fibonacci_sequence(5), [0, 1, 1, 2, 3])

    def test_generate_fibonacci_sequence_with_n_10(self):
        self.assertEqual(generate_fibonacci_sequence(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

if __name__ == '__main__':
    unittest.main()
