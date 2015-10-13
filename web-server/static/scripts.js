/**
 * Created by Thomas on 05/10/2015.
 */

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
    document.getElementById("upB").id = "upA";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "doUp"}), success:function(data){alert(JSON.parse(data));}});
};

var stopUp = function() {
    document.getElementById("upA").id = "upB";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "stopUp"}), success:function(data){alert(JSON.parse(data));}});
};

var doDown = function(){
    document.getElementById("downB").id = "downA";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "doDown"}), success:function(data){alert(JSON.parse(data));}});
};

var stopDown = function() {
    document.getElementById("downA").id = "downB";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "stopDown"}), success:function(data){alert(JSON.parse(data));}});
};

var doLeft = function(){
    document.getElementById("leftB").id = "leftA";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "doLeft"}), success:function(data){alert(JSON.parse(data));}});
};

var stopLeft = function() {
    document.getElementById("leftA").id = "leftB";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "stopLeft"}), success:function(data){alert(JSON.parse(data));}});
};

var doRight = function(){
    document.getElementById("rightB").id = "rightA";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "doRight"}), success:function(data){alert(JSON.parse(data));}});
};

var stopRight = function() {
    document.getElementById("rightA").id = "rightB";
    var response = $.ajax({url:'/', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({function: "stopRight"}), success:function(data){alert(JSON.parse(data));}});
};



/*document.addEventListener('mousedown',function(){
    alert('hello world!');
});*/

/*$('#upKey').click(function(){
    alert('hello world!')
});*/
