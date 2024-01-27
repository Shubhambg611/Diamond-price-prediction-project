echo [$(date)]: "START"

echo [$(date)]: "creating env with 3.8 version"

conda create --prefix ./env python=3.8 -y

echo [$(date)]: "actiavting the enviroment"

source activate ./env

echo [$(date)]: "installig the dev requirements"

pip install -r requirements.txt

echo[$(date)]:"END"