/**
 * Created by Thomas on 05/10/2015.
 */
var manueel = null;
var beschrijving = null;
var complex = null;

var last_update = 0;
var timer = null;
var updateTime = function () {
    last_update += 0.1;
    $("#last_updated_power").text(Math.round10(last_update, -1));
};

$(document).ready(function () {
    timer = setInterval(updateTime, 1000);
    manueel = io.connect('http://' + document.domain + ':' + location.port + '/manueel');
    beschrijving = io.connect('http://' + document.domain + ':' + location.port + '/beschrijving');
    complex = io.connect('http://' + document.domain + ':' + location.port + '/complex');

    manueel.on('connect', function () {
        // window.alert('connected manueel');
        //manueel.on('alert', function(msg){window.alert("manueel meldt: " + JSON.stringify(msg));});
        manueel.on('disconnect', function () {
            window.alert('manueel disconnected')
        }); //TODO: via kleurencodering weergeven of socket verbonden is of niet en automatisch proberen te reconnecten

        manueel.on('power', function (data) {
            $("#value_power").text(data)
            if (timer != null) {
                clearInterval(timer);
                last_update = 0;
                $("#last_updated_power").text(0);
            }
            timer = setInterval(updateTime, 100);
        })
    });

    beschrijving.on('connect', function () {
        //beschrijving.on('alert', function(msg){window.alert("beschrijving meldt: " + JSON.stringify(msg));});

        beschrijving.on('updateRouteDescription', function (route) {
            var routeBody = $("#currentRoute table tbody");
            routeBody.empty();

            route.forEach(function () {
                var newRow = document.createElement('tr');
                var newName = document.createElement('td');
                var newId = document.createElement('td');
                var newIdContent = document.createTextNode('id: ' + route.id);
                var newNameContent = document.createTextNode('command: ' + route.commandName);
                newName.appendChild(newNameContent);
                newId.appendChild(newIdContent);
                newRow.appendChild(newName);
                newRow.appendChild(newId);
                routeBody.append(newRow);
            })
        });
    });

    complex.on('connect', function () {
        //complex.on('alert', function(msg){window.alert("complex meldt: " + JSON.stringify(msg));});
    });

    //here comes all the submit overrides

    $('form#line').submit(function (event) {
        complex.emit('line', {func: "line"});
        return false;
    });

    $('form#square').submit(function (event) {
        complex.emit('square', {func: "square"});
        return false;
    });

    $('form#circle').submit(function (event) {
        complex.emit('circle', {func: "circle"});
        return false;
    });

    $('form#rStart').submit(function (event) {
        beschrijving.emit('start', {});
        return false;
    });

    $('form#rLeft').submit(function (event) {
        beschrijving.emit('left', {nr: $("#NrLeft").val(), unit: $("#selectType").val()});
        return false;
    });

    $('form#rRight').submit(function (event) {
        beschrijving.emit('right', {nr: $("#NrRight").val(), unit: $("#selectType").val()});
        return false;
    });

    $('form#rStop').submit(function (event) {
        beschrijving.emit('stop', {nr: $("#NrStop").val(), unit: $("#selectType").val()});
        return false;
    });

    //here comes responses on socket calls
    //TODO: antwoorden opvangen

    var keyDown = function (e) {
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

    var keyUp = function (e) {
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
    var response = $.ajax({
        url: '/',
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset-utf-8',
        data: JSON.stringify(dataToSend),
        success: doOnSuccess
    });
    return response
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
         });*///TODO: werkt onerstaande? anders gebruik bovenstaande
        $("#video_stream > img").each(function () {
            this.remove()
        })
    }
};

var getAllfunctionsInQueue = function () {
    //TODO: implement this function
};

var cancelFunction = function (id) {
    //TODO: implement this function
};

// Closure to expand the Math module, source form: https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Math/round
(function () {//TODO: vervang heel deze code door: http://stackoverflow.com/questions/4098685/rounding-numbers-to-2-digits-after-comma
    /**
     * Decimal adjustment of a number.
     *
     * @param {String}  type  The type of adjustment.
     * @param {Number}  value The number.
     * @param {Integer} exp   The exponent (the 10 logarithm of the adjustment base).
     * @returns {Number} The adjusted value.
     */
    function decimalAdjust(type, value, exp) {
        // If the exp is undefined or zero...
        if (typeof exp === 'undefined' || +exp === 0) {
            return Math[type](value);
        }
        value = +value;
        exp = +exp;
        // If the value is not a number or the exp is not an integer...
        if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0)) {
            return NaN;
        }
        // Shift
        value = value.toString().split('e');
        value = Math[type](+(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp)));
        // Shift back
        value = value.toString().split('e');
        return +(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp));
    }

    // Decimal round
    if (!Math.round10) {
        Math.round10 = function (value, exp) {
            return decimalAdjust('round', value, exp);
        };
    }
    // Decimal floor
    if (!Math.floor10) {
        Math.floor10 = function (value, exp) {
            return decimalAdjust('floor', value, exp);
        };
    }
    // Decimal ceil
    if (!Math.ceil10) {
        Math.ceil10 = function (value, exp) {
            return decimalAdjust('ceil', value, exp);
        };
    }
})();


/*document.addEventListener('mousedown',function(){
 alert('hello world!');
 });*/

/*$('#upKey').click(function(){
 alert('hello world!')
 });*/
