import subprocess
import time
import a2s

from prometheus_client import (
    Gauge
)

class GameServerMetrics:
    def __init__(self,container,address):
        self.container = container
        self.address = address

    def get_container_status(self):
        status = subprocess.check_output("docker ps -a| grep " + self.container + " | awk '{print $8}'",
                                         shell=True,
                                         stderr=subprocess.STDOUT).decode("utf-8").strip()
        if 'Up' in status:
            return 0
        else:
            return 1

    def get_player_count(self):
        try:
            return len(a2s.players(self.address))
        except:
            pass
            return 0

    def get_server_info(self):
        try:
            info = a2s.info(self.address)
            if info.server_name:
                return 0
            else:
                return 1
        except:
            pass
            return 1

class GameServerCollector(GameServerMetrics):
    def __init__(self,container,metric_name,address):
        super().__init__(container,address)
        self.metric_name = metric_name
        self.container_status = Gauge(f'{self.metric_name}_container',
                                      'Container status up or down',
                                      labelnames=['container_status']).labels('isDown')
        self.player_count = Gauge(f'{self.metric_name}_players',
                                  'Current active players', 
                                  labelnames=['active_players']).labels('online')
        self.server_status = Gauge(f'{self.metric_name}_status',
                                   'Server status from query',
                                   labelnames=['server_status']).labels('status')

    def collect(self):
        self.container_status.set(self.get_container_status())
        self.player_count.set(self.get_player_count())
        self.server_status.set(self.get_server_info())

    def run_metrics_loop(self):
        while True:
            self.collect()
            time.sleep(30)
