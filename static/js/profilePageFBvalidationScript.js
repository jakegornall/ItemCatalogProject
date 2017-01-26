function loggedIn(FBauthResponse) {
    $('#login-button').hide();
    $('#signup-button').hide();
    FB.api('/' + FBauthResponse.userID, function(response) {
        $('#user-settings-button').html('Welcome, ' + response.name + '!');
        $('#user-settings-button').show();
    });
}


function statusChangeCallback(response) {
    var FBstatus = response.status;
    var FBauthResponse = response.authResponse;
    if (FBstatus === 'connected') {
        loggedIn(FBauthResponse);
    } else {
    	window.location = "/"
    }
}

// checks login status after user clicks #fb-login-button.
function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}


// facebook sdk
window.fbAsyncInit = function() {
    FB.init({
        appId      : '382930878726593',
        cookie     : true,
        xfbml      : true,
        version    : 'v2.8'
    });
    FB.AppEvents.logPageView();
    // fetches users facbook login status.
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
  };

(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));