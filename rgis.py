from flask import Flask
from subprocess import Popen, PIPE
from reverseproxied import ReverseProxied
from string import rstrip
import json
from random import randrange,shuffle
from niger import loadmaps
from bfs import traverse, traverseStrahler

maps = loadmaps("NigerShapefiles/NigerRiverDict")
ordermaps = loadmaps("NigerShapefiles/NigerRiverDictionary")

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

@app.route('/Africa/Niger/Upstream/<lat>/<lon>/<cell>')
def AfricaNigerUpstream(lat,lon,cell):
    try:
	cellno = int(cell)
    except ValueError:
	return json.dumps({ "Upstream": [] })	
    return json.dumps(traverse(maps,cellno))

# load the correct maps
@app.route('/Africa/Niger/Upstream/Order/<lat>/<lon>/<cell>/<order>')
def AfricaNigerUpstreamOrder(lat,lon,cell,order):
    try:
	cellno = int(cell)
        ordno  = int(order)    
    except ValueError:
	return json.dumps({ "Upstream": [] })	
    return json.dumps(traverseStrahler(ordermaps,cellno,ordno))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
