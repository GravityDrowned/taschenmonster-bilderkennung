#!/bin/bash
set -e
echo "Preparing BlueZ for nxbt..."
mkdir -p /run/systemd/system/bluetooth.service.d
cat > /run/systemd/system/bluetooth.service.d/nxbt.conf << EOF
[Service]
ExecStart=
ExecStart=/usr/libexec/bluetooth/bluetoothd --compat --noplugin=*
EOF
systemctl daemon-reload
systemctl restart bluetooth
echo "Waiting for BlueZ to stabilize..."
sleep 5
echo "Starting pkmn..."