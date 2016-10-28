// fetches on clearance and on sale items from API every 7 seconds.
var pastClearanceResults = [];
var pastSaleResults = [];
function ItemRefresh() {
    $.ajax({
        type: "GET",
        url: "/clearanceItemsAPI",
        dataType: "json",
        success: function (response) {
            var results = response["results"];
            $("#loader-CI").attr("style", "display: none");
            for (i = 0; i < results.length; i++) {
                if (pastClearanceResults.indexOf(results[i]["id"]) === -1) {
                    $("#clearanceItemsContainer").append(
                        "<div class='col-md-4 clearance-item' style='max-width: 200px'><img src='" + results[i]["imageURL"] + "' class='img-responsive'><h2>" + results[i]["name"] + "</h2><h4>" + results[i]["price"] + "</h4></div>"
                    );
                    pastClearanceResults.push(results[i]["id"]);
                }
            }
        },
        error: function (errorThrown) {
            $("#loader-CI").attr("style", "display: none");
            console.log(errorThrown);
            $("#clearanceItemsContainer").html("Clearance Items Unavailable");
        }
    });
    // fetches on sale items from API every 7 seconds.
    $.ajax({
        type: "GET",
        url: "/saleItemsAPI",
        dataType: "json",
        success: function (response) {
            var results = response["results"];
            $("#loader-SI").attr("style", "display: none");
            for (i = 0; i < results.length; i++) {
                if (pastSaleResults.indexOf(results[i]["id"]) === -1) {
                    $("#saleItemsContainer").append(
                        "<div class='col-md-4 clearance-item' style='max-width: 200px'><img src='" + results[i]["imageURL"] + "' class='img-responsive'><h2>" + results[i]["name"] + "</h2><h4>" + results[i]["price"] + "</h4></div>"
                    );
                    pastSaleResults.push(results[i]["id"]);
                }
            }
        },
        error: function (errorThrown) {
            $("#loader-SI").attr("style", "display: none");
            console.log(errorThrown);
            $("#saleItemsContainer").html("Clearance Items Unavailable");
        }
    });
}
ItemRefresh();
setInterval(function () {
    ItemRefresh()
    }, 5000);