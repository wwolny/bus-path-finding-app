# AASD

## Requirements and installation
To create and activate [virtual environnement](https://docs.python.org/3/tutorial/venv.html) run:
```
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

Required version of Python is **>=3.8**.

All dependencies needed for the usage of the package are stored in the `requirements.txt` file. To install run:
```
pip install -r requirements.txt
```

In case of development install packages stored in the `requirements-dev.txt` file.

## XMPP server
To start XMPP server go to `containers` directory and run command `docker-compose up`. To stop container hit `ctrl+c` or run command `docker-compose stop` in other terminal (the same directory).

New users are added via `add_agents.sh` script. To execute script run eg. `source add_agents.sh`.

## Agents
### Driver
Implemented as FSM.

States:
* init - wait for other agents to be available
* chat - ready to take passengers
* dnf - full

Subscribe to all clients

