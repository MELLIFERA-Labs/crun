l# CRUN 

CRUN is a simple command line tool to spin up blockchain node. It is designed to be simple and easy to use.

Python 3.8 or python3.10 is required to run this tool. 

## Installation

To install simply download the latest release from the [releases page](https://github.com/MELLIFERA-Labs/crun/releases/tag/v0.1.0)

You can use command for download
```bash

wget https://github.com/mellifera-labs/crun/releases/latest/download/crun 
chmod +x crun  

```

## Usage

Install with default settings 

```bash
crun install lava_testnet
```
Check `crun list` for available networks for install

## Example of usage 

You can override any setting from `crun show <network>` output by passing `-e` flag with `key=value` pairs. 

For example, let's check the settings for lava_testnet

```bash
crun show lava_testnet
```

```yaml
hain_id: lava-testnet-2
netname: lava_testnet
repo: https://github.com/lavanet/lava.git
version: v2.1.1
binary: lavad
genesis: https://storage.mellifera.network/lava_testnet/genesis.json
addressbook: https://storage.mellifera.network/lava_testnet/addrbook.json
snapshot: https://storage.mellifera.network/lava_testnet/snapshot_latest.tar.lz4
go_version: go1.20.14
cosmos_folder: '.lava'
...etc
```
Any of these settings can be overridden with `-e` flag. 

Here is few examples of usage:

1. Install lava_testnet from state_sync

```bash
# Check modified settings 
crun show lava_testnet -e "install_from=state_sync"
# Run crun to Install lava_testnet from state_sync
crun install lava_testnet -e "install_from=state_sync"
```

2. Install `lava_testnet` with custom port prefix and custom cosmos folder

```bash
crun install lava_testnet -e "custom_port_prefix=137;cosmos_folder=.lavatestnet"
```
This command will install lava_testnet with custom port prefix 137 and cosmos HOME folder .lavatestnet

RPC port will be 13757, P2P port will be 13756, GRPC port will be 13790, REST port will be 13717; instead of default 26657, 26656, 9090, 1317


## Install crun from source

1. Clone the repository

2. Create venv and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```
3. Run crun

```bash
python crun.py
```

## Supported networks

- Namada mainnet
- Lava testnet
- Lava mainnet 
- Warden testnet
- Kyve mainnet


Check more how it works with our [services](https://services.mellifera.network/)


