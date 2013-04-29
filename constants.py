#!/usr/bin/python
from __future__ import division

class Const:
  NOVALUE = -9999.0
  SHAPEFILE='NigerShapefiles/Niger_River_Active_1min.shp'
  SHAPEFILE15s='NigerShapefiles/Niger_Basin_15s.shp'
  DICTIONARY='NigerShapefiles/NigerRiverDictionary'
  DATABASE='NigerShapefiles/NigerRiverActive1mJ.txt'
  FIELDS = ['ID', 'q_dist_1m_annual' , 'q_dist25_1m_annual', 'q_dist50_1m_annual',	
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
     'Discharge50-11','Discharge50-12','GRUMP_Pop_2000', 'RamCropland2000Km2',
     'Runoff_Annual_2000', 'Runoff25_Annual_2000', 'Runoff50_Annual_2000',
     'AirTemperature_2000','AirTemperature_2000-01','AirTemperature_2000-02',
     'AirTemperature_2000-03','AirTemperature_2000-04','AirTemperature_2000-05',
     'AirTemperature_2000-06','AirTemperature_2000-07','AirTemperature_2000-08',
     'AirTemperature_2000-09','AirTemperature_2000-10','AirTemperature_2000-11',
     'AirTemperature_2000-12','Precipitation_2000','Precipitation_2000-01',
     'Precipitation_2000-02','Precipitation_2000-03','Precipitation_2000-04',
     'Precipitation_2000-05','Precipitation_2000-06','Precipitation_2000-07',
     'Precipitation_2000-08','Precipitation_2000-09','Precipitation_2000-10',
     'Precipitation_2000-11','Precipitation_2000-12', 'Discharge_by_Pop_Dist_2000', 
     'Discharge_by_Pop_Dist25_2000', 'Discharge_by_Pop_Dist50_2000', 
     'Runoff_by_Pop_Dist_2000', 'Runoff_by_Pop_Dist25_2000', 'Runoff_by_Pop_Dist50_2000']
  DISCHARGE = ['q_dist_1m_annual', 'q_dist25_1m_annual', 'q_dist50_1m_annual']         
  BODCOD = [0.15, 0, 0.3, 0.75, 0.85]
  NITROGEN = [0.15, 0, 0.1, 0.25, 0.7]
  BOD5 = 11
  COD  = 36.5
  TotNITROGEN = 3.7
  TotPHOSPHOROUS = 0.9


