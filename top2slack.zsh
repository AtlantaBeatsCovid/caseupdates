#!/bin/zsh
# update
python ./parse

# post
python ./post_top_numbers.py "$1"
