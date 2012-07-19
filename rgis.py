#!/usr/bin/python
from __future__ import division
from flask import Flask
from subprocess import Popen, PIPE
from reverseproxied import ReverseProxied
from string import rstrip
import json
from random import randrange,shuffle
from preprocess  import loadmaps
from bfs import traverse, traverseStrahler
from loaddata import loadIDdictionary

#maps = loadmaps("NigerShapefiles/NigerRiverDict")
ordermaps = loadmaps("NigerShapefiles/NigerRiverDictionary")
idct = loadIDdictionary('NigerShapefiles/ID2q+q25+q50+pop+crop.txt')

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)


@app.route('/')
def list_functions():
    return 'netAccumulate'


bindir='/usr/local/share/ghaas/bin/'
pntgridvalue=bindir+'pntGridValue ' # note the space afterwards

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

#@app.route('/Africa/Niger/Upstream/<lat>/<lon>/<cell>')
#def AfricaNigerUpstream(lat,lon,cell):
#   try:
#	cellno = int(cell)
#    except ValueError:
#	return json.dumps({ "Upstream": [] })	
#    return json.dumps(traverse(maps,cellno))

# load the correct maps
@app.route('/Africa/Niger/Upstream/Order/<lat>/<lon>/<cell>/<order>')
def AfricaNigerUpstreamOrder(lat,lon,cell,order):
    try:
	cellno = int(cell)
        ordno  = int(order)    
    except ValueError:
	return json.dumps({ "Upstream": [] })	
    return json.dumps(traverseStrahler(ordermaps,cellno,ordno))

def cell2json(name,idx,cell):
    try:
        lst = idct[cell]
    except  KeyError:
        return json.dumps({ name : -9999 })   
    return json.dumps({ name:lst[idx]})


@app.route('/Africa/Niger/Upstream/Discharge/<cell>')
def AfricaNigerUpstreamQ(cell):
    return cell2json("Discharge",0,cell)

@app.route('/Africa/Niger/Upstream/Discharge25/<cell>')
def AfricaNigerUpstreamQ25(cell):
    return cell2json("Discharge25",1,cell)
    
@app.route('/Africa/Niger/Upstream/Discharge50/<cell>')
def AfricaNigerUpstreamQ50(cell):
    return cell2json("Discharge50",2,cell)

@app.route('/Africa/Niger/Upstream/Population/<cell>')
def AfricaNigerUpstreamPopulation(cell):
    return cell2json("Population",3,cell)

@app.route('/Africa/Niger/Upstream/Cropland/<cell>')
def AfricaNigerUpstreamCropland(cell):
    return cell2json("Cropland",4,cell)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
