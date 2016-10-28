// displays and hides user settings drop down menu on click.
$('#user-settings-button').click(function() {
    if ($('#user-settings-menu').css('display') == 'block') {
        $('#user-settings-menu').attr('style', 'display: none');
    } else {
        $('#user-settings-menu').attr('style', 'display: block');
    }
});