#!/usr/bin/env bash
# Link the integration into the Home Assistant devcontainer's config directory.
#
# Requires the devcontainer to bind mount this repository at
# /workspaces/croma-infrared-ha, so the symlink resolves inside the container. Edits on
# the host are then live; Home Assistant still needs a restart to pick up
# changed Python.
set -euo pipefail

DEST="${HA_CORE:-$HOME/projects/ha-core}/config/custom_components"

mkdir -p "$DEST"
rm -rf "${DEST:?}/croma_infrared"
ln -s /workspaces/croma-infrared-ha/custom_components/croma_infrared "$DEST/croma_infrared"
echo "linked $DEST/croma_infrared -> /workspaces/croma-infrared-ha/custom_components/croma_infrared"
