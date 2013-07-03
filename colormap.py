#!/usr/bin/python
# Create jQuery flot data structure from ESRI color map
# Author: Florian Lengyel
# Date:   Jun 25, 2013
# License: MIT
from __future__ import division
import sys
import argparse as arg
import json as js

descript = "Convert ArcGIS Color Table plugin syntax to flot data structure"
epistr   = "Software is released under the GPL (c) 2013 Florian Lengyel, CUNY Environmental CrossRoads Initiative, Advanced Science Research Center, The City College of New York. Contact: gmail/skype/twitter florianlengyel."
parser  = arg.ArgumentParser( description = descript, epilog=epistr )
parser.add_argument( '-s', '--scaling',
		     type=int,
		     default=1,
		     help='Scale values by int multiple; e.g., a power of 10.')
parser.add_argument( 'color_table', 
		     type=arg.FileType('r'),
		     help='Name of BC-Consult Color Table file' )

class ColorMap(object):
  def color(self, args, map):
      return  '#{0:02x}{1:02x}{2:02x}'.format( map['red'], map['green'], map['blue'] )

  def __init__(self, args):
      self.mymap = dict()
      self.colormap = []
      self.valuemap = []
      for line in args.color_table:
        field = line.split(' ')
        map = { 'value': int(field[0].strip())/args.scaling, 
      	        'red'  : int(field[1].strip()),
  	        'green': int(field[2].strip()),
	        'blue' : int(field[3].strip())}
        self.colormap.append( self.color(args, map) )
        self.valuemap.append( map['value'] )
      self.mymap['colors'] = self.colormap 
      self.mymap['values'] = self.valuemap
    

if __name__ == '__main__':
  args = parser.parse_args()
  cm   = ColorMap(args)
  print  cm.mymap
  a = js.dumps(cm.mymap)
  print js.loads(a)
