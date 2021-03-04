python --version
# assume l'esistenza di una variabile di nome
# GANTTHOME=directory/di/base/
# il posto più comodo su un server è /etc/environment (system wide)
# in "casa" forse è più comodo nel .bashrc
echo $GANTTHOME

cd $GANTTHOME
pwd
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_ENV=development
export FLASK_APP=api_ilserver-risorse.py
#export FLASK_APP=api_ilserver-activity.py
. ./gantV/bin/activate
python --version
flask run --host=127.0.0.1 --port=8090
