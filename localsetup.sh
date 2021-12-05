#! /bin/sh
if [ -d ".env" ];
then
    echo ".env folder found, installing dependencies using pip3"
else 
    echo ".env folder is not found, creating a virtual environment"
    python3.8 -m venv .env
fi
. .env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
deactivate
