/**
 * The editor controls tab-specific functions. It receives commands from the background page.
 * Functions starting with underscore(_) are not callable by the api. They are helper-functions only.
*/
var zoomLevel = .25;
//set current zoom level on load
var currentZoom = parseInt($('body').css('zoom'));
//stores last text input object. Used to enter text and submit forms.
var lastEditedInput = null;

/**
 * from https://css-tricks.com/snippets/jquery/make-jquery-contains-case-insensitive/
 * Caps-insensitive contains method
 */
$.expr[":"].containsci = $.expr.createPseudo(function(arg) {
  return function( elem ) {
    return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
  };
});

/**
 * Called from the background page to call a function.
 */
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (typeof window[request.func] == 'function') {
      window[request.func].apply(null, request.params);
      sendResponse({msg: "success"});
    } else {
      sendResponse({msg: "error"});
    }   
  });

function scrollDown(num){
  if (num == undefined) {
    num = 1;
  }
  var current = $(document).scrollTop();
  var dest = current + ($(window).height())*num;
  _scrollVertical(dest);
}

function scrollUp(num){
  if (num == undefined) {
    num = 1;
  }
  var current = $(document).scrollTop();
  var dest = current - ($(window).height())*num;
  _scrollVertical(dest);
}

function scrollLeft(){
  var current = $(document).scrollLeft();
  var dest = current - $(window).width();
  _scrollHorizontal(dest);
}

function scrollRight(){
  var current = $(document).scrollLeft();
  var dest = current + $(window).width();
  _scrollHorizontal(dest);
}

function refresh(){
  location.reload();
}

function backwardPage(){
  parent.history.back();
}

function forwardPage(){
  parent.history.forward();
}

/**
 * Zooms in by the given amount additively.
 * @param amount The % to zoom in.
 */
function zoomIn(amount){
  console.log(amount);
  if (context == "D") {
    var tb = $("viewer-toolbar");
  } else {
    var dec_amount = amount / 100;
    _setZoom(currentZoom + dec_amount);
  }
}

/**
 * Zooms out by the given amount additively.
 * @param amount The % to zoom out.
 */
function zoomOut(amount, context){
  if (context == "D") {
    //alert($("#zoom-out-button").find("div").attr("id"));
  } else {
    var dec_amount = amount / 100;
    _setZoom(currentZoom - dec_amount);
  }
}

/**
 * Click an object on the current page.
 * <a> objects are given priority over <div> objects.
 * @param str The string to search for in the object text.
 */
function click(str){
  var b = $("a:containsci("+str+")").first();
  if(b[0] == undefined){
    //only check direct text for matches, not the children's text.
    b = $("div:containsci("+str+")").filter(function() {
      return (
      $(this).clone() //clone the element
      .children() //select all the children
      .remove() //remove all the children
      .end() //again go back to selected element
      .filter(":containsci("+str+")").length > 0)
    });
  } 
    b[0].click();
}

/**
 * Set the value of the last edited input to the given string.
 * @param str The string to input.
 */
function enterText(str){
  lastEditedInput.val(str);
}

/**
 * Select and element by name.
 * Name is searched for in element placeholder and title.
 * @param name The name to search for in the input identifier.
 */
function selectElement(name){
  var re =  RegExp(name ,"i"); 
  var e;
  e = $("input[placeholder]").filter(function() {
   return re.test(this.placeholder);
  }).first();

  if (e.val() == undefined) {
    e = $("input[title]").filter(function() {
      return re.test(this.title);
    }).first();
  }
  if (e.val() != undefined){
    lastEditedInput = e;
    e.focus();
  }
}

/**
 * Submits the form containing the last edited input.
 */
function submitText(){
  if (lastEditedInput != null) {
    lastEditedInput.closest('form').submit();
  }
}

/**
 * Plays the topmost visible video.
 */
function playVideo(){
  var doc = $(window).scrollTop();
  $("button[aria-label='Play']").each(function(){
    var relative = $(this).offset().top - doc;
    if (relative > 0) {
      $(this).click();
      return false;
    }
  });
}

/**
 * Pauses the topmost visible video.
 */
function pauseVideo(){
  var doc = $(window).scrollTop();
  $("button[aria-label='Pause']").each(function(){
    var relative = $(this).offset().top - doc;
    if (relative > 0) {
      $(this).click();
      return false;
    }
  });
}

/**
 * Loads the next video in the topmost visible video frame.
 */
function nextVideo(){
  var doc = $(window).scrollTop();
  $("a[title='Next']").each(function(){
    var relative = $(this).offset().top - doc;
    if (relative > 0) {
      window.location.href = $(this).attr("href");
      return false;
    }
  });
}

/**
 * Sets the topmost visible video fullscreen.
 */
function openFullscreen(){
  var doc = $(window).scrollTop();
  $("button[title='Full screen']").each(function(){
    var relative = $(this).offset().top - doc;
    if(relative > 0){
      $(this).click();
      return false;
    }
  });
}

/**
 * Sets the current fullscreen video to normal.
 */
