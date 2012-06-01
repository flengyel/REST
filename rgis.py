from flask import Flask
from subprocess import Popen, PIPE
from reverseproxied import ReverseProxied
from string import rstrip
import json

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)


@app.route('/')
def list_functions():
    return 'netAccumulate'

@app.route('/ls')
def ls_app():
    return Popen('ls', stdout=PIPE,shell=True).stdout.read()


bindir='/usr/local/share/ghaas/bin/'
pntgridvalue=bindir+'pntGridValue ' # note the space afterwards

@app.route('/netAccumulate')
def netacc():
    p=Popen(bindir+'netAccumulate --help',stdout=PIPE,stderr=PIPE,shell=True)
    print p.wait()
    return p.stdout.read() + p.stderr.read()


@app.route('/elev/<lat>/<lon>')
def elev(lat,lon):
    p=Popen(bindir+'pntGridValue Net+Elevation_15s.gdbc -c '+lat+','+lon, stdout=PIPE,stderr=PIPE,shell=True)
    print p.wait()
    lst = p.stdout.read().split()
    return json.dumps({rstrip(lst[0],':'):lst[1]})

@app.route('/Africa/Elevation/15sec/<lat>/<lon>')
def AfricaElevation15sec(lat,lon):
    datadir='/data/RGISarchive/Africa/Elevation/HydroSHEDSv110/15sec/Static/'
    indicator=datadir+'Africa_Elevation_HydroSHEDSv110_15sec_Static.gdbc'
    p=Popen(pntgridvalue  + indicator +  ' -c '+lat+','+lon, stdout=PIPE,stderr=PIPE,shell=True)
    print p.wait()
    lst = p.stdout.read().split()
    return json.dumps({rstrip(lst[0],':'):lst[1]})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
