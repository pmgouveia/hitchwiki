#!/bin/bash

# Export Hitchwiki pages related to SemanticMediaWiki (forms, templates etc)

SCRIPTSDIR=/var/www/scripts
PAGESDIR=$SCRIPTSDIR/pages
WIKIDIR=/var/www/public/wiki

cd $WIKIDIR

echo "Exporting Semantic content..."

if [ ! -f $PAGESDIR/_pagelist.txt ]; then
  echo "ERROR: $PAGESDIR/pagelist.txt does not exist! Aborting."
  exit 1
fi

# Loop them trough and import to mediawiki using https://www.mediawiki.org/wiki/Manual:Edit.php
#
# Option/Parameter    Description
# -u <user>	          Username
# -s <summary>	      Edit summary
# -m	                Minor edit
# -b	                Bot (hidden) edit
# -a	                Enable autosummary
# --no-rc	            Do not show the change in recent changes
#
# Load page names into array



# Return lines from the file into $MAPFILE array
source $SCRIPTSDIR/vendor/filelines2array.sh
fileLines2Array $PAGESDIR/_pagelist.txt

# Loop array trough
let i=0
for l in "${MAPFILE[@]}"
do

  PAGE=${MAPFILE[$i]}

  echo "Exporting '$PAGE'..."

  if [ -z "${PAGE}" ]; then
    echo "-> ERROR: Filename empty!"
    continue
  fi

  php maintenance/getText.php "$PAGE" >"$PAGESDIR/$PAGE"

  let i++
done




echo ""
echo "All done!"
echo ""