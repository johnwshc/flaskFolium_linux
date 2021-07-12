from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, session
# import geopy
# import folium
# from analz.geo_main import GeoTest as gt
from analz.geo_main import MapsDB, Mapp
from pathlib import Path
from config import Config
from analz.forms import CreateMapForm
from analz.geo_main import GeoTest, MapsDB

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_map/<name>', methods=['GET'])
def folium_single_map(name=None):
    if name is None:
        flash('no name provided',category='missing data')
        return redirect(url_for('hello_world'))
    mdb = MapsDB()
    if name in list(mdb.mdic.keys()):
        map = mdb.get_Mapp_from_db(name)
        address = map.address
        longitude = map.longitude
        latitude = map.latitude
        mfile = Path(map.filename).name
        return render_template('single_folium.html', map=mfile, address=address, latitude=latitude, longitude=longitude)
    else:
        flash('no existing map named {}'.format(name))
        return redirect(url_for('hello_world'))


@app.route('/make_map', methods=['GET', 'POST'])
def make_map():
    form = CreateMapForm()
    if form.validate_on_submit():
        mapname = form.mapname.data
        address = form.address.data
        loc, lstr = GeoTest.get_single_location(addr=address)
        map_fn = mapname + '.html'
        mfile = GeoTest.get_folium_map(loc,map_fn)
        return redirect(url_for('folium_single_map', name=mapname))
    return render_template('create_map.html', form=form)


if __name__ == '__main__':
    app.run()

