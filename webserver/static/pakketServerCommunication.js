/**
 * Created by Thomas on 11/02/2016.
 */
var pakketUrl = "http://127.0.0.1:5000";
var teamName = "zilver";

var post = function (dataToSend, doOnSuccess, url) {
    doOnSuccess = doOnSuccess || function () {
        };
    /*return $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset-utf-8',
        data: JSON.stringify(dataToSend),
        success: doOnSuccess
    });*/

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            console.log(this.responseText);
            doOnSuccess(this.responseText)
        }
    });

    xhr.open("POST", url);
    xhr.send(data);
};

var register = function(secret_key){
    var response = post(secret_key, function(data){
        window.alert(data);
    }, pakketUrl + "/robots/" + teamName);
};

