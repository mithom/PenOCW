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


var upKey = 38;
var downKey = 40;
var leftKey = 37;
var rightKey = 39;

var doUp = function(){
    window.alert("up")
}

var doDown = function(){
    window.alert("down")
}

var doLeft = function(){
    window.alert("left")
}

var doRight = function(){
    window.alert("right")
}



/*document.addEventListener('mousedown',function(){
    alert('hello world!');
});*/

/*$('#upKey').click(function(){
    alert('hello world!')
});*/

document.addEventListener('keydown',a,false);