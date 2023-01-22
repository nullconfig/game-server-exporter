import click
from .game_server_exporter import GameServerCollector
from prometheus_client import start_http_server

@click.command()
@click.option('-c',
              '--container', 
              default='steamcmd', 
              help='Name of the docker container running',
              metavar='steamcmd')
@click.option('-p',
              '--server-port', 
              type=int, 
              default=8888, 
              help='UDP port for the server',
              metavar='8888')
@click.option('-m',
              '--metric-name', 
              help ='The name for the prometheus metrics',
              metavar='game_server')
@click.option('-me',
              '--metrics-endpoint', 
              type=int, 
              default=9103, 
              help='TCP port to host metrics endpoint',
              metavar='9103')
@click.option('-a',
              '--server-address',
              help='Address of the game server to exporter',
              metavar='x.x.x.x')
def main(container,server_address,server_port,metric_name,metrics_endpoint):
    start_http_server(metrics_endpoint)
    address = (server_address,server_port)
    GameServerCollector(container,metric_name,address).run_metrics_loop()
