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
    print len(rec0.shape.points), " points: ", rec0.shape.points
    print len(rec0.record), " record: ", rec0.record
    for sr in sh.shapeRecords():
	print "ID: ", sr.record[7]
	print "NAME:", sr.record[8]
	print "UPSTREAM:", sr.record[9]
