function login(website, username, password) {
    console.log(website);
    console.log(username);
    console.log(password);

    $.postDigest(website, {
        username: username,
        password: password
    }).done(function(data, textStatus, xhr) {
        alert('LOGIN SUCCESSS');
        window.close();
    }).fail(function(xhr, textStatus, errorThrown) {
        alert('LOGIN FAIL');
        window.close();
    });
}

function onInit () {
    console.log("onInit");
    var website = location.href + "login/";
    var username = "foo";
    var password = "bar";
    login(website, username, password);
}


$(function(){
    onInit ();
    //document.addEventListener('DOMContentLoaded', onInit, false);
});
