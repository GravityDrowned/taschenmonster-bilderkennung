#!/bin/bash
set -e

# Resolve the home directory of the user who invoked sudo,
# so the doctr model cache is shared between root and normal user runs.
REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)
export DOCTR_CACHE_DIR="$REAL_HOME/.cache/doctr"

echo "Using doctr cache at: $DOCTR_CACHE_DIR"

echo "Preparing BlueZ for nxbt..."
mkdir -p /run/systemd/system/bluetooth.service.d
cat > /run/systemd/system/bluetooth.service.d/nxbt.conf << 'SERVICEEOF'
[Service]
ExecStart=
ExecStart=/usr/sbin/bluetoothd --compat --noplugin=*
SERVICEEOF
systemctl daemon-reload
systemctl restart bluetooth

echo "Waiting for BlueZ to stabilize..."
sleep 5

echo "Starting pkmn..."
cd "$(dirname "$(realpath "$0")")"
exec "$REAL_HOME/.local/bin/uv" run python main.py
