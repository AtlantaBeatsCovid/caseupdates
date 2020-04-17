#!/bin/zsh
# assumes postToSlack.sh from https://github.com/sulhome/bash-slack is at ~

# update
./parse.zsh >> covid.log

# post
~/postToSlack.sh -t "$(echo $(date +%d.%m.%y-%H:%M:%S))" -b "Top Case Increases:"$'\n'"$(perl ./top_10.pl covid.log)" -c "caseupdates" -u "$1"
