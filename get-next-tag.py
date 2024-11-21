#!/bin/python3
# A script to determine the next tag for getsolus/solus-appstream-data.
# This behavior is likely fairly specific to this repository.

import subprocess

git_tags = subprocess.check_output(['git', '--no-pager', 'tag', '--sort=-creatordate']).split(b'\n')
latest_number = int(git_tags[0].strip(b'v'))
next_tag = f'v{latest_number + 1}'
print(next_tag)
