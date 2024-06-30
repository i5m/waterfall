import unittest
from utils.funcs import *


class TestCatchUpFormula(unittest.TestCase):

    def test_catch_up_calculation(self):
        ci = 500
        PR = 0.1
        cu = 600
        expected_result = ci * PR / (cu - ci)
        result = catch_up_formula(ci, PR, cu)
        self.assertAlmostEqual(result, expected_result, places=2)


class TestCleanCurrency(unittest.TestCase):

    def test_clean_string_currency(self):
        cleaned_value = clean_currency("$1,234.56")
        self.assertAlmostEqual(cleaned_value, 1234.56, places=2)

    def test_clean_float(self):
        original_value = 1234.56
        cleaned_value = clean_currency(original_value)
        self.assertEqual(cleaned_value, original_value)


class TestDateDifference(unittest.TestCase):

    def test_positive_difference(self):
        date1 = datetime(2023, 5, 20)
        date2 = datetime(2023, 6, 15)
        difference = diff_dates(date1, date2)
        self.assertEqual(difference, 26)

    def test_negative_difference(self):
        date1 = datetime(2023, 6, 15)
        date2 = datetime(2023, 5, 20)
        difference = diff_dates(date1, date2)
        self.assertEqual(difference, 26)


class TestDataframeLoading(unittest.TestCase):

    def test_valid_csv_loading(self):
        path = "./data/example_commitments.csv"
        df = load_dataframe(path)
        self.assertIsInstance(df, pd.DataFrame)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            load_dataframe("nonexistent.csv")


class TestNumToCurrency(unittest.TestCase):

    def test_usd_currency(self):
        formatted_value = num_2_currency("$", 1234.56)
        self.assertEqual(formatted_value, "$1234.56")

    def test_eur_currency(self):
        formatted_value = num_2_currency("€", 1234.56)
        self.assertEqual(formatted_value, "€1234.56")


class TestPreferredReturnFormula(unittest.TestCase):

    def test_preferred_return_calculation(self):
        C = 1000
        R = 0.05
        d = 365
        expected_result = C * ((1 + R) ** (d / 365))
        result = preferred_return_formula(C, R, d)
        self.assertAlmostEqual(result, expected_result, places=2)


class TestStringToDateConversion(unittest.TestCase):

    def test_valid_date_conversion(self):
        date_str = "05/20/2023"
        expected_date = datetime(2023, 5, 20)
        converted_date = str_2_date(date_str)
        self.assertEqual(converted_date, expected_date)

    def test_invalid_date_conversion(self):
        with self.assertRaises(ValueError):
            str_2_date("31/02/2023")


if __name__ == "__main__":
    unittest.main()

