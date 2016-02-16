from flask import Flask, request, jsonify, make_response
from functools import wraps
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

secret_keys = {}
available_parcels = {142: [1, 2],
                     145: [2, 3],
                     147: [2, 1]}
on_the_road_parcels = {140: [2, 4, "A-Team"]}
delivered_parcels = {141: [1, 3, "B-Team"],
                     143: [3, 1, "B-Team"]}
positions = {"A-Team": [1, 2],
             "B-Team": [3, 3]}

# TODO: ghost robots laten bewegen


def APICall(f):
    @wraps(f)
    def cross_origin_headers(*args, **kwargs):
        ans = make_response(f(*args, **kwargs))
        h = ans.headers
        h["Access-Control-Allow-Origin"] = 'http://127.0.0.1:4848'
        h["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
        h["Access-Control-Request-Headers"] = "Content-Type, Origin, Cache-Control"
        #h["Access-Control-Allow-Credentials"] = 'true'
        return ans
    return cross_origin_headers


@app.route('/robots/<team>', methods=['POST'])
@cross_origin()
def register(team):
    try:
        print request.data
        if secret_keys.get(team) is not None:
            return "SORRY"
        secret_keys[team] = int(request.data, 16)
        print secret_keys
        return "OK"
    except ValueError:
        return "SORRY"


@app.route('/robots/<team>/<secret_key>', methods=['DELETE'])
@cross_origin()
def delete(team, secret_key):
    try:
        if secret_keys[team] == int(secret_key, 16):
            del secret_keys[team]
            return "OK"
        return "SORRY"
    except:
        return "SORRY"


@app.route('/map', methods=['GET'])
@cross_origin()
def get_map():
    route_map = {"verticles": [
                    [1, {"origin": 3, "straight": 2}],
                    [2, {"origin": 1, "straight": 3}],
                    [3, {"origin": 2, "straight": 1, "left": 4}],
                    [4, {"origin": 3, "straight": 1, "left": 2}]
                ],
                "edges":[
                    [1, 2, 0.3],
                    [1, 3, 0.5],
                    [3, 1, 0.5],
                    [2, 3, 0.1],
                    [3, 2, 0.1],
                    [3, 4, 0.7],
                    [4, 2, 0.3],
                    [4, 1, 0.8]
                ]
    }
    return jsonify(route_map)


@app.route('/parcels', methods=['GET'])
@cross_origin()
def get_parcels():
    return jsonify({"available-parcels": [[nb] + available_parcels[nb] for nb in available_parcels.keys()],
                    "on-the-road-parcels": [[nb] + on_the_road_parcels[nb] for nb in on_the_road_parcels.keys()],
                    "delivered-parcels": [[nb] + delivered_parcels[nb] for nb in delivered_parcels.keys()]})


@app.route('/robots/<team>/claim/<parcel_nb>', methods=['PUT'])
@cross_origin()
def claim(team, parcel_nb):
    try:
        parcel_nb = int(parcel_nb)
        if int(request.data, 16) == secret_keys[team]:
            parcel = available_parcels.pop(parcel_nb, None)
            if parcel is not None:
                parcel.append(team)
                on_the_road_parcels[parcel_nb] = parcel
                return "OK"
        return "SORRY"
    except:
        return "SORRY"


@app.route('/robots/<team>/delivered/<parcel_nb>', methods=['PUT'])
@cross_origin()
def deliver(team, parcel_nb):
    try:
        parcel_nb = int(parcel_nb)
        if int(request.data, 16) == secret_keys[team]:
            parcel = on_the_road_parcels.pop(parcel_nb, None)
            if parcel is not None and parcel[2] == team:
                delivered_parcels[parcel_nb] = parcel
                return "OK"
        return "SORRY"
    except:
        return "SORRY"


@app.route('/positions/<team>/<from_node>/<to_node>', methods=['PUT'])
@cross_origin()
def set_position(team, from_node, to_node):
    try:
        if int(request.data, 16) == secret_keys[team]:
            positions[team] = [from_node, to_node]
            return "OK"
        return "SORRY"
    except:
        return "SORRY"


@app.route('/positions', methods=['GET'])
@cross_origin()
def get_position():
    return jsonify({"positions": [[team] + positions[team] for team in positions.keys()]})


if __name__ == "__main__":
    app.run(host='0.0.0.0')