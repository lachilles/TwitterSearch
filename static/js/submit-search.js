"use strict";

function showSearchResults(result) {
    alert(result);
    console.log("Made it to showSearchResults")
}

function submitSearch(evt) {
    evt.preventDefault();
    var formInputs = {
        "search": $("#search-text").val()
    };
    console.log(formInputs);

    $.get("/search-results.json",
           formInputs,
           showSearchResults
           );
}
$("#search-button").on("click", submitSearch);

// $("#tweet-data-div").html(result);