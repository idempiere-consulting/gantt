python --version
cd /root/gantt
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_ENV=development
export FLASK_APP=ilserver-risorse.py
. /root/gantt/gantV/bin/activate
python --version
flask run --host=0.0.0.0 --port=8090
