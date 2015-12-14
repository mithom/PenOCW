/**
 * Created by Thomas on 05/10/2015.
 */
var manueel = null;
var beschrijving = null;
var complex = null;

var heldKeys = {};
var last_update = new Date().getTime();
var timer = null;
var updateTime = function () {
    $("#last_updated_power").text(((new Date().getTime() - last_update)/1000).toFixed(1));
};

$(document).ready(function () {
    var selected = $("input[type='radio'][name='controlType']:checked").val();
    switch(selected){
        case 'manueel':
            activateManueel();
            break;
        case 'complex':
            activateComplex();
            break;
        case 'routeDescription':
            activateRouteDescription();
            break;
    }


    timer = setInterval(updateTime, 100);

    //here comes all the submit overrides

    $('form#line').submit(function () {
        complex.emit('line', {func: "line"});
        return false;
    });

    $('form#square').submit(function () {
        complex.emit('square', {func: "square"});
        return false;
    });

    $('form#circle').submit(function () {
        complex.emit('circle', {func: "circle"});
        return false;
    });

    $('form#rStart').submit(function () {
        beschrijving.emit('start', {});
        return false;
    });

    $('form#rLeft').submit(function () {
        beschrijving.emit('left', {nr: $("#NrLeft").val(), unit: $("#selectType").val()});
        return false;
    });

    $('form#rRight').submit(function () {
        beschrijving.emit('right', {nr: $("#NrRight").val(), unit: $("#selectType").val()});
        return false;
    });

    $('form#rStop').submit(function () {
        beschrijving.emit('stop', {nr: $("#NrStop").val(), unit: $("#selectType").val()});
        return false;
    });

    var keyDown = function (e) {
        if($("input[type='radio'][name='controlType']:checked").val() == 'manueel') {
            if (!(e.keyCode in heldKeys)) {
                heldKeys[e.keyCode] = true;
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
            }
        }
    };

    var keyUp = function (e) {
        delete heldKeys[e.keyCode];
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

    document.addEventListener('keydown', keyDown, false);
    document.addEventListener('keyup', keyUp, false);

});


//vanaf hier buiten document.ready()
var upKey = 38;
var downKey = 40;
var leftKey = 37;
var rightKey = 39;

var doUp = function () {
    manueel.emit("up", {status: 'active'});
    $("#up").toggleClass("active passive");
    //var response = post({function: "doUp"}, getId);
};

var stopUp = function () {
    $("#up").toggleClass("active passive");
    //var response = post({function: "stopUp"}, getId);
    manueel.emit("up", {status: 'passive'});
};

var doDown = function () {
    $("#down").toggleClass("active passive");
    //var response = post({function: "doDown"}, getId);
    manueel.emit("down", {status: 'active'});
};

var stopDown = function () {
    $("#down").toggleClass("active passive");
    //var response = post({function: "stopDown"}, getId);
    manueel.emit("down", {status: 'passive'});
};

var doLeft = function () {
    $("#left").toggleClass("active passive");
    //var response = post({function: "doLeft"}, getId);
    manueel.emit("left", {status: 'active'});
};

var stopLeft = function () {
    $("#left").toggleClass("active passive");
    //var response = post({function: "stopLeft"}, getId)
    manueel.emit("left", {status: 'passive'});
};

var doRight = function () {
    $("#right").toggleClass("active passive");
    //var result = post({function: "doRight"}, getId)
    manueel.emit("right", {status: 'active'});
};

var stopRight = function () {
    $("#right").toggleClass("active passive");
    //var result = post({function: "stopRight"}, getId);
    manueel.emit("right", {status: 'passive'});
    //window.alert(result)
    //for(var key in result){window.alert(key); window.alert(result[key]);}
    //alert(id)
};

var getId = function (response, status, xhr) {//find a way to save the id that is returned (via global list or something)
    try {
        return response.id
    } catch (err) {
        alert("an error has occured: " + err.message);
        throw err;
    }
};

var post = function (dataToSend, doOnSuccess) {
    doOnSuccess = doOnSuccess || function () {
        };
    return $.ajax({
        url: '/',
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset-utf-8',
        data: JSON.stringify(dataToSend),
        success: doOnSuccess
    });
};

var startStream = function () {
    if ($("#video_button").text() == "start stream") {
        $("#video_button").text("stop stream");
        var img = $("<img>").attr("src", Flask.url_for('video_feed')).attr("height", "120px");
        $("#video_stream").append(img)
    } else {
        $("#video_button").text("start stream");
        /*$("#video_stream img").each(function(){
         this.remove()
         });*/
        $("#video_stream > img").each(function () {
            this.remove()
        })
    }
};

var activateManueel = function(){
    $("#direct-control").removeClass('hidden');
    $("#commands").addClass('hidden');
    $("#route-input").addClass('hidden');
    $("#power_info").removeClass('hidden');
    connectManueel()
};

var activateComplex = function(){
    $("#direct-control").addClass('hidden');
    $("#commands").removeClass('hidden');
    $("#route-input").addClass('hidden');
    $("#power_info").addClass('hidden');
    connectComplex()
};

var activateRouteDescription = function(){
    $("#direct-control").addClass('hidden');
    $("#commands").addClass('hidden');
    $("#route-input").removeClass('hidden');
    $("#power_info").removeClass('hidden');
    connectRoute()
};

var connectManueel = function(){
    disconnect(complex);
    disconnect(beschrijving);
    manueel = io.connect('http://' + document.domain + ':' + location.port + '/manueel', {'forceNew': true});
    manueel.on('connect', function () {
        // window.alert('connected manueel');
        //manueel.on('alert', function(msg){window.alert("manueel meldt: " + JSON.stringify(msg));});
        manueel.on('disconnect', function () {
            //window.alert('manueel disconnected')
        }); //TODO: via kleurencodering weergeven of socket verbonden is of niet en automatisch proberen te reconnecten

        manueel.on('power', function (data) {
            $("#value_power").text(data);
            if (timer != null) {
                clearInterval(timer);
                last_update = new Date().getTime();
                $("#last_updated_power").text(0);
            }
            timer = setInterval(updateTime, 100);
        });

        manueel.on('askDisconnect', function(data){
            disconnect(manueel);//TODO: switch page
        });
    });
};
var disconnect = function(socket){
    if(socket != null){
        socket.disconnect()
    }
};

var connectComplex = function(){
    disconnect(manueel);
    disconnect(beschrijving);
    complex = io.connect('http://' + document.domain + ':' + location.port + '/complex', {'forceNew': true});

    complex.on('connect', function () {
        //complex.on('alert', function(msg){window.alert("complex meldt: " + JSON.stringify(msg));});
        complex.on('askDisconnect', function(data){
            disconnect(complex);//TODO: switch page
        });

        complex.on('disconnect', function(){
            //window.alert("complex dc")
        })
    });
};

var connectRoute = function(){
    disconnect(complex);
    disconnect(manueel);
    beschrijving = io.connect('http://' + document.domain + ':' + location.port + '/beschrijving', {'forceNew': true});
    beschrijving.on('connect', function () {
        //beschrijving.on('alert', function(msg){window.alert("beschrijving meldt: " + JSON.stringify(msg));});

        beschrijving.on('updateRouteDescription', function (...route) {// we use the arguments variable here cus we don't know how many we will get
            var routeBody = $("#currentRoute table tbody");
            routeBody.empty();

            route.forEach(function (elem) {
                var newRow = document.createElement('tr');
                var newName = document.createElement('td');
                var newId = document.createElement('td');
                var newParams = document.createElement('td');
                var newButton = document.createElement('button');
                var newIdContent = document.createTextNode('id: ' + elem.id);
                var newNameContent = document.createTextNode('command: ' + elem.commandName);
                var paramString = '';
                $.each(elem.params, function(key,val) {
                    paramString += key + ': ' + val + ', ';
                });
                var newParamsContent = document.createTextNode('params: ' + paramString);
                var newButtonText = document.createTextNode('X');
                newButton.onclick = function() {
                    //$(this).parents('tr').remove();
                    beschrijving.emit("cancel_id", {"id": function(){return elem.id;}()});
                };
                newName.appendChild(newNameContent);
                newId.appendChild(newIdContent);
                newParams.appendChild(newParamsContent);
                newButton.appendChild(newButtonText);
                newRow.appendChild(newId);
                newRow.appendChild(newName);
                newRow.appendChild(newParams);
                newRow.appendChild(newButton);
                routeBody.append(newRow);
            });
        });

        beschrijving.on('askDisconnect', function(data){
            disconnect(beschrijving);//TODO: switch page
        });

        beschrijving.emit("ask_update")
    });
};


/*document.addEventListener('mousedown',function(){
 alert('hello world!');
 });*/

/*$('#upKey').click(function(){
 alert('hello world!')
 });*/
