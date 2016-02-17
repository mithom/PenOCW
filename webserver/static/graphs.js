/**
 * Created by Thomas on 09/02/2016.
 */
//this file is supposed to handle the visualisation of the graphs
// create an array with nodes
var nodes = new vis.DataSet();
var edges = new vis.DataSet();
var secret_key;
var adjusted = {nodes : {}, edges: {}};

$(document).ready(function(){
    secret_key = make_secret_key();
    register(secret_key);
    unregister(secret_key);
    register(secret_key);
    get_map();
    get_parcels();
    //get_positions();

    //window.alert(JSON.parse(road_map));
    // create an array with nodes
    /*nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);

    // create an array with edges
    edges = new vis.DataSet([
        {id: 1, from: 1, to: 3, arrows:"to"},
        {id: 2, from: 1, to: 2, arrows:"to"},
        {id: 3, from: 2, to: 4, arrows:"to"},
        {id: 4, from: 2, to: 5, arrows:"to"},
        {id: 5, from: 5, to: 2, arrows:"to"}
    ]);*/

});


//functions to manipulate the graph (should only use update for the labels

function updateNode(id, label) {
    //try {
        nodes.update({
            id: id,
            label: nodes.get(id)['label'] + '\n' +label, //TODO: multiline wagen + knoopnaam
            font: {background: label}
        });
    //}
    /*catch (err) {
        alert(err);
    }*/
}

function updateEdge(id, label) {
    //try {
    odlLabel = edges.get(id)['label'] || '';
    if(odlLabel != ""){
        odlLabel += "\n"
    }
        edges.update({
            id: id,
            label: odlLabel + label,
            font: {background: label}
        });
    //}
    /*catch (err) {
        alert(err);
    }*/
}

var drawData = function(){
    //console.log(road_map.verticles);
    for(edge in road_map.verticles){
        nodes.add({id: road_map.verticles[edge][0], label: road_map.verticles[edge][0]});
    }
    var i = 0;
    for(edge in road_map.edges){
        edges.add({
            id: i++,
            from: road_map.edges[edge][0],
            to: road_map.edges[edge][1],
            arrows:{to:{scaleFactor:0.5}}
        });
    }
    drawMap();
};

var drawMap = function(){
    // create a network
    var container = document.getElementById('mynetwork');

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        height: '300px',
        width: '500px',
        locale: "nl",
        autoResize: true
    };

    // initialize your network!
    var network = new vis.Network(container, data, options);
};

var clearLabels = function(){
    //console.log(adjusted);
    for(idnb in adjusted.nodes){
        nodes.update({
            id: idnb,
            label : idnb
        })
    }
    for(idnb in adjusted.edges){
        edges.update({
            id: idnb,
            label: ""
        })
    }
    adjusted = {nodes : {}, edges: {}};
};

var drawLabels = function(){
    clearLabels();
    for(pos in positions){
        var team = positions[pos][0];
        var from = positions[pos][1];
        var to = positions[pos][2];
        if(from != to){
            var id = findEdge(from, to);
            adjusted.edges[id]= true;
            updateEdge(id,team);
        }else {
            updateNode(from, team);
            adjusted.nodes[from]= true;
        }
    }
};

var findEdge = function(from, to){
    for(var i =0; i< edges.length;i++){
        if(edges.get(i)["from"] == from && edges.get(i)["to"] == to){
            return edges.get(i)["id"];
        }
    }
};