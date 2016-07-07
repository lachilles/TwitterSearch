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

        $(".tweet").append(
            '<td>' + createdAt + '</td>' +
            '<td>' + user + '</td>' +
            '<td>' + tweet_text + '</td>' +
            '<td>' + favoriteCount + '</td></tr>'
            );
        // $(".user").append();
        // $(".text").append();
        // $(".favorite").append();
    });
    // var arrayLength = actualResults.length;
    // for (var i = 0; i < arrayLength; i++) {
    //     // alert(actualResults[i]);
    //     //Do something
    //     var createdAt = actualResults.created_at;
    //     var tweet_text = actualResults.tweet_text;
    //     var user = actualResults.user;
    //     var favoriteCount = actualResults.favorite_count;
    //     var hashtags = actualResults.hashtags;
        
    // //     console.log(createdAt);
    // //     console.log(tweet_text);
    // //     console.log(user);
    // //     console.log(favoriteCount);
    // //     console.log(hashtags);

    //     $(".created_at").append(this.createdAt);
    //     $(".user").append(this.user);
    //     $(".text").append(this.tweet_text);
    //     $(".favorite").append(this.favoriteCount);
    // // }
}

// Output:
// "obj.a = 1"
// "obj.b = 2"
// "obj.c = 3"

    // var keyword = actualResults.prop.current_keyword;


//     console.log("keyword: " + keyword);
//     console.log("createdAt: " + createdAt);
//     console.log("tweet_text: " + tweet_text);
//     console.log("Made it to showSearchResults");
//     $(".created_at").append(this.createdAt);
//     $(".user").append(this.user);
//     $(".text").append(this.tweet_text);
//     $(".favorite").append(this.favoriteCount);
// }


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
