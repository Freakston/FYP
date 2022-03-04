/* We need to know who called this so as to get it's details from server */

var queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
var term = urlParams.get("name");

$("h1").text("Details of the job "+term);