# import geopandas
import geopy.location
from geopy.geocoders import Nominatim, GoogleV3
from geopy.extra.rate_limiter import RateLimiter
from config import Config
import pandas as pd
import folium
import os
from flask import url_for
import json
import shutil
from pathlib import Path
import requests


class ZipService:
    api_key = '18HL8EU1LH6KP5KNXJGV'
    sample_api_url = 'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/<endpoint>?key=<APIKEY>'
    sample_rest_url = 'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/GetZipCodeDetails/90210?key=DEMOAPIKEY'

    def __init__(self, zip):
        self.data = ZipService.get_zip_details(zip)

    @staticmethod
    def get_zip_details(zip_5:str):
        ustr = 'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/GetZipCodeDetails/{}'.format(zip_5)
        payload = {'key': ZipService.api_key}
        return requests.get(ustr, params=payload).json()





class AmazonZipLocations:

    def __init__(self):
        self.dff  = USffc.from_json(USffc.last_US_json)
        cols = list(self.dff.columns)
        # make country a new variable/column
        if 'country' not in cols:
            self.dff['country'] = self.dff.address.apply(lambda x: x[-3])
        if 'zips' not in cols:
            self.dff['zips'] = self.dff.address.apply(lambda x: x.split(',')[-2].strip())
            self.dff['state'] = self.dff['zips'].apply(lambda x: x.split(' ')[0].strip())
            self.dff['zips'] = self.diff.zips.apply(lambda x: x.split(' ')[1].strip())
        if 'geo_address' not in cols:
            self.dff['geo_address'] = self.dff.location.apply(lambda x: x['address'])





    @staticmethod
    def clean_zip(x):
        r = x.split(',')[-1].strip()
        if not r:
            return None
        if '-' in r:
            r = r[-10:]
            return r
        r = r[-5:]
        return r




    @staticmethod
    def pprint_dic(dic):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(dic)






class USffc:

    file1 = os.path.join(Config.data_dir['default'], 'afc_us.txt')
    cols = ['state', 'code', 'type', 'address']
    last_US_json = os.path.join(Config.data_dir['default'],  'amazon_fulfillment_centers.json')

    def __init__(self):

        with open(USffc.file1) as f:
            lines = f.readlines()
        slines = pd.Series(lines)
        ssll = slines.loc[slines.apply(lambda x: False if 'Featured' in x else True)]
        rows = [x.split('\t') for x in ssll]
        self.df = pd.DataFrame(rows,columns=USffc.cols)
        self.df = self.df.iloc[1:,]
        self.df.reset_index(drop=True,inplace=True)
        self.df = self.df.copy(deep=True)
        self.df.address = self.df.address.apply(lambda x: x.rstrip())

    def to_json(self, file=None):
        if file:
            jsn = self.df.to_json(file, orient='split')

        else:
            # overwrite last file
            jsn = self.df.to_json(USffc.last_US_json, orient='split')

        return jsn

    @staticmethod
    def from_json(filen=last_US_json):
        dff = pd.read_json(filen, orient='split')
        dff.point = dff.point.apply(lambda x: tuple(x) if x else None)
        # dff.drop(labels=['location'], axis=1, inplace=True)
        return dff


class CAffc:

    file = os.path.join(Config.data_dir['default'], 'canada_amazon.txt')
    cols = ['code', 'province', 'type', 'address']

    def __init__(self):
        with open (CAffc.file) as f:
            lines = f.readlines()
        self.slines = pd.Series(lines)
        self.rows = [s.split("=") for s in self.slines]
        self.df = pd.DataFrame(self.rows, columns=CAffc.cols)
        for col in self.df.columns:
            self.df[col] = self.df[col].apply(lambda x: x.strip())


