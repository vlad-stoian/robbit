import os
import re
import sys
import git
import glob
import textwrap
from datetime import datetime, timezone

DEBUG = False

def print_debug(what, message):
    if DEBUG:
        print("<debug = {}> -> {}".format(what, message))


if __name__ == "__main__":
    print_debug("hello_message", "Hello There!")

    script_path, locks_repo_path = sys.argv

    locks_repo = git.Repo(locks_repo_path)

    locks = []

    for filepath in glob.glob("{}/*-envs/claimed/*".format(locks_repo_path)):
        lock_name = os.path.basename(os.path.normpath(filepath))

        commits_touching_path = list(locks_repo.iter_commits(paths=filepath, max_count=1))

        if len(commits_touching_path) < 1:
            print("No commits for lock {}".format(lock_name))
            continue

        claim_date = commits_touching_path[0].committed_datetime
        committer_name = commits_touching_path[0].committer.name
        author_name = commits_touching_path[0].author.name

        claimer = "{} + {}".format(author_name, committer_name)

        if committer_name == author_name:
            claimer = author_name

        if claimer == "CI Pool Resource":
            claimer = commits_touching_path[0].message.split(' ')[0]

        pattern = re.compile(r'.*\/(?P<type>(.*))\-envs\/.*')
        match = pattern.search(filepath)

        timediff = datetime.now(timezone.utc) - claim_date

        locks.append({
            "name": lock_name ,
            "claimer": claimer,
            "date": claim_date,
            "ago": "{} days ago".format(timediff.days),
            "type": match.group('type'),
        })

    print('```')
    format_string = "{:>15} {:>10} {:>35} {:>22} {:>14}"
    print(format_string.format("OpsMan Env", "Type", "Claimed by", "Claimed on", "That means"))
    print("-" * 100)

    for lock in sorted(locks, key=lambda lock: lock["date"]):
        print(format_string.format(
            textwrap.shorten(lock["name"], width=25),
            textwrap.shorten(lock["type"], width=10),
            textwrap.shorten(lock["claimer"], width=35),
            textwrap.shorten(lock["date"].strftime("%d %b %Y %H:%M:%S"), width=22),
            textwrap.shorten(lock["ago"], width=14),
        ))

    print('```')

