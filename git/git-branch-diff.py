#!/usr/bin/python

import subprocess
import argparse

DELIMITER = "|--|"

def get_commit_dict(branch_name):
    ignore = subprocess.check_output(["git", "checkout", branch_name])
    commits = subprocess.check_output(["git", "log", "--no-merges", "--pretty=format:\"%H|--|%<(15,trunc)%an|--|%<(10,trunc)%ar|--|%s\""])
    m = {}
    for commit in commits.split("\n"):
        tokens = commit.split(DELIMITER)
        m[tokens[3]] = commit.replace(DELIMITER, "  ")
    return m

parser = argparse.ArgumentParser(description="Diffs commits of two branches based on commit description.")
parser.add_argument('--old-branch', dest='old_branch', type=str, help='name of the older git branch', required=True)
parser.add_argument('--new-branch', dest='new_branch', type=str, help='name of the newer git branch', required=True)

args = parser.parse_args()
old_branch = args.old_branch
new_branch = args.new_branch

old_commits = get_commit_dict(old_branch)
new_commits = get_commit_dict(new_branch)

for old_commit in old_commits:
    if old_commit not in new_commits:
        print old_commits[old_commit]
