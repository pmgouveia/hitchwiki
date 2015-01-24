#!/bin/bash

#
# Include path variables in any bash script
#
# Invoking script has to be in the same folder as this file in order for path
# resolution to work correctly
#
# Usage:
#   "source path_resolve.sh"
#

#
# Canonical paths to important directories
#
# Can be relied upon in all 3 scenarios:
# - run a script inside the Vagrant box;
# - run a script on the host OS of the Vagrant box;
# - run a script in a non-Vagrant setup, eg. production server.
#

ROOTDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
CONFDIR="$ROOTDIR/configs"
CONFPATH="$CONFDIR/mediawiki.php"
SCRIPTDIR="$ROOTDIR/scripts"
WIKIDIR="$ROOTDIR/public/wiki"

#
# Canonical paths to important directories inside the Vagrant box
#
# Useful for passing explicit paths from the host OS to a script inside Vagrant,
# for example:
#
#   source "path_resolve.sh"
#   vagrant ssh -c "bash \"$VAGRANT_SCRIPTDIR/export_pages.sh\""
#
# Serve no purpose when used in a non-Vagrant environment, eg. production server
#

VAGRANT_ROOTDIR="/var/www"
VAGRANT_CONFDIR="$VAGRANT_ROOTDIR/configs"
VAGRANT_CONFPATH="$VAGRANT_CONFDIR/mediawiki.php"
VAGRANT_SCRIPTDIR="$VAGRANT_ROOTDIR/scripts"
VAGRANT_WIKIDIR="$VAGRANT_ROOTDIR/public/wiki"
