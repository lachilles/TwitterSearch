"use strict";

function showSearchResults(result) {
    alert(result);
    console.log("Made it to showSearchResults")
}

function submitSearch(evt) {
    evt.preventDefault();

    var formInputs = {
        "search": $("#search-box").val()
    };

    $.post("/search-results.json/",
           formInputs,
           showSearchResults
           );
}

$("#search-box").on("submit", submitSearch);