# Alma location checker
## Requirements
1. Python3 and virtualenv
```bash
sudo apt update
sudo apt install python3-virtualenv
```
2. venv
```bash
virtualenv venv
. venv/bin/activate
```

3. run
```bash
pip install --editable .
alma-location-checker --loglevel INFO
```