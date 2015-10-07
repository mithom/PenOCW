/**
 * Created by Thomas on 05/10/2015.
 */

var a = function(e){
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

/*var b = function(){
    window.alert('hello world, you pressed the upKey botton!')
};*/

var b = function(e){
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

var upKey = 38;
var downKey = 40;
var leftKey = 37;
var rightKey = 39;

var doUp = function(){
    document.getElementById("upB").id = "upA";
}

var stopUp = function() {
    document.getElementById("upA").id = "upB";
}

var doDown = function(){
    document.getElementById("downB").id = "downA";
}

var stopDown = function() {
    document.getElementById("downA").id = "downB";
}

var doLeft = function(){
    document.getElementById("leftB").id = "leftA";
}

var stopLeft = function() {
    document.getElementById("leftA").id = "leftB";
}

var doRight = function(){
    document.getElementById("rightB").id = "rightA";
}

var stopRight = function() {
    document.getElementById("rightA").id = "rightB";
}



/*document.addEventListener('mousedown',function(){
    alert('hello world!');
});*/

/*$('#upKey').click(function(){
    alert('hello world!')
});*/

document.addEventListener('keydown',a,false);
document.addEventListener('keyup', b, false)