import os
import sys
import git
import glob

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

        locks.append({
            "name": lock_name ,
            "claimer": claimer,
            "date": claim_date,
        })

    for lock in sorted(locks, key=lambda lock: lock["date"]):
        print("{:>25} {:>35} {:>25}".format(lock["name"], lock["claimer"], lock["date"].strftime("%d %b %Y %H:%M:%S")))

