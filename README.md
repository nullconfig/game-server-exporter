# Game Server Exporter
A prometheus exporter for game servers that support the A2S query protocol

Build the exporter
```bash
python -m build
```
Install the exporter globally
```bash
sudo pip install dist/game_server_exporter-0.0.1.tar.gz
```

Running the exporter as a systemd service
```
[Unit]
Description=Game Server Exproter
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
User=root
ExecStart=game-server-exporter --container steamcmd \
--address x.x.x.x --port 8888 --metric-name game_server --metrics-endpoint 9103

[Install]
WantedBy=multi-user.target
```
