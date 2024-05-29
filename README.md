# CRUN 

CRUN is a simple command line tool to spin up blockchain node. It is designed to be simple and easy to use.

Python 3.8 or python3.10 is required to run this tool. 

## Installation

To install simply download the latest release from the [releases page](https://github.com/MELLIFERA-Labs/crun/releases/tag/v0.1.0)

## Usage


### Install a blockchain node example

```bash
crun install lava_testnet
```

### Change default settings 

1. Show the current settings for network 

```bash
crun show lava_testnet
```

2. You can check how setting will be changed by running the following command

```bash
crun show lava_testnet -e "install_from=state_sync"
```

3. Run install with new settings

```bash
crun install lava_testnet -e "install_from=state_sync"
```

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