class Mapp:

    def __init__(self, fn, addr=None, latitude=None,longitude=None,  desc=None):
        self.filename = fn

        self.address = addr
        self.latitude = latitude
        self.longitude = longitude
        self.name = Path(self.filename).stem
        self.descriptiton = desc
        self.markers = []

    def __repr__(self):
        return 'Mapp: name = {}, filename = {}, \naddress = {}, \nlatitude = {}, ' \
               'longitude = {}, description = {}'.format(self.name, self.filename, self.address, self.latitude,
                                                         self.longitude, self.descriptiton)

    def set_markers(self, mkrs: list):
        self.markers =  mkrs

    def set_name(self, name):
        self.name = name

    def set_description(self, desc):
        self.descriptiton = desc

    def to_dict(self):
        d_marks = []
        if self.markers:
            for m in self.markers:
                d_marks.append(m.to_dic())
        return {'filename': self.filename, 'address': self.address, 'latitude': self.latitude, 'longitude': self.longitude,
                'description': self.descriptiton, 'markers': d_marks}

    @staticmethod
    def from_dic(dic: dict):
        fn = dic['filename']
        addr = dic['address']
        lat = dic['latitude']
        lon = dic['longitude']
        desc = dic['description']
        markers = [Marker.from_dic(dic['markers'][x]) for x in dic['markers']]
        mapp =  Mapp(fn,addr=addr,latitude=lat, longitude=lon, desc=desc)
        mapp.markers = markers
        return mapp




class Marker:

    def __init__(self, lat, long, addr='', name=None, popup=None, tooltip=None):

        self.name = name
        self.latitude = lat
        self.longitude = long
        self.address = addr
        self.popup = self.address if not popup else popup
        self.tooltip = 'click me' if not tooltip else tooltip


    def set_popup(self, ht_txt):
        self.popup = ht_txt


    def set_tooltip(self, txt):
        self.tooltip = txt


    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.latitude

    def get_coordinates(self):
        return self.latitude, self.longitude

    def get_address(self):
        return self.address

    def to_dic(self):
        return {'latitude':self.get_latitude(), 'longitude': self.get_longitude(), 'name': self.name,
                'popup': self.popup, 'tooltip': self.tooltip}

    @staticmethod
    def from_dic(dic: dict):
        return Marker(dic['latitude'], dic['longitude'], dic['name'], dic['popup'], dic['tooltip'])


class MapsDB:

    mfile = os.path.join(Config.data_dir['default'], 'maps.json')
    zipcode_data_file = os.path.join(Config.data_dir['default'], 'clean_amazon_zipcode_data.json')
    selected_zip_data_keys = ['AsianPop', 'AverageFamilySize', 'AverageHouseValue', 'BlackPop', 'Bus03PayrollAnnual',
                              'City', 'CountiesArea', 'CountyANSI', 'CountyFIPS', 'CountyName', 'FemalePop',
                              'HawaiianPop', 'HispanicPop', 'HouseholdsPerZipcode', 'IncomePerHousehold',
                              'IndianPop', 'Latitude', 'Longitude', 'MSA', 'MSAName', 'MalePop', 'MedianAge',
                              'MedianAgeFemale', 'MedianAgeMale', 'Medicare_CBSA_Code', 'Medicare_CBSA_Name',
                              'Medicare_CBSA_Type', 'PersonsPerHousehold', 'PopulationEstimate', 'Region',
                              'SSA_State_County_Code', 'State', 'StateANSI', 'StateFIPS', 'TimeZone', 'WhitePop',
                              'ZipCode', 'ZipCodePopulation']

    def __init__(self):
        with open(MapsDB.mfile) as f:
            self.mdic =  json.load(f)
        with open(MapsDB.zipcode_data_file) as f:
            self.zipdata = json.load(f)
            self.clean_zip_data()

    def clean_zip_data(self):
        keys = list(self.zipdata.keys())
        for z in keys:
            self.zipdata[z] = self.zipdata[z]['item']
        rows  = [self.zipdata[z] for z in keys]
        self.df_zdata =  pd.DataFrame(data=rows)
        self.df_zdata = self.df_zdata[MapsDB.selected_zip_data_keys]


    def get_Mapp_from_db(self, name: str):

        dic = self.mdic.get(name, None)
        if dic is not None:
            return Mapp(dic['filename'],dic['address'], dic['latitude'], dic['longitude'], dic['description'])
        else:
            return None

    def add_mapp(self, map: Mapp):

        keys = self.mdic.keys()
        if map.name in keys:
            raise Exception("folium map name is already in DB")
        else:

            fn = map.filename
            a = map.address
            lo = map.longitude
            la = map.latitude
            d = map.descriptiton
            n = map.name
            dic = map.to_dict()
            self.mdic[n] = dic
            self.save_mapsDB()
            print('map {} stored in maps.json'.format(n))

    def save_mapsDB(self):
        import time
        from pathlib import Path
        timestr = time.strftime("%Y%m%d-%H%M%S")
        pp = Path(MapsDB.mfile)
        # stem = pp.stem
        # suf = pp.suffix
        # parent = pp.parent
        dst = Path.joinpath(pp.parent,'{}.{}{}'.format(pp.stem,timestr,pp.suffix))
        try:
            shutil.copyfile(MapsDB.mfile, str(dst))
            with open(MapsDB.mfile, "w") as f:
                json.dump(self.mdic, f)
        except Exception as inst:
            print(inst)


    def save_zipdata(self):
        import time
        from pathlib import Path
        timestr = time.strftime("%Y%m%d-%H%M%S")
        pp = Path(MapsDB.zipcode_data_file)
        # stem = pp.stem
        # suf = pp.suffix
        # parent = pp.parent
        dst = Path.joinpath(pp.parent, '{}.{}{}'.format(pp.stem, timestr, pp.suffix))
        try:
            shutil.copyfile(MapsDB.zipcode_data_file, str(dst))
            with open(MapsDB.zipcode_data_file, "w") as f:
                json.dump(self.zipdata, f)
        except Exception as inst:
            print(inst)

    def pop_mapp(self, mapname):
        self.mdic.pop(mapname)
        self.save_mapsDB()


