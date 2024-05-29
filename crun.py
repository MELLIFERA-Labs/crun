import os
import sys
# set the path for ansible 
new_path = sys.exec_prefix + '/bin'
current_path = os.environ.get('PATH', '')
os.environ['PATH'] = new_path + os.pathsep + current_path

import json

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

import click
import tempfile
from pathlib import Path
import yaml
import ansible_runner

def pretty_print_with_highlight(data):
    """Pretty print a Python dictionary with syntax highlighting."""
    # Convert the dictionary to a formatted string
    formatted_str = json.dumps(data, indent=4)
    # Apply syntax highlighting using Pygments
    return highlight(formatted_str, PythonLexer(), TerminalFormatter())

def running_from_pex() -> bool:
    pex_root = os.environ.get("PEX_ROOT", os.path.expanduser("~/.pex"))
    return any([pex_root in p for p in sys.path])

def print_error(msg):
    click.echo(click.style(msg, fg='red'), err=True)

def convert_extra_vars(extra_vars):
    extra_vars_dict = {}
    extra_vars = filter(lambda x: x.strip() != '', extra_vars.split(';'))

    for var in extra_vars:
        key, value = var.strip().split('=')
        if value.strip().isdigit():
            value = int(value) 
        if type(value) == str and value.strip().lower() == 'true':
            value = True
        if type(value) == str and value.strip().lower() == 'false':
            value = False
        extra_vars_dict[key] = value
    return extra_vars_dict
 
default_vars = {
  'node_name': "CRUN_MELLIFERA_NODE",
  'download_cosmovisor_url': 'https://storage.mellifera.network/bins/general/cosmovisor', 
  'download_cosmovisor': True,
  'install_from': 'snapshot'
}

def get_playbook_folder():
    is_pex = running_from_pex()
    current_dir = Path(__file__).parent
    if is_pex:
       return current_dir / 'playbook'
    else: 
       return current_dir / 'resources/playbook'

@click.group()
def cli():
    pass

@cli.command()
def list():
    playbook_folder = get_playbook_folder()
    list = os.listdir(playbook_folder / 'group_vars')
    click.echo('List of available networks:')
    click.echo('---------------------------')

    for network in list:
        netname = network.split('.')[0]
        if netname != 'all':
         click.echo(netname)

def get_config_by_netname(netname):
    playbook_folder = get_playbook_folder()
    list_files = os.listdir(playbook_folder / 'group_vars')
    netnames = [{ "name": network.split('.')[0], "file": network  } for network in list_files]

    if netname not in map(lambda x: x['name'], netnames):
        return None
    netfile = next(filter(lambda x: x['name'] == netname, netnames))['file']
    
    with open(playbook_folder / 'group_vars' / netfile) as f:
        content = f.read()
        return yaml.full_load(content)

@cli.command()
@click.argument('netname')
@click.option('--extra-vars','-e', type=str , help="Show the configuration with the extra vars. Example: --extra-vars 'node_name=MELLIFERA;use_state_sync=true'")
def show(netname, extra_vars):
  ext = {}
  if extra_vars is not None:
    ext = convert_extra_vars(extra_vars)
  
  config = get_config_by_netname(netname)
  if config is None:
    print_error('Network %s not found' % netname)
    return 
  final_config = {**default_vars, **config, **ext}
  click.echo('------  %s config  ------' % netname) 
  click.echo(pretty_print_with_highlight(final_config))
  click.echo('------  %s config  ------' % netname)

@cli.command()
@click.argument('network_name')
@click.option('--extra-vars','-e', 
              type=str , 
              help="Run the installation with the overrided  vars. Example: --extra-vars 'node_name=MELLIFERA;install_from=state_sync'")
def install(network_name, extra_vars):
    playbook_folder = get_playbook_folder()
    ext = {}
    if extra_vars is not None:
        ext = convert_extra_vars(extra_vars)
    config = get_config_by_netname(network_name)
    if config is None:
        print_error('Network %s not found' % network_name)
        return
    final_config = {**default_vars, **config, **ext}
    if os.path.exists(final_config['cosmos_folder']):
        print_error('Cosmos folder %s already exists. Please remove it before running the installation or change "cosmos_folder" var with --extra-var option' % final_config['cosmos_folder'])
        return
     
    if os.geteuid() != 0:
        print_error('Installation requires root privileges. Creating services file and start systemd unit.\nPlease run: sudo crun install %s' % network_name)
        return
   
    click.echo('Running installation with the following configuration:')
    click.echo(pretty_print_with_highlight(final_config))
    with tempfile.TemporaryDirectory() as temp_dir_artifacts:
     ansible_runner.run(private_data_dir=playbook_folder, artifact_dir=temp_dir_artifacts, playbook='local.yml', passwords={}, extravars=final_config)


if __name__ == '__main__':
    cli()
