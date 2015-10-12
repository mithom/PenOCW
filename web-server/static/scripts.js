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
};

var stopUp = function() {
    document.getElementById("upA").id = "upB";
    var a = $.ajax({url:'/fun', type: "POST", dataType:"json", contentType:'application/json; charset-utf-8', data:JSON.stringify({a: true,b:6}), success:function(data){alert(data);}});
};

var doDown = function(){
    document.getElementById("downB").id = "downA";
};

var stopDown = function() {
    document.getElementById("downA").id = "downB";
};

var doLeft = function(){
    document.getElementById("leftB").id = "leftA";
};

var stopLeft = function() {
    document.getElementById("leftA").id = "leftB";
};

var doRight = function(){
    document.getElementById("rightB").id = "rightA";
};

var stopRight = function() {
    document.getElementById("rightA").id = "rightB";
};



/*document.addEventListener('mousedown',function(){
    alert('hello world!');
});*/

/*$('#upKey').click(function(){
    alert('hello world!')
});*/

document.addEventListener('keydown',a,false);
document.addEventListener('keyup', b, false);

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            //hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    //document.body.appendChildfuncid(form);
    form.submit();
}