import unittest
import pandas as pd
import os
import task1

CWD = os.getcwd()
task1_get_data_actual = pd.read_csv(os.path.join(CWD, "gbp_test_data.csv"))
task1_get_raw_data_actual = pd.read_csv(os.path.join(CWD, "gbp_test_raw_data.csv"))
task1_get_exchange_rate_data_actual = pd.read_csv(
    os.path.join(CWD, "gbp_test_exchange_rate.csv")
)
task1_get_exchange_rate_data_NOK_actual = pd.read_csv(
    os.path.join(CWD, "nok_test_exchange_rate.csv")
)


class TestTask1(unittest.TestCase):
    def test_final_data(self):
        # Test final output data
        pd.testing.assert_frame_equal(
            task1_get_data_actual,
            task1.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP"),
        )
        pd.testing.assert_frame_equal(
            task1_get_raw_data_actual,
            task1.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"),
        )

    def test_exchange_rate(self):
        # Test Exchange rate data
        task1_get_ex_rate_actual = pd.read_csv(
            os.path.join(CWD, "gbp_test_exchange_rate.csv")
        )

        task1_get_ex_rate = task1.get_exchange_rate("GBP")
        task1_get_ex_rate_nok = task1.get_exchange_rate("NOK")
        pd.testing.assert_frame_equal(task1_get_ex_rate_actual, task1_get_ex_rate)
        pd.testing.assert_frame_equal(
            task1_get_exchange_rate_data_NOK_actual, task1_get_ex_rate_nok
        )

    def test_raw_data(self):
        # Test raw data
        pd.testing.assert_frame_equal(
            task1_get_raw_data_actual,
            task1.get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"),
        )
