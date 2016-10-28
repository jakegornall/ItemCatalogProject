function accessTokenToServer(access_token) {
    var url = "/login"
    $.ajax({
        type: "POST",
        url: url,
        processData: false,
        contentType: "application/octet-stream; charset=utf-8",
        data: access_token,
        dataType: "json",
        success: function(response) {
            if (response.success) {
                var state = response.state;
                var userID = response.userID;
                console.log(response.message)
                $('#to-profile-link').attr("href", "/" + userID + "/profile?state=" + state);
                $('#to-account-settings-link').attr("href", "/" + userID + "/userSettings?state=" + state);
            } else if (response.success) {
                console.log(response.message)
            } else {
                console.log("Invalid Response From Server.")
            }
        },
        failure: function() {
            console.log("failed to send user info to server.")
        }
    });
}


function logOut() {
    $('#login-button').show();
    $('#signup-button').show();
    $('#user-settings-button').hide();
    $('#user-settings-menu').attr('style', 'display: none');
    $.ajax({
        url: "/fbdisconnect",
        type: "POST",
        success: function(response) {
            console.log(response)
        },
        failure: function() {
            console.log("error occurred while logging out.")
        }
    });
}


function loggedIn(FBauthResponse) {
    $('#login-button').hide();
    $('#signup-button').hide();
    console.log(FBauthResponse)
    FB.api('/' + FBauthResponse.userID, function(response) {
        $('#user-settings-button').html('Welcome, ' + response.name + '!');
        $('#user-settings-button').show();
        accessTokenToServer(FBauthResponse.accessToken);
    });
}


function statusChangeCallback(response) {
    var FBstatus = response.status;
    var FBauthResponse = response.authResponse;
    if (FBstatus === 'connected') {
        loggedIn(FBauthResponse);
    } else if (FBstatus === 'not_authorized') {
        logOut();
        console.log('MyShop.com is not authorized to access your Facebook information.')
    } else {
        logOut();
        console.log('user not connected to Facebook.')
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
        appId      : '331293527223662',
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