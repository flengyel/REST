#!/usr/bin/python
from   __future__ import division
from   constants import Const
import json
import redis
from   flask import Flask
from   subprocess import Popen, PIPE
from   reverseproxied import ReverseProxied
from   string import rstrip
from   random import randrange,shuffle
from   preprocess  import loadmaps
from   bfs import traverse, traverseStrahler, traverseStrahlerRedis
from   idmap import IDmap

# redis appears to be slower than loading maps from
# cPickle!
ordermaps = loadmaps("NigerShapefiles/NigerRiverDictionary")

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


# Use redis 2.6+. Redis 2.4.9 (used by cartodb) does not support StrictRedis().
r     = redis.StrictRedis(host='localhost', port=6379, db=0)

myidmap = IDmap('NigerShapefiles/NigerRiverActive1m.txt',myfields)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

def cell2json(cell,name,fld):
#   print "cell2json cell type:", type(cell)
    return json.dumps({ name:myidmap.field(cell,fld)})

def c2f(cell,fld):
#   print "c2f cell type:", type(cell)
    return myidmap.field(cell,fld)

@app.route('/')
def list_functions():
    return 'netAccumulate'


bindir='/usr/local/share/ghaas/bin/'
pntgridvalue=bindir+'pntGridValue ' # note the space afterwards


@app.route('/Africa/Elevation/15sec/<lat>/<lon>')
def AfricaElevation15sec(lat,lon):
    datadir='/data/RGISarchive/Africa/Elevation/HydroSHEDSv110/15sec/Static/'
    indicator=datadir+'Africa_Elevation_HydroSHEDSv110_15sec_Static.gdbc'
    p=Popen(pntgridvalue  + indicator +  ' -c '+lat+','+lon, stdout=PIPE,stderr=PIPE,shell=True)
    print p.wait()
    lst = p.stdout.read().split()
    return json.dumps({rstrip(lst[0],':'):lst[1]})


@app.route('/Africa/Niger/Upstream/Order/<lat>/<lon>/<cell>/<order>')
def AfricaNigerUpstreamOrder(lat,lon,cell,order):
    try:
	cellno = int(cell)
        ordno  = int(order)    
    except ValueError:
	return json.dumps({ "Upstream": [] })	
#   return json.dumps(traverseStrahlerRedis(r,cellno,ordno))
    return json.dumps(traverseStrahler(ordermaps,cellno,ordno))


DISCHARGE = ['q_dist_1m_annual', 'q_dist25_1m_annual', 'q_dist50_1m_annual']         
BODCOD = [0.15, 0, 0.3, 0.75, 0.85]
BOD5 = 11
NOVALUE = -9999.0

@app.route('/Africa/Niger/Scenario/Annual/BOD/<int:cell>/<int:irr>/<int:wwt>')
def AfricaNigerScenarioAnnualBOD(cell, irr, wwt):
    retval = { "BOD" : NOVALUE }
    if irr < 0 or irr > 2 or wwt < 0 or wwt > 4:
        return json.dumps(retval)
    # Christ -- dynamic typing strikes again. The cell used to index 
    # is a string?!?
    Q = c2f(cell,DISCHARGE[irr])    
#    print 'Q',Q, 1-BODCOD[wwt],irr, DISCHARGE[irr], cell, c2f(2, 'q_dist_1m_annual')
    if Q == NOVALUE:
        return json.dumps(retval)
    try:
        retval["BOD"] = BOD5 * 100000 / Q * (1 - BODCOD[wwt]) 
    except ZeroDivisionError:
        return json.dumps(retval)
    return json.dumps(retval)
 

def BODcalc(wwt,Q):
    try:
        loading = BOD5 * 100000 / Q * (1 - BODCOD[wwt])
    except ZeroDivisionError:
        return NOVALUE
    return loading

def BODmap(Q):
    return { "wwt0": BODcalc(0,Q), "wwt1": BODcalc(1,Q), "wwt2": BODcalc(2,Q),
             "wwt3": BODcalc(3,Q), "wwt4": BODcalc(4,Q) }

def irrQ(cell,irr):
    return c2f(cell,DISCHARGE[irr])    

def BODCODmap(cell):
    return { "irr0": BODmap(irrQ(cell,  0)), "irr25": BODmap(irrQ(cell, 1)), 
              "irr50": BODmap(irrQ(cell, 2)) }
    
    
@app.route('/Africa/Niger/Annual/BOD/<int:cell>')
def AfricaNigerAnnualBOD(cell):
    return json.dumps(BODCODmap(cell)) 
   
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
