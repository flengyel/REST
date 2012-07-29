#!/usr/bin/python
from __future__ import division
import collections
# type annotation obsolete.
#from pyanno import returnType, parameterTypes, privateMethod, protectedMethod, selfType, ignoreType


# given 
#    fname: the filename of an RGIS created ascii river network with an ID to grid sampled data values
#    myfields: a list of singly quoted strings of field names of interest  including 'ID' (at the beginning)
# 
# create two dictionaries: 
#    idmap:    dictionary mapping ID to the tuple of selected fields
#    dictmap:  mapping of the field names to indexes within the selection

# return river network segment ID to (cropland area, q, q+25%, q+50%)
# Note that many segments have nothing upstream -- we must supply the
# nodata values -- they do not appear in the output processed by RGIS.

# Note: if there are missing values, this shows up as empty!
# Provide the list of names and the list of fields

class IDmap(object):
  """IDmap objects define mappings between vector data IDs and gridded data fields"""

  def __init__(self, fname, myfields):
    self.NOVALUE = -9999.0
    self.fname = fname
    self.myfields = myfields  
    fieldmap = dict()        # this is private, intimate even
    self.idmap    = collections.defaultdict(tuple)  # extensible tuple
    header   = True
    fields = len(self.myfields)
    for line in open(self.fname,'r'):
	lst = line.split('\t')
        if header:
           header = False
	   for i in range(len(lst)):
               string = lst[i].rstrip()  # the last field may have trailing spaces
               string = string[1:-1]     # remove the double quotations at the beginning and end
               fieldmap[string] = i # note the field number in the RGIS file
        else:   
           ID = lst[fieldmap['ID']]      # subtlety: the type is a string. A dictionary 
                                         # interprets a unicode ket as a string apparently 
           for field in self.myfields[1:]:   
	       try:
                  v = float(lst[fieldmap[field]])
               except ValueError:
		  v = self.NOVALUE
		  # print ID
               finally:
                  self.idmap[ID] += (v,)

    # create myfield to dictionary tuple index 
    self.tuplemap  = dict()   # maps the field name to dictionary tuple field
    for i in range(len(self.myfields[1:])):
       self.tuplemap[self.myfields[1:][i]] = i

  def tuple(self,ID): 
     return self.idmap[str(ID)] # This violates OOP

  
  def field(self,ID,field):
     try:
        t = self.idmap[str(ID)] # get the tuple -- this is defensive.
     except KeyError:
        return self.NOVALUE
     try:
	i = self.tuplemap[field]
     except KeyError:
        return self.NOVALUE
     try:
	v = t[i]
     except IndexError:
        return self.NOVALUE
     return v
        

if __name__ == '__main__':
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

    idmap = IDmap('NigerShapefiles/NigerRiverActive1m.txt', myfields) 
    print idmap.tuple('2')  
    print zip(myfields[1:], idmap.tuple('2'))
    print idmap.field('2','q_dist_1m_annual')

