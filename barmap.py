#!/usr/bin/python
from __future__ import division

barmap = {
  'q_dist_1m_annual' : 'Niger_Discharge_2000_06min_Colormap.clr',
  'q_dist25_1m_annual': 'Niger_Discharge25_1000_06min_Colormap.clr',
  'q_dist50_1m_annual':	'Niger_Discharge50_2000_06min_Colormap.clr',
  'CropLandAreaAcc': '',
  'Pop2000': '',
  'PopAcc2000': '',
  'Runoff-01': 'Runoff_01_2000_06min_Colormap.clr',
  'Runoff-02': 'Runoff_02_2000_06min_Colormap.clr',
  'Runoff-03': 'Runoff_03_2000_06min_Colormap.clr',
  'Runoff-04': 'Runoff_04_2000_06min_Colormap.clr',
  'Runoff-05': 'Runoff_05_2000_06min_Colormap.clr',
  'Runoff-06': 'Runoff_06_2000_06min_Colormap.clr',
  'Runoff-07': 'Runoff_07_2000_06min_Colormap.clr',
  'Runoff-08': 'Runoff_08_2000_06min_Colormap.clr',
  'Runoff-09': 'Runoff_09_2000_06min_Colormap.clr',
  'Runoff-10': 'Runoff_10_2000_06min_Colormap.clr',
  'Runoff-11': 'Runoff_11_2000_06min_Colormap.clr',
  'Runoff-12': 'Runoff_12_2000_06min_Colormap.clr',
  'Runoff25-01': 'Runoff25_01_2000_06min_Colormap.clr',
  'Runoff25-02': 'Runoff25_02_2000_06min_Colormap.clr',
  'Runoff25-03': 'Runoff25_03_2000_06min_Colormap.clr',
  'Runoff25-04': 'Runoff25_04_2000_06min_Colormap.clr',
  'Runoff25-05': 'Runoff25_05_2000_06min_Colormap.clr',
  'Runoff25-06': 'Runoff25_06_2000_06min_Colormap.clr',
  'Runoff25-07': 'Runoff25_07_2000_06min_Colormap.clr',
  'Runoff25-08': 'Runoff25_08_2000_06min_Colormap.clr',
  'Runoff25-09': 'Runoff25_09_2000_06min_Colormap.clr',
  'Runoff25-10': 'Runoff25_10_2000_06min_Colormap.clr',
  'Runoff25-11': 'Runoff25_11_2000_06min_Colormap.clr',
  'Runoff25-12': 'Runoff25_12_2000_06min_Colormap.clr',
  'Runoff50-01': 'Runoff50_01_2000_06min_Colormap.clr',
  'Runoff50-02': 'Runoff50_02_2000_06min_Colormap.clr',
  'Runoff50-03': 'Runoff50_03_2000_06min_Colormap.clr',
  'Runoff50-04': 'Runoff50_04_2000_06min_Colormap.clr',
  'Runoff50-05': 'Runoff50_05_2000_06min_Colormap.clr',
  'Runoff50-06': 'Runoff50_06_2000_06min_Colormap.clr',
  'Runoff50-07': 'Runoff50_07_2000_06min_Colormap.clr',
  'Runoff50-08': 'Runoff50_08_2000_06min_Colormap.clr',
  'Runoff50-09': 'Runoff50_09_2000_06min_Colormap.clr',
  'Runoff50-10': 'Runoff50_10_2000_06min_Colormap.clr',
  'Runoff50-11': 'Runoff50_11_2000_06min_Colormap.clr',
  'Runoff50-12': 'Runoff50_12_2000_06min_Colormap.clr',
  'Discharge-01': 'Discharge_01_2000_06min_Colormap.clr',
  'Discharge-02': 'Discharge_02_2000_06min_Colormap.clr',
  'Discharge-03': 'Discharge_03_2000_06min_Colormap.clr',
  'Discharge-04': 'Discharge_04_2000_06min_Colormap.clr',
  'Discharge-05': 'Discharge_05_2000_06min_Colormap.clr',
  'Discharge-06': 'Discharge_06_2000_06min_Colormap.clr',
  'Discharge-07': 'Discharge_07_2000_06min_Colormap.clr',
  'Discharge-08': 'Discharge_08_2000_06min_Colormap.clr',
  'Discharge-09': 'Discharge_09_2000_06min_Colormap.clr',
  'Discharge-10': 'Discharge_10_2000_06min_Colormap.clr',
  'Discharge-11': 'Discharge_11_2000_06min_Colormap.clr',
  'Discharge-12': 'Discharge_12_2000_06min_Colormap.clr',
  'Discharge25-01': 'Discharge25_01_2000_06min_Colormap.clr',
  'Discharge25-02': 'Discharge25_02_2000_06min_Colormap.clr',
  'Discharge25-03': 'Discharge25_03_2000_06min_Colormap.clr',
  'Discharge25-04': 'Discharge25_04_2000_06min_Colormap.clr',
  'Discharge25-05': 'Discharge25_05_2000_06min_Colormap.clr',
  'Discharge25-06': 'Discharge25_06_2000_06min_Colormap.clr',
  'Discharge25-07': 'Discharge25_07_2000_06min_Colormap.clr',
  'Discharge25-08': 'Discharge25_08_2000_06min_Colormap.clr',
  'Discharge25-09': 'Discharge25_09_2000_06min_Colormap.clr',
  'Discharge25-10': 'Discharge25_10_2000_06min_Colormap.clr',
  'Discharge25-11': 'Discharge25_11_2000_06min_Colormap.clr',
  'Discharge25-12': 'Discharge25_12_2000_06min_Colormap.clr',
  'Discharge50-01': 'Discharge50_01_2000_06min_Colormap.clr',
  'Discharge50-02': 'Discharge50_02_2000_06min_Colormap.clr',
  'Discharge50-03': 'Discharge50_03_2000_06min_Colormap.clr',
  'Discharge50-04': 'Discharge50_04_2000_06min_Colormap.clr',
  'Discharge50-05': 'Discharge50_05_2000_06min_Colormap.clr',
  'Discharge50-06': 'Discharge50_06_2000_06min_Colormap.clr',
  'Discharge50-07': 'Discharge50_07_2000_06min_Colormap.clr',
  'Discharge50-08': 'Discharge50_08_2000_06min_Colormap.clr',
  'Discharge50-09': 'Discharge50_09_2000_06min_Colormap.clr',
  'Discharge50-10': 'Discharge50_10_2000_06min_Colormap.clr',
  'Discharge50-11': 'Discharge50_11_2000_06min_Colormap.clr',
  'Discharge50-12': 'Discharge50_12_2000_06min_Colormap.clr',
  'GRUMP_Pop_2000': '',
  'RamCropland2000Km2': '',
  'Runoff_Annual_2000': 'Niger_Runoff_2000_06min_Colormap.clr',
  'Runoff25_Annual_2000': 'Niger_Runoff25_2000_06min_Colormap.clr',
  'Runoff50_Annual_2000': 'Niger_Runoff50_2000_6min_Colormap.clr',
  'AirTemperature_2000': 'Global_AirTemperature_2000_30min_Colormap.clr',
  'AirTemperature_2000-01': 'AirTemp_2000_01_30min_Colormap.clr',
  'AirTemperature_2000-02': 'AirTemp_2000_02_30min_Colormap.clr',
  'AirTemperature_2000-03': 'AirTemp_2000_03_30min_Colormap.clr',
  'AirTemperature_2000-04': 'AirTemp_2000_04_30min_Colormap.clr',
  'AirTemperature_2000-05': 'AirTemp_2000_05_30min_Colormap.clr',
  'AirTemperature_2000-06': 'AirTemp_2000_06_30min_Colormap.clr',
  'AirTemperature_2000-07': 'AirTemp_2000_07_30min_Colormap.clr',
  'AirTemperature_2000-08': 'AirTemp_2000_08_30min_Colormap.clr',
  'AirTemperature_2000-09': 'AirTemp_2000_09_30min_Colormap.clr',
  'AirTemperature_2000-10': 'AirTemp_2000_10_30min_Colormap.clr',
  'AirTemperature_2000-11': 'AirTemp_2000_11_30min_Colormap.clr',
  'AirTemperature_2000-12': 'AirTemp_2000_12_30min_Colormap.clr',
  'Precipitation_2000': 'Global_Precipitation_2000_30min_Colormap.clr',
  'Precipitation_2000-01': 'Precip_2000_01_30min_Colormap.clr',
  'Precipitation_2000-02': 'Precip_2000_02_30min_Colormap.clr',
  'Precipitation_2000-03': 'Precip_2000_03_30min_Colormap.clr',
  'Precipitation_2000-04': 'Precip_2000_04_30min_Colormap.clr',
  'Precipitation_2000-05': 'Precip_2000_05_30min_Colormap.clr',
  'Precipitation_2000-06': 'Precip_2000_06_30min_Colormap.clr',
  'Precipitation_2000-07': 'Precip_2000_07_30min_Colormap.clr',
  'Precipitation_2000-08': 'Precip_2000_08_30min_Colormap.clr',
  'Precipitation_2000-09': 'Precip_2000_09_30min_Colormap.clr',
  'Precipitation_2000-10': 'Precip_2000_10_30min_Colormap.clr',
  'Precipitation_2000-11': 'Precip_2000_11_30min_Colormap.clr',
  'Precipitation_2000-12': 'Precip_2000_12_30min_Colormap.clr',
  'Discharge_by_Pop_Dist_2000': 'Discharge_By_Population_Dist_2000_01min_Colormap.clr',
  'Discharge_by_Pop_Dist25_2000': 'Discharge_By_Population_Dist25_2000_01min_Colormap.clr',
  'Discharge_by_Pop_Dist50_2000': 'Discharge_By_Population_Dist50_2000_01min_Colormap.clr',
  'Runoff_by_Pop_Dist_2000': 'Runoff_by_Population_Dist_2000_01min_Colormap.clr',
  'Runoff_by_Pop_Dist25_2000': 'Runoff_by_Population_Dist25_2000_01min_Colormap.clr',
  'Runoff_by_Pop_Dist50_2000': 'Runoff_by_Population_Dist50_2000_01min_Colormap.clr',
}

