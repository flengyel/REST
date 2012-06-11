#!/usr/bin/python
import shapefile

def latlonstr(lat,lon):
    fspec = '%.17f'
    return fspec % lat + ',' + fspec % lon

def shapeID(sr):
    return sr.record[7]	# a magic number

def pass1(shapes):
    dct = dict()
    for rec in shapes.shapeRecords():
	bbox = rec.shape.bbox
	tgt = latlonstr(bbox[2],bbox[3])
	dct[tgt] = [shapeID(rec)]    # target goes to segment shape ID and empty list
	print tgt, dct[tgt]
    return dct

def pass2(shapes, dct):
    for rec in shapes.shapeRecords():
	bbox = rec.shape.bbox
	src = latlonstr(bbox[0],bbox[1])
	if src in dct:
	    IDlist = dct[src]
            IDlist.append(shapeID(rec)) # gotcha: this modifies the list and returns none
	    dct[src] = IDlist 
 	    print src, dct[src]
    return dct	 
	

if __name__ == '__main__':
    print latlonstr(10.0102020201012,6.123456789012345)
    sh = shapefile.Reader("Niger_River_Active_1min.shp")
    print "Loading shapes..."
    dct = pass1(sh)
    pass2(sh, dct)
    exit(0)
    shape = sh.shapes()
    print len(sh.fields), " fields: ", sh.fields
    print "Loading records..."
    sr = sh.shapeRecords()
    rec0 = sr[0]
    print "shapeType: ", rec0.shape.shapeType
    print len(rec0.shape.points), "points: ", rec0.shape.points
    print "bbox:", rec0.shape.bbox
    print len(rec0.record), "record: ", rec0.record
    for sr in sh.shapeRecords():
        shp = sr.shape
        print shp.bbox
        print shp.bbox[2]-shp.bbox[0],shp.bbox[3]-shp.bbox[1]
	print "ID: ", sr.record[7]
	print "NAME:", sr.record[8]
	print "UPSTREAM:", sr.record[9]
