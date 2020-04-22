#!/bin/zsh
# update
~/anaconda3/envs/covid/bin/python ./parse.py

# post
~/anaconda3/envs/covid/bin/python ./post_top_numbers.py "$1"

