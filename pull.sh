#!/bin/bash
cd /home/arya2705/vfly_dataentry
git config --global credential.helper 'store --file=/home/arya2705/vfly_dataentry/git_token.txt'
git pull origin develop
