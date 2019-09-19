import unittest
from datetime import datetime, timedelta


import function


class TestChore(unittest.TestCase):
    # def test_invalid_cron_syntax(self):
    #     invalid = [
    #         "foo",
    #         "* * * * * * *",
    #         "",
    #     ]
    #     [self.assertRaises(ValueError, function.Chore, "wat", cron)
    #      for cron in invalid]

    # def test_valid_cron_syntax(self):
    #     # we should work w/ valid cron syntax
    #     crons = [
    #         "0 20 * * 1,3,5",
    #         "0 9 * * 6",
    #         "0 9 1 1,7 *",
    #     ]
    #     [function.Chore("wat", cron) for cron in crons]

    # def test_should_run(self):
    #     on_the_tenth = function.Chore("a", "0 10 10 * *")
    #     tenth = datetime(2019, 1, 10, 1, 1, 1)
    #     self.assertTrue(on_the_tenth.should_run(tenth))

    #     # jobs for the 11th shouldn't run on the 10th
    #     self.assertFalse(on_the_tenth.should_run(tenth + timedelta(days=1)))

    def test_stuff(self):
        jobs = function.jobs_for_day(datetime(2019, 1, 10, 1, 1, 1))
        self.assertGreater(
            len(jobs), 0, "There should be some chores every day, but got no chores?")
        print(jobs)


if __name__ == '__main__':
    unittest.main()
