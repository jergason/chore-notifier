# Chore notifier sends a list of chore assignments each day
from datetime import datetime
import random
import os

from croniter import croniter
import twilio.rest

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_FROM = '+13852627167'
TWILIO_TO_NUMBERS = os.environ['TWILIO_TO_NUMBERS'].split(",")


class Chore:
    def __init__(self, name, cron, kids=False):
        if not croniter.is_valid(cron):
            raise ValueError(
                "cron was not valid cron sytax. Should be in min hour day" +
                " month day_of_week, instead was {}".format(cron)
            )
        self.name = name
        self.cron = cron
        self.kids = kids

    def should_run(self, date):
        morning = datetime(date.year, date.month, date.day)
        cron = croniter(self.cron, morning, False)
        next = cron.get_next(datetime)
        # We only care about year, month and day, strip the rest off
        return (datetime(next.year, next.month, next.day) ==
                datetime(date.year, date.month, date.day))


class Person():
    def __init__(self, name,  is_kid=False):
        self.name = name
        self.is_kid = is_kid


# TODO: can't parse dates like "every other saturday"
chores = [
    # min hour day month day_of_week

    # Daily
    Chore("Empty litter box", "0 20 * * 1,3,5"),
    Chore("Do dishes", "0 20 * * *"),
    Chore("Wipe counters", "0 20 * * *"),
    Chore("Sweep", "0 20 * * *"),
    Chore("Laundry?", "0 20 * * 1,3,5"),

    # Weekly
    Chore("Vacuum living room", "0 9 * * 6"),
    Chore("Vacuum downstairs", "0 9 * * 6"),
    Chore("Vacuum Annabelle's room", "0 9 * * 6"),
    Chore("Vacuum parent's room", "0 9 * * 6"),
    Chore("Vacuum Jamison's room", "0 9 * * 6"),
    Chore("Empty trash cans", "0 9 * * 6"),
    Chore("Mop kitchen", "0 9 * * 6"),
    Chore("Clean master bathroom", "0 9 * * 6"),
    Chore("Clean hallway bathroom", "0 9 * * 6"),

    # Monthly
    Chore("Wash walls upstairs", "0 9 1 1,7 *"),
    Chore("Wash walls downstairs", "0 9 1 1,7 *"),
    Chore("Wash windows", "0 9 1 3,9 *"),
]

people = [
    Person("Elizabeth"),
    Person("Jamison"),
    # Person("Annabelle", True),
]


def jobs_for_day(date):
    return [chore for chore in chores if chore.should_run(date)]


def assign_chores(chores, people):
    assignments = {p.name: [] for p in people}
    for c in chores:
        person = random.choice(people)
        assignments[person.name].append(c.name)

    return assignments


def generate_report(assignments, date):
    report = "Chore List For {}\n\n".format(date.strftime("%a, %b %d, %Y"))
    for name, chores in assignments.items():
        if len(chores) == 0:
            continue
        report += "=={}==\n{}\n\n".format(
            name, "\n".join(["- {}".format(chore) for chore in chores]))
    return report.strip()


def send_text(report, numbers):
    client = twilio.rest.Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # print(report)
    for number in numbers:
        message = client.messages.create(
            from_=TWILIO_FROM,
            body=report,
            to=number
        )
        print("Sent message! {}".format(message))


def run(date):
    jobs = [chore for chore in chores if chore.should_run(date)]
    assignments = assign_chores(jobs, people)
    report = generate_report(assignments, date)
    send_text(report, TWILIO_TO_NUMBERS)


def do_chore_list(event, context):
    run(datetime.now())


if __name__ == '__main__':
    run(datetime.now())
