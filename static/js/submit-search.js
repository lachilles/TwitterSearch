
"use strict";

// ***************Show search results****************************

// build function that displays/shows the current search that was sent through submit button

function showSearchResults(result) {  //the result being passed in are the ones I set in my route
    // alert(result);
    console.log("Made it to showSearchResults");

    $(".created_at").empty();
    $(".user").empty();
    $(".text").empty();
    $(".favorite").empty();

    // Need to figure out how to grab following variables from json

    console.log(result);

    var actualResults = result.result;
    console.log(actualResults);
    

//     for (var j = 0; j < myArray.length; j++){

//     console.log(myArray[j.x]);

// }
//     yourArray.forEach( function (arrayItem)
// {
//     var x = arrayItem.prop1 + 2;
//     alert(x);
// });
    
    actualResults.forEach( function (i)
    {
        var createdAt = i.created_at;
        var tweet_text = i.tweet_text;
        var user = i.user;
        var favoriteCount = i.favorite_count;
        var hashtags = i.hashtags;
        console.log(hashtags);

        // $(".tweet").append(
        //     '<td>' + createdAt + '</td>' 
        //     );
        $(".table-striped").append(
            '<tr><td>' + createdAt + '</td>' +
            '<td>' + user + '</td>' +
            '<td>' + tweet_text + '</td>' +
            '<td>' + favoriteCount + '</td></tr>'

            );

    });

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
