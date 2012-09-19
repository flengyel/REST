#!/usr/bin/python
from   __future__ import division
from   constants import Const
import json
import sys
import numpy  # for array
#import redis
from   flask import Flask
from   subprocess import Popen, PIPE
from   reverseproxied import ReverseProxied
from   string import rstrip
from   random import randrange,shuffle
from   preprocess  import loadmaps
from   bfs import traverse, traverseStrahler, traverseStrahlerRedis
from   idmap import IDmap
from   histogram import histogram

# redis appears to be slower than loading maps from
# cPickle!
myMaps = loadmaps(Const.DICTIONARY)

# Use redis 2.6+. Redis 2.4.9 (used by cartodb) does not support StrictRedis().
#r     = redis.StrictRedis(host='localhost', port=6379, db=0)

myIDmap = IDmap(Const.DATABASE, Const.FIELDS)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

def cell2json(cell,name,fld):
#   print "cell2json cell type:", type(cell)
    return json.dumps({ name:myIDmap.field(cell,fld)})

def c2f(cell,fld):
#    print >> sys.stderr, "c2f cell type:", type(cell), "cell:", cell, 'field:', fld
    return myIDmap.field(cell,fld)

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
    return json.dumps(traverseStrahler(myMaps,cellno,ordno))



def WWTcalc(load, removal, wwt,Q):
    try:
        loading = load * 100000 / Q * (1 - removal[wwt])
    except ZeroDivisionError:
        return Const.NOVALUE
    return loading

def WWTmap(load,removal,Q):
    return { "wwt0": WWTcalc(load,removal,0,Q), 
             "wwt1": WWTcalc(load,removal,1,Q), 
	     "wwt2": WWTcalc(load,removal,2,Q),
             "wwt3": WWTcalc(load,removal,3,Q), 
	     "wwt4": WWTcalc(load,removal,4,Q) }

def irrQ(cell,irr):
    return c2f(cell,Const.DISCHARGE[irr])    


def WWTmatrix(load,removal,cell):
    """load is the load factor BOD5 or COD"""
    return { "irr0":   WWTmap(load,removal,irrQ(cell,  0)), 
	     "irr25":  WWTmap(load,removal,irrQ(cell, 1)), 
             "irr50":  WWTmap(load,removal,irrQ(cell, 2)) }
    
    
@app.route('/Africa/Niger/Annual/BOD/<int:cell>')
def AfricaNigerAnnualBOD(cell):
    return json.dumps(WWTmatrix(Const.BOD5,Const.BODCOD,cell)) 
   
@app.route('/Africa/Niger/Annual/COD/<int:cell>')
def AfricaNigerAnnualCOD(cell):
    return json.dumps(WWTmatrix(Const.COD,Const.BODCOD,cell)) 

@app.route('/Africa/Niger/Annual/NITROGEN/<int:cell>')
def AfricaNigerAnnualNitrogen(cell):
    return json.dumps(WWTmatrix(Const.TotNITROGEN,Const.NITROGEN,cell)) 

@app.route('/Africa/Niger/Annual/PHOSPHOROUS/<int:cell>')
def AfricaNigerAnnualPhosphorous(cell):
    return json.dumps(WWTmatrix(Const.TotPHOSPHOROUS,Const.NITROGEN,cell)) 

#### Basic Histograms ####
# histogram(maps, myIDmap, key, order, myField, bins):
# def histog"""Returns count, freq array, bin endpoints, (ID, Value, Bin) list"""
@app.route('/Africa/Niger/Hist/<int:cell>/<int:order>/<field>/<int:bins>')
def AfricaNigerHistogram(cell,order,field,bins):
    count, frequencies, endpoints, _ = histogram(myMaps, myIDmap, cell, order,field, bins)
    ends = numpy.array(endpoints)
    midpoints = 0.5*(ends[1:]+ends[:-1])
    freqs = numpy.array(frequencies)
    props = freqs/count
    # NOTE: numpy.array([...]) is not JSON serializable; convert to list
    return json.dumps({ 'id' : cell, 'count' : count, 
                        'freqs': frequencies,
                        'endpoints' : endpoints, 
	                'midpoints' : list(midpoints), 
                        'proportions' : list(props) })



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
    app.debug=True
    app.run(host='0.0.0.0')
