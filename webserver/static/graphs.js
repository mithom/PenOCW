/**
 * Created by Thomas on 09/02/2016.
 */
//this file is supposed to handle the visualisation of the graphs
// create an array with nodes
var nodes
var edges
$(document).ready(function(){
    register(123456789);
    // create an array with nodes
    nodes = new vis.DataSet([
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
    ]);

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
});


//functions to manipulate the graph (should only use update for the labels
function addNode() {
    try {
        nodes.add({
            id: document.getElementById('node-id').value,
            label: document.getElementById('node-label').value
        });
    }
    catch (err) {
        alert(err);
    }
}

function updateNode() {
    try {
        nodes.update({
            id: document.getElementById('node-id').value,
            label: document.getElementById('node-label').value
        });
    }
    catch (err) {
        alert(err);
    }
}
function removeNode() {
    try {
        nodes.remove({id: document.getElementById('node-id').value});
    }
    catch (err) {
        alert(err);
    }
}

function addEdge() {
    try {
        edges.add({
            id: document.getElementById('edge-id').value,
            from: document.getElementById('edge-from').value,
            to: document.getElementById('edge-to').value
        });
    }
    catch (err) {
        alert(err);
    }
}
function updateEdge() {
    try {
        edges.update({
            id: document.getElementById('edge-id').value,
            from: document.getElementById('edge-from').value,
            to: document.getElementById('edge-to').value
        });
    }
    catch (err) {
        alert(err);
    }
}
function removeEdge() {
    try {
        edges.remove({id: document.getElementById('edge-id').value});
    }
    catch (err) {
        alert(err);
    }
}
