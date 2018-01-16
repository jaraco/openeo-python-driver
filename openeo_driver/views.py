from flask import request, url_for, jsonify

from openeo_driver import app
from .ProcessGraphDeserializer import graphToRdd, health_check


@app.route('/v0.1')
def index():
    return 'OpenEO GeoPyspark backend. ' + url_for('timeseries')

@app.route('/v0.1/health')
def health():
    return health_check()

@app.route('/v0.1/timeseries')
def timeseries():
    return 'OpenEO GeoPyspark backend. ' + url_for('point')


@app.route('/v0.1/timeseries/point', methods=['GET', 'POST'])
def point():
    if request.method == 'POST':
        print("Handling request: "+str(request))
        print("Post data: "+str(request.data))
        x = float(request.args.get('x', ''))
        y = float(request.args.get('y', ''))
        srs = request.args.get('srs', '')
        startdate = request.args.get('startdate', '')
        enddate = request.args.get('enddate', '')

        process_graph = request.get_json()
        image_collection = graphToRdd(process_graph, None)
        return jsonify(image_collection.timeseries(x, y, srs))
    else:
        return 'Usage: Query point timeseries using POST.'

@app.route('/v0.1/tile_service', methods=['GET', 'POST'])
def tile_service():
    if request.method == 'POST':
        print("Handling request: "+str(request))
        print("Post data: "+str(request.data))
        process_graph = request.get_json()
        image_collection = graphToRdd(process_graph, None)
        return jsonify(image_collection.tiled_viewing_service())
    else:
        return 'Usage: Retrieve tile service endpoint.'