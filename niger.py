#!/usr/bin/python
import shapefile

if __name__ == '__main__':
    sh = shapefile.Reader("Niger_River_Active_1min.shp")
    print "Loading shapes..."
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
