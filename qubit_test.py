import unittest
from qubit import Qubit

# qubit_test.py
# Unit test for qubit.py
class QubitTest(unittest.TestCase):

    # Verifies init function.
    def test_init(self):
        """Test init function with (0,0)"""
        qubit_a = Qubit(0,0)
        self.assertEqual(qubit_a.value, 0)
        self.assertEqual(qubit_a.polarization, 0)
        """Test init function with (1,0)"""
        qubit_b = Qubit(1,0)
        self.assertEqual(qubit_b.value, 1)
        self.assertEqual(qubit_b.polarization, 0)
        """Test init function with (1,1)"""
        qubit_c = Qubit(1,1)
        self.assertEqual(qubit_c.value, 1)
        self.assertEqual(qubit_c.polarization, 1)


    # Verify init function exception for invalid value.
    def test_invalid_value_exception(self):
        """Test init function with (2,1) raises ValueError"""
        with self.assertRaises(ValueError):
            Qubit(2,1)


    # Verify init function exception for invalid polarization.
    def test_invalid_polarization_exception(self):
        """Test init function with (1,2) raises ValueError"""
        with self.assertRaises(ValueError):
            Qubit(1,2)


    # Verify set function when value and polarization is valid.
    def test_valid_set(self):
        """Test set(1,1) function changes (0,0) to (1,1)"""
        qubit = Qubit(0,0)
        qubit.set(1, 1)
        self.assertEqual(qubit.value, 1)
        self.assertEqual(qubit.polarization, 1)


    # Verify set function when value or polarization is invalid.
    def test_invalid_set(self):
        """Test function set(2,0) and set(1,-1) raises ValueError"""
        qubit = Qubit(0,0)
        with self.assertRaises(ValueError):
            qubit.set(2, 0)
        with self.assertRaises(ValueError):
            qubit.set(1, -1)


    # Verifies measurement function returns same value.
    #
    # If polarization == polarization
    # Then measurement <- value
    def test_match_polarization(self):
        """Test measure function(0) on (1,0) returns 1"""
        qubit = Qubit(1,0)
        measurement = qubit.measure(0)
        self.assertEqual(measurement, 1)


    # Verifies measurement function changes polarization.
    #
    # If polarization != polarization,
    # Then polarization should flip, i.e., !polarization,
    # And value may change to either [0,1]
    def test_no_match_polarization(self):
        """Test measure function(1) on (1,0) returns ([0,1], 1)"""
        qubit = Qubit(1,0)
        measured = qubit.measure(1)
        self.assertIn(measured, [0,1])
        self.assertEqual(qubit.polarization, 1)


# Entry point.
# Run with `python3 qubit_test.py -v` for verbose output.
if __name__ == '__main__':
    with open("logs/test_qubit.txt", "w") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.defaultTestLoader.discover('.', pattern='*_test.py')
        unittest.main(testRunner=runner, exit=False)
