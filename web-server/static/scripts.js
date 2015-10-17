/**
 * Created by Thomas on 05/10/2015.
 */
var socket
$(document).ready(function(){
    //TODO: script on startup})
    manueel = io.connect('http://' + document.domain + ':' + location.port + '/manueel');
    beschrijving = io.connect('http://' + document.domain + ':' + location.port + '/beschrijving');
    complex = io.connect('http://' + document.domain + ':' + location.port + '/complex');

    manueel.on('alert', function(msg){window.alert("manueel meldt: " + JSON.stringify(msg));});
    beschrijving.on('alert', function(msg){window.alert("beschrijving meldt: " + JSON.stringify(msg));});
    complex.on('alert', function(msg){window.alert("complex meldt: " + JSON.stringify(msg));});


    //here comes all the submit overrides

    $('form#line').submit(function(event) {
        complex.emit('line', {func:"line"});
        return false;
    });

    $('form#square').submit(function(event) {
        complex.emit('square', {func:"square"});
        return false;
    });

    $('form#circle').submit(function(event) {
        complex.emit('circle', {func:"circle"});
        return false;
    });
});

var keyDown = function(e){
    switch (e.keyCode) {
        case upKey:
            doUp();
            break;
        case downKey:
            doDown();
            break;
        case leftKey:
            doLeft();
            break;
        case rightKey:
            doRight();
            break;
    }
};

var keyUp = function(e){
    switch (e.keyCode) {
        case upKey:
            stopUp();
            break;
        case downKey:
            stopDown();
            break;
        case leftKey:
            stopLeft();
            break;
        case rightKey:
            stopRight();
            break;
    }
};

document.addEventListener('keydown',keyDown,false);
document.addEventListener('keyup', keyUp, false);

var upKey = 38;
var downKey = 40;
var leftKey = 37;
var rightKey = 39;

var doUp = function(){
    //socket.emit("manual driving",{function: "doUp"});
    $("#up").toggleClass("active passive");
    var response = post({function: "doUp"}, getId);
};

var stopUp = function() {
    $("#up").toggleClass("active passive");
    var response = post({function: "stopUp"}, getId);
};

var doDown = function(){
    $("#down").toggleClass("active passive");
    var response = post({function: "doDown"}, getId);
};

var stopDown = function() {
    $("#down").toggleClass("active passive");
    var response = post({function: "stopDown"}, getId);
};

var doLeft = function(){
    $("#left").toggleClass("active passive");
    var response = post({function: "doLeft"}, getId);
};

var stopLeft = function() {
    $("#left").toggleClass("active passive");
    var response = post({function: "stopLeft"}, getId)
};

var doRight = function(){
    $("#right").toggleClass("active passive");
    var result = post({function: "doRight"}, getId)
};

var stopRight = function() {
    $("#right").toggleClass("active passive");
    var result = post({function: "stopRight"}, getId);
    //window.alert(result)
    //for(var key in result){window.alert(key); window.alert(result[key]);}
    //alert(id)
};

var getId = function(response, status, xhr){//find a way to save the id that is returned (via global list or something)
    try{
        return response.id
    }catch(err){
        alert("an error has occured: " + err.message);
        throw err;
    }
};

var post = function(dataToSend, doOnSuccess){
    doOnSuccess = doOnSuccess || function(){};
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify(dataToSend), success:doOnSuccess});
    return response
};

var startStream = function(){
    if($("#video_button").text() == "start stream") {
        $("#video_button").text("stop stream");
        var img = $("<img>").attr("src", Flask.url_for('video_feed'));
        $("#video_stream").append(img)
    }else{
        $("#video_button").text("start stream");
        /*$("#video_stream img").each(function(){
            this.remove()
        });*///TODO: werkt onerstaande? anders gebruik bovenstaande
        $("#video_stream > img").each(function(){this.remove()})
    }
};

var getAllfunctionsInQueue = function(){
    //TODO: implement this function
};

var cancelFunction = function(id){
    //TODO: implement this function
};


/*document.addEventListener('mousedown',function(){
    alert('hello world!');
});*/

/*$('#upKey').click(function(){
    alert('hello world!')
});*/
