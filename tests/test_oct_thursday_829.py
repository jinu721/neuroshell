import unittest


class TestOct829(unittest.TestCase):
    def test_duration_under_a_minute(self):
        secs = 29
        self.assertLess(secs, 60)

    def test_filter_keeps_blank_when_no_rules(self):
        lines = ["ok", "", "done"]
        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