class GeoTest:

    data_dir = Config.data_dir['default']
    sample_addrs = 'sample_addresses.csv'
    sample_single = 'Champ de Mars, Paris, France'


    @staticmethod
    def get_single_location(addr=sample_single):
        locator = GoogleV3(api_key='AIzaSyCE9TVk83kqFcOeJY88UHRRLx-AYDWCS28')
        try:
            location = locator.geocode(addr)
            lstr = 'Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude)
            return location, lstr
        except Exception as inst:
            return None, None

    def __init__(self, dff:pd.DataFrame):
        self.df = dff

    @staticmethod
    def get_df_addrs(data:pd.DataFrame = None):

        if not data:
           raise Exception("pandas df of addresses. ")
        else:

            locator = GoogleV3(api_key='AIzaSyCE9TVk83kqFcOeJY88UHRRLx-AYDWCS28')
            geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
            data['location'] = data['address'].apply(geocode)

            data['point'] = data['location'].apply(lambda loc: tuple(loc.point) if loc else None)
            data['address2'] = data['location'].apply(lambda loc: loc.address if loc else None)
            data['address'] = data['address2']
            data.drop(labels=['address2'], axis=1, inplace=True)
            data['latitude'] = data.location.apply(lambda x: x.latitude if x else None)
            data['longitude'] = data.location.apply(lambda x: x.longitude if x else None)
            data.drop(labels=['location'], axis=1, inplace=True)
            gtest = GeoTest(data)
            return data

    @staticmethod
    def get_folium_map(loc1: geopy.location.Location, mfile:str, desc=None, markers=None, tiles='OpenStreetMap',
                       attrib=None, API_key=None):

        m = folium.Map(location=[loc1.latitude, loc1.longitude], tiles=tiles, zoom_start=13,  width='75%',  height = '75%')

        # all map files should be in the flask templates directory, store only relative file names.
        m.save(os.path.join(Config.templates_dir, mfile))
        mapp = Mapp(mfile, addr=loc1.address, latitude=loc1.latitude, longitude=loc1.longitude, desc=desc )
        db = MapsDB()
        db.add_mapp(mapp)
        db.save_mapsDB()

        return mfile
