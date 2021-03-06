#!/bin/bash

#
# Install bot's dependencies
#

if [ ! -f Vagrantfile ]; then # an arbirtrary file that appears only once in the whole repository tree
    echo "ERROR: Bad working directory ($(pwd))."
    echo "Scripts have to be run from the root directory of the hitchwiki repository."
    echo "Aborting."
    exit 1
fi

source "scripts/_path_resolve.sh"
source "$SCRIPTDIR/_settings.sh"

WIKIBOTDIR="$SCRIPTDIR/bot"

sudo apt-get install python-pip python-dev libmysqlclient-dev
sudo pip install MySQL-python requests httplib2 ftfy

cd "$WIKIBOTDIR"
if cd ".cache"; then
    git stash # preserve fresh cache entries
    git pull
    git stash pop
else
    git clone https://github.com/hitchwiki/hitchwiki-migrate-cache.git .cache
fi

cd "$WIKIBOTDIR"
if cd "pywikibot-core"; then
    git pull
else
    git clone https://github.com/wikimedia/pywikibot-core.git pywikibot-core
fi
cd "$WIKIBOTDIR/pywikibot-core"
git submodule update --init

cd "$WIKIBOTDIR" # pywikibot's requirement
chown $USER:$USER "user-config.py"
chmod ga-rx "user-config.py"
