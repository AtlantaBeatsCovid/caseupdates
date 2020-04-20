#!/bin/zsh
# update
python ./parse.py

# post
python ./post_top_numbers.py "$1"
