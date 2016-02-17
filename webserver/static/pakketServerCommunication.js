/**
 * Created by Thomas on 11/02/2016.
 */
var pakketUrl = "http://127.0.0.1:5000";
var teamName = "zilver";

var road_map = null;
var parcels;
var positions;
var call_succes;

var call = function (dataToSend, doOnSuccess, url, method) {
    doOnSuccess = doOnSuccess || function () {
        };

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": url,
        "method": method,
        "headers": {
            "content-type": "application/json",
            "origin": "http//127.0.0.14848",
            "cache-control": "no-cache"
        },
        "processData": false,
        "data": dataToSend
    };

    $.ajax(settings).done(function (response) {
        console.log(response);
        doOnSuccess(response);
    });
};

var register = function(secret_key){
    call(secret_key, function(data){
        //window.alert(data);
    }, pakketUrl + "/robots/" + teamName, 'POST');
};

var unregister = function(secret_key){
    call(null, function(data){
        //window.alert(data);
    }, pakketUrl + "/robots/" + teamName +"/"+secret_key, 'DELETE');
};

var get_map = function(){
    call(null, function(data){
        road_map = data;
        //console.log(road_map);
        drawData()
    }, pakketUrl + "/map", 'GET');
};

var get_parcels = function(){
    call(null, function(data){
        parcels = data
    }, pakketUrl + "/parcels", 'GET');
};

var claim = function(nb, secret_key){
  call(secret_key, function(data){}, pakketUrl + "/robots/" + teamName + "/claim/"+ nb, 'PUT');
};

var deliver = function(nb, secret_key){
    call(secret_key, function(data){}, pakketUrl + "/robots/" + teamName + "/delivered/"+ nb, 'PUT');
};

var set_position = function(from_node, to_node, secret_key){
    call(secret_key, function(data){}, pakketUrl + "/positions/" + teamName + "/" +from_node +"/"+ to_node, 'PUT');
};

var get_positions = function(){
    call(null, function(data){
        positions = data.positions;
        drawLabels();
    }, pakketUrl + "/positions", 'GET');
};

var make_secret_key = function()
{
    var text = "";
    var possible = "abcdef0123456789";

    for( var i=0; i < 10; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
};