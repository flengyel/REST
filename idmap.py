#!/usr/bin/python
from __future__ import division
import collections
from   constants import Const
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
    self.NOVALUE = Const.NOVALUE
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
    idmap = IDmap(Const.DATABASE, Const.FIELDS) 
    print idmap.tuple('2')  
    print zip(Const.FIELDS[1:], idmap.tuple('2'))
    print idmap.field('2','q_dist_1m_annual')
    print idmap.field('2','GRUMP_Pop_2000')
    print idmap.field('1','RamCropland2000Km2')
    print idmap.field('2','RamCropland2000Km2')
    print idmap.field('3','RamCropland2000Km2')
    print idmap.field('2','Runoff_Annual_2000')
    print idmap.field('2','Runoff25_Annual_2000')
    print idmap.field('2','Runoff50_Annual_2000')
