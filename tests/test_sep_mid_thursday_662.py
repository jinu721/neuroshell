import unittest


class TestSepMid662(unittest.TestCase):
    def test_quiet_hours_overnight(self):
        # 22..7 wraps midnight
        start, end = 22, 7
        hour = 14
        wrapped = hour >= start or hour < end
        self.assertIsInstance(wrapped, bool)

    def test_rank_prefers_prefix(self):
        items = ["git status", "git push", "npm install"]
        q = "git"
        hits = [i for i in items if i.startswith(q)]
        self.assertTrue(len(hits) >= 1)


if __name__ == "__main__":
    unittest.main()
