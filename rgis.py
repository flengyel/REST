#!/usr/bin/python
from __future__ import division
import json
import redis
from flask import Flask
from subprocess import Popen, PIPE
from reverseproxied import ReverseProxied
from string import rstrip
from random import randrange,shuffle
from preprocess  import loadmaps,IDkey
from bfs import traverse, traverseStrahler, traverseStrahlerRedis
#from loaddata import loadIDdictionary
from idmap import IDmap

# redis appears to be slower than loading maps from
# cPickle!
#ordermaps = loadmaps("NigerShapefiles/NigerRiverDictionary")

myfields = ['ID', 'q_dist_1m_annual' , 'q_dist25_1m_annual', 'q_dist50_1m_annual',	
                'CropLandAreaAcc','Pop2000','PopAcc2000','Runoff-01','Runoff-02','Runoff-03',
                'Runoff-04','Runoff-05','Runoff-06','Runoff-07','Runoff-08','Runoff-09',
                'Runoff-10','Runoff-11','Runoff-12','Runoff25-01','Runoff25-02','Runoff25-03',
		'Runoff25-04','Runoff25-05','Runoff25-06','Runoff25-07','Runoff25-08',	
                'Runoff25-09','Runoff25-10','Runoff25-11','Runoff25-12','Runoff50-01',
        	'Runoff50-02','Runoff50-03','Runoff50-04','Runoff50-05','Runoff50-06',
                'Runoff50-07','Runoff50-08','Runoff50-09','Runoff50-10','Runoff50-11',
                'Runoff50-12','Discharge-01','Discharge-02','Discharge-03','Discharge-04',
           	'Discharge-05','Discharge-06','Discharge-07','Discharge-08','Discharge-09',
		'Discharge-10','Discharge-11','Discharge-12','Discharge25-01','Discharge25-02',
		'Discharge25-03','Discharge25-04','Discharge25-05','Discharge25-06',
		'Discharge25-07','Discharge25-08','Discharge25-09','Discharge25-10',
		'Discharge25-11','Discharge25-12','Discharge50-01','Discharge50-02',
		'Discharge50-03','Discharge50-04','Discharge50-05','Discharge50-06',	
		'Discharge50-07','Discharge50-08','Discharge50-09','Discharge50-10',	
		'Discharge50-11','Discharge50-12']

idmap = IDmap('NigerShapefiles/NigerRiverActive1m.txt',myfields)
r     = redis.StrictRedis(host='localhost', port=6379, db=0)
#r     = redis.StrictRedis(unix_socket_path='/tmp/redis.sock', db=0)

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
    return json.dumps(traverseStrahlerRedis(r,cellno,ordno))

def cell2json(cell,name,fld):
    return json.dumps({ name:idmap.field(cell,fld)})


@app.route('/Africa/Niger/Discharge/Annual/<cell>')
def AfricaNigerUpstreamQ(cell):
    return cell2json(cell,'Discharge','q_dist_1m_annual')

@app.route('/Africa/Niger/Discharge25/Annual/<cell>')
def AfricaNigerUpstreamQ25(cell):
    return cell2json(cell,'Discharge25','q_dist25_1m_annual')
    
@app.route('/Africa/Niger/Discharge50/Annual/<cell>')
def AfricaNigerUpstreamQ50(cell):
    return cell2json(cell,'Discharge50','q_dist50_1m_annual')

@app.route('/Africa/Niger/Upstream/Cropland/<cell>')
def AfricaNigerUpstreamCropland(cell):
    return cell2json(cell,'Cropland','CropLandAreaAcc')

@app.route('/Africa/Niger/Upstream/Population/<cell>')
def AfricaNigerUpstreamPopulation(cell):
    return cell2json(cell,"Population", 'PopAcc2000')

@app.route('/Africa/Niger/Population/<cell>')
def AfricaNigerLocalPopulation(cell):
    return cell2json(cell,"Population", 'Pop2000')

@app.route('/Africa/Niger/Runoff/Monthly/<cell>/<mm>')
def AfricaNigerLocalRunoff(cell,mm):
    fieldname = 'Runoff-'+mm
    return cell2json(cell, fieldname, fieldname)

@app.route('/Africa/Niger/Runoff25/Monthly/<cell>/<mm>')
def AfricaNigerLocalRunoff25(cell,mm):
    fieldname = 'Runoff25-'+mm
    return cell2json(cell, fieldname, fieldname)

@app.route('/Africa/Niger/Runoff50/Monthly/<cell>/<mm>')
def AfricaNigerLocalRunoff50(cell,mm):
    fieldname = 'Runoff50-'+mm
    return cell2json(cell, fieldname, fieldname)

@app.route('/Africa/Niger/Discharge/Monthly/<cell>/<mm>')
def AfricaNigerDischargeMonthly(cell,mm):
    fieldname = 'Discharge-'+mm
    return cell2json(cell, fieldname, fieldname)

@app.route('/Africa/Niger/Discharge25/Monthly/<cell>/<mm>')
def AfricaNigerDischarge25Monthly(cell,mm):
    fieldname = 'Discharge25-'+mm
    return cell2json(cell, fieldname, fieldname)

@app.route('/Africa/Niger/Discharge50/Monthly/<cell>/<mm>')
def AfricaNigerDischarge50Monthly(cell,mm):
    fieldname = 'Discharge50-'+mm
    return cell2json(cell, fieldname, fieldname)


#@app.route('/Africa/Niger/Upstream/PopByCrop/<cell>')
#def AfricaNigerUpstreamPopByCrop(cell):
#    try:
#        lst = idct[cell]
#    except  KeyError:
#        return json.dumps({ name : -9999 })   
#    return json.dumps({ "PopByCrop":lst[3]/lst[4]})
    

    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
