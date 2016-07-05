"use strict";

// ***************Show search results****************************

// build function that displays/shows the current search that was sent through submit button

function showSearchResults(result) {  //the result being passed in are the ones I set in my route
    // alert(result);

    var keyword = result.current_keyword;
    var createdAt = result.created_at;
    var tweet_text = result.tweet_text;
    var user = result.user;
    var favoriteCount = result.favorite_count;
    var hashtags = result.hashtags;

    console.log(result);
    console.log(keyword);
    console.log(createdAt);
    console.log(tweet_text);
    console.log("Made it to showSearchResults");
    $(".created_at").append(this.createdAt);
    $(".user").append(this.user);
    $(".text").append(this.tweet_text);
    $(".favorite").append(this.favoriteCount);
}


function submitSearch(evt) {
    evt.preventDefault();
    var formInputs = {
        "search": $("#search-text").val()
    };
    console.log(formInputs);

    // go to this route in my app 
    // when you come back succesfully run the function showSearchResults

    $.post("/search-results.json",
           formInputs,
           showSearchResults
           );
}

// grab the elent by id search-button
// listen for click
// run submitSearch funcion

$("#search-button").on("click", submitSearch);