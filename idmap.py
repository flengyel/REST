#!/usr/bin/python
from __future__ import division
import collections

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
           ID = lst[fieldmap['ID']]
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
     return self.idmap[ID] # This violates OOP

  def field(self,ID,field):
     try:
        t = self.idmap[ID] # get the tuple
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
    myfields = ['ID', 'q_dist_1m ascii', 'q_dist25_1m ascii', 'q_dist50_1m ascii', 'PopAcc2000', 'CropLandAreaAcc']
    idmap = IDmap('NigerShapefiles/NigerID2PopCrop.txt', myfields) 
    print idmap.tuple('220')  
    print zip(myfields[1:], idmap.tuple('220'))
    print idmap.field('220','CropLandAreaAcc')
    print idmap.field('220','q_dist_1m ascii')
    print idmap.field('220','bogus')
    print idmap.field('304201','CropLandAreaAcc')    

