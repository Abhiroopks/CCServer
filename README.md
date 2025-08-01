# CCServer
Command &amp; Control of Remote Agents

## Setup
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate
```

## Running Server
```bash
# Activate the virtual env.
source .venv/bin/activate

# Run server
python3 manage.py runserver
```

## Running Agent
```bash
# Must run in linux environment with dependencies installed
python3 linux_agent.py
```


## TODO
* Agents create Result object and return to server
* web page for viewing Results
* Command object needs to be more complex
    * cmd to change polling interval for agent
    * add staging cmd
    * add exfil command
    * add shutdown agent cmd
* encrypt comms
* Make things prettier

