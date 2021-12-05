#! /bin/sh
if [ -d ".env" ];
then 
    echo "Enabling virtual environment"
else
    echo "No virtual environment was found"
    exit N
fi
. .env/bin/activate
export FLASK_ENV=development
python3 main.py
deactivate
