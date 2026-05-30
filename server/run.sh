#!/bin/bash
set -e

# Resolve the home directory of the user who invoked sudo
REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)

echo "Loading bluetooth kernel module..."
modprobe bluetooth
modprobe bluetooth_6lowpan 2>/dev/null || true

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

echo "Verifying socket.AF_BLUETOOTH is available..."
"$REAL_HOME/.local/bin/uv" run python -c "
import socket
val = socket.AF_BLUETOOTH
print(f'  socket.AF_BLUETOOTH = {val} (OK)')
"

echo "Starting pkmn server..."
cd "$(dirname "$(realpath "$0")")"
exec "$REAL_HOME/.local/bin/uv" run uvicorn main:app --host 0.0.0.0 --port 8000