function closeFullscreen(){
  var doc = $(window).scrollTop();
  $("button[title='Exit full screen']").each(function(){
    var relative = $(this).offset().top - doc;
    if (relative > 0) {
      $(this).click();
      return false;
    }
  });
}

/**
 * Play currently selected music.
 */
function playMusic(is_spotify){
  var is_spotify = _getBool(is_spotify);
  if (is_spotify) {
    var frame = $("#app-player");
    var contents = frame.contents();
    var btn = contents.find("button[id='play-pause']");
    btn.click();
  } else {
    $(".playButton").click();
  }
}

/**
 * Pause currently selected music.
 */
function pauseMusic(is_spotify){
  var is_spotify = _getBool(is_spotify);
  if (is_spotify) {
    var frame = $("#app-player");
    var contents = frame.contents();
    var btn = contents.find("button[id='play-pause']");
    btn.click();
  } else {
    $(".pauseButton").click();
  }
}

/**
 * Plays the next song in the current playlist.
 */
function nextSong(is_spotify){
  var is_spotify = _getBool(is_spotify);
  if (is_spotify) {
    var frame = $("#app-player");
    var contents = frame.contents();
    var btn = contents.find("button[id='next']");
    btn.click();
  } else {
    $(".skipButton").click();
  }
}

/**
 * Returns true if the given string is valid artist input.
 * @param str The string to check.
 */
function _isValidArtistInfo(str) {
  return str != undefined && typeof(str) == "string" && str.length > 0;
}

/**
 * Searches spotify for the specified artist.
 * @param artist The artist name.
 */
function _doArtistSearch(artist) {
  if (!_isValidArtistInfo(artist)) {
    return;
  }
  $.get( "https://api.spotify.com/v1/search?q="+artist+"&type=artist&limit=1", function( data ) {
    window.location.href = data["artists"]["items"][0]["external_urls"]["spotify"];
  });
}

/**
 * Searches spotify for the specified album.
 * @param album The album name.
 */
function _doAlbumSearch(album) {
  if (!_isValidArtistInfo(album)) {
    return;
  }
  $.get( "https://api.spotify.com/v1/search?q="+album+"&type=album&limit=1", function( data ) {
    window.location.href = data["albums"]["items"][0]["external_urls"]["spotify"];
  });
}

/**
 * Searches spotify for the specified song.
 * @param song The song name.
 */
function _doSongSearch(song) {
  if (!_isValidArtistInfo(song)) {
    return;
  }
  $.get( "https://api.spotify.com/v1/search?q="+song+"&type=track&limit=1", function( data ) {
    window.location.href = data["tracks"]["items"][0]["external_urls"]["spotify"];
  });
}

/**
 * Searches spotify for the a song which matches the specified artist/album/song.
 * @param artist The artist name.
 * @param album The album name.
 * @param song The song name.
 */
function _doArtistInfoSearch(artist, album, song) {
  var query = "https://api.spotify.com/v1/search?q=";
  if (_isValidArtistInfo(artist)) { query += "artist:"+artist; }
  if (_isValidArtistInfo(album)) { query += "%20album:"+album; }
  if (_isValidArtistInfo(song)) { query += "%20track:"+song; }
  query += "&type=track&limit=1";
  $.get(query, function( data ) {
    window.location.href = data["tracks"]["items"][0]["external_urls"]["spotify"];
  });
}

/**
 * Search music for the given type.
 * @param is_spotify True if current site is spotify
 * @param artist The artist name.
 * @param album The album name.
 * @param song The song name.
 * @param type The result type, "artist", "album", or "song".
 */
function searchMusic(is_spotify, artist, album, song, type){
  var is_spotify = _getBool(is_spotify);
  if(is_spotify){
    if (type=="artist"){
      _doArtistSearch(artist);
    } else if (type == "album") {
      _doAlbumSearch(album);
    } else if (type == "song") {
      _doSongSearch(song);
    } else {
      _doArtistInfoSearch(artist, album, song);
    }
  } else{
      window.location.href = "http://www.pandora.com/search/" + [artist, album, song].join(" ").trim();
  }
}

/**
 * Goes to specified page in the pdf.
 * @param num The page number.
 */
function goToPage(num){
  window.location.href = window.location.href.split("#page")[0]+"#page="+num;
  window.location.reload(true);
}

function _setZoom(z){
  $('body').css('zoom', z.toString());
  currentZoom = z;
}

function _scrollHorizontal(dest){
  $('html, body').animate({
    scrollLeft: dest
  }, 1000);
}

function _scrollVertical(dest){
  $('html, body').animate({
    scrollTop: dest
  }, 1000);
}

/**
 * Create a text box which displays the given string. Fades out quickly.
 * @param str The string to display.
 */
function _addMessage(str){
  $('<div id="WebJargonInfo" style="position:fixed;color:white;background-color:black;right:5px;top:55px;width:100px;height:60px;z-index:1000;">'+str+'</div>').appendTo('html');
  $("#WebJargonInfo").fadeOut(2000, function(){
    $("#WebJargonInfo").remove();
  });
}

function _getBool(str){
  var bool = (str === "true");
  return bool;
}
