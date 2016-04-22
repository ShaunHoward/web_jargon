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

/**
 * Calls a function in the backgroud page.
 */
function _callBackgroundFunction(cmd, params) {
  chrome.runtime.sendMessage({func: cmd, params: params}, function(response) {
    if(response && response.msg){
      return response.msg;
    }
  });
}

// https://ctrlq.org/code/19797-regex-youtube-id
function _extractVideoID(url){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
    var match = url.match(regExp);
    if (match && match[7].length == 11){
        return match[7];
    }
    return ""
}

/**
 * Opens a new youtube page with the video as fullscreen.
 */
function _openYoutubeFullscreen() {
  // store the embedded player prefix for substring checking
  var embed_prefix = "http://www.youtube.com/embed/";
  // get the current web page url
  var curr_url = window.location.href;
  // extract the video id from the url
  var video_id = _extractVideoID(curr_url);

  // open maximized almost full-screen player if not already in maximized mode
  if (video_id != "" && curr_url.indexOf(embed_prefix) == -1) {
    // create fullscreen url with autoplay
    fullscreen_url = embed_prefix + video_id + "?autoplay=1";
    // print url to console
    _callBackgroundFunction("_printConsoleMessage", [fullscreen_url]);
    // open the fullscreen url in the current open tab
    _callBackgroundFunction("_finishOpeningURL", [fullscreen_url, true]);
    return "success";
  } else {
    return "error";
  }
}

/**
 * Returns to the normal youtube page without fullscreen.
 */
function _closeYoutubeFullscreen() {
  // define the standard-sized youtube video prefix
  var standard_prefix = "https://www.youtube.com/watch?v=";
  // get the current web page url
  var curr_url = window.location.href;
  // extract the video id from the url
  var video_id = _extractVideoID(curr_url);

  // open the standard video player page if possible
  if (video_id != "" && curr_url.indexOf(standard_prefix) == -1) {
    // create standard url for autoplay and maintaining position in video
    standard_url = standard_prefix + video_id + "?autoplay=1";
    // print url to console
    _callBackgroundFunction("_printConsoleMessage", [standard_url]);
    // open the standard url in the tab at the correct position in time
    _callBackgroundFunction("_finishOpeningURL", [standard_url, true]);
    return "success";
  } else {
    return "error";
  }
}

// set zoom level
function _setZoom(z){
  $('body').css('zoom', z.toString());
  currentZoom = z;
}

// scroll amount of pixels given to the left or right
function _scrollHorizontal(dest){
  $('html, body').animate({
    scrollLeft: dest
  }, 1000);
}

// scroll amount of pixels given up or down
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
  var m = $("#WebJargonInfo");
  if(m != undefined){
    m.remove();
  }
  $('<div id="WebJargonInfo" style="position:fixed; color:white; background-color:black; right:5px; top:55px; width:100px; height:40px; z-index:1000; text-align:center; padding-top:10px; background-color: #a5c7ef; color:black;">'+str+'</div>').appendTo('html');
  $("#WebJargonInfo").fadeOut(2000, function(){
    $("#WebJargonInfo").remove();
  });
}

// turns a string into a boolean type if possible, else returns false
function _getBool(str){
  var bool = (str === "true");
  return bool;
}

// checks if the input string is a non-empty string
function _isValidArtistInfo(str) {
  return str != undefined && typeof(str) == "string" && str.length > 0;
}

// searches spotify for specified artist
function _doArtistSearch(artist) {
  if (!_isValidArtistInfo(artist)) {
    return;
  }
  $.get( "https://api.spotify.com/v1/search?q="+artist+"&type=artist&limit=1", function( data ) {
    window.location.href = data["artists"]["items"][0]["external_urls"]["spotify"];
  });
}

// searches spotify for specified album
function _doAlbumSearch(album) {
  if (!_isValidArtistInfo(album)) {
    return;
  }
  $.get( "https://api.spotify.com/v1/search?q="+album+"&type=album&limit=1", function( data ) {
    window.location.href = data["albums"]["items"][0]["external_urls"]["spotify"];
  });
}

// searches spotify for specified song
function _doSongSearch(song) {
  if (!_isValidArtistInfo(song)) {
    return;
  }
  $.get( "https://api.spotify.com/v1/search?q="+song+"&type=track&limit=1", function( data ) {
    window.location.href = data["tracks"]["items"][0]["external_urls"]["spotify"];
  });
}

// searches spotify for specified artist, album, and/or song
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
 * Zoom the pdf document in or out, as specified, by the given amount.
 */
function _pdfZoom(zoomIn, amount) {
  // zoom only works given a page number and zoom level
  // extract current zoom info
  var curr_zoom = 100;
  // define page and zoom substrings of url
  var page_str = "#page=";
  var zoom_str = "&zoom=";
  // extract zoom level from current url, if possible
  var zoom_split = window.location.href.split(zoom_str);
  var zoom = zoom_split[1];
  // attempt to get and set the current zoom level
  if (zoom != undefined && zoom != "") {
    curr_zoom = Number(zoom);
  }
  // start the new doc url using shortest available part of current url
  var new_url = window.location.href.split(page_str)[0];
  var curr_page = 1;
  // get the page number from the url, if possible
  if (zoom_split[0].indexOf(page_str) != -1) {
    var page = zoom_split[0].substring(zoom_split[0].indexOf(page_str)+page_str.length);
    if (page != undefined && page != "") {
      curr_page = Number(page);
    }
  }
  // construct the new url including page number
  new_url = new_url + page_str + Number(curr_page);
  // calculate the zoom amount
  var new_zoom_level;
  if (zoomIn) {
    new_zoom_level = curr_zoom + amount;
  } else {
    new_zoom_level = curr_zoom - amount;
  }
  // add zoom level to the new url
  new_url = new_url + zoom_str + new_zoom_level.toString();
  // set new url and reload the page
  window.location.href = new_url;
  window.location.reload(true);
}

/**
 * Scrolls down the specified number of pages.
 */
function scrollDown(num){
  if (num == undefined) {
    num = 1;
  }
  var current = $(document).scrollTop();
  var dest = current + ($(window).height())*num;
  _scrollVertical(dest);
}

/**
 * Scrolls up the specified number of pages.
 */
function scrollUp(num){
  if (num == undefined) {
    num = 1;
  }
  var current = $(document).scrollTop();
  var dest = current - ($(window).height())*num;
  _scrollVertical(dest);
}

/**
 * Scrolls left as much as possible.
 */
function scrollLeft(){
  var current = $(document).scrollLeft();
  var dest = current - $(window).width();
  _scrollHorizontal(dest);
}

/**
 * Scrolls right as much as possible.
 */
function scrollRight(){
  var current = $(document).scrollLeft();
  var dest = current + $(window).width();
  _scrollHorizontal(dest);
}

// refresh the current page
function refresh(){
  location.reload();
}

// go back a page in the current browsing session
function backwardPage(){
  parent.history.back();
}

// go forward a page in the current browsing session
function forwardPage(){
  parent.history.forward();
}

/**
 * Zooms in by the given amount additively.
 * @param amount The % to zoom in.
 */
function zoomIn(amount, context){
  // determine whether to zoom pdf or normal web page
  var is_pdf = window.location.href.indexOf(".pdf") > -1;
  if (is_pdf) {
    _pdfZoom(true, amount);
  } else {
    var dec_amount = amount / 100;
    _setZoom(currentZoom + dec_amount);
  }
}

/**
 * Zooms out by the given amount additively.
 * @param amount The % to zoom out.
 */
function zoomOut(amount){
  // determine whether to zoom pdf or normal web page
  var is_pdf = window.location.href.indexOf(".pdf") > -1;
  if (is_pdf) {
    _pdfZoom(false, amount);
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
  str = str.trim();
  // do not match to the empty string
  if (str != "" && str.length > 0) {
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

  // try to get the input placeholder element
  e = $("input[placeholder]").filter(function() {
   return re.test(this.placeholder);
  }).first();

  // try to get the input title element
  if (e.val() == undefined) {
    e = $("input[title]").filter(function() {
      return re.test(this.title);
    }).first();
  }
  // set the element in focus if it was found
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
  var is_youtube = window.location.href.indexOf("youtube") > -1;
  if (is_youtube) {
      _openYoutubeFullscreen();
  } else {
    $("button[title='Full screen']").each(function(){
        var relative = $(this).offset().top - doc;
        if(relative > 0){
          $(this).click();
          return false;
        }
    });
  }
}

/**
 * Sets the current fullscreen video to normal.
 */
function closeFullscreen(){
  var doc = $(window).scrollTop();
  var is_youtube = window.location.href.indexOf("youtube") > -1;
  if (is_youtube) {
      _closeYoutubeFullscreen();
  } else {
    $("button[title='Exit full screen']").each(function(){
      var relative = $(this).offset().top - doc;
      if (relative > 0) {
        $(this).click();
        return false;
      }
    });
  }
}

/**
 * Plays music on either pandora or spotify
 * depending on the input parameter.
 * It is required that the media player desired is loaded as a web page.
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
 * Pause currently selected music on either spotify or pandora.
 * It is required that the media player desired is loaded as a web page.
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
 * Plays the next song in the current playlist for either pandora or spotify.
 * It is required that the media player desired is loaded as a web page.
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
function goToPage(page_number){
  if (page_number > 0) {
    var zoom_str = "&zoom=";
    var curr_url = window.location.href;
    var regex = new RegExp("#page=([0-9])+");
    var split_url = window.location.href.split(regex);
    var new_url = split_url[0] + "#page=" + page_number;
    if (split_url.length > 2) {
      new_url = new_url + split_url[2];
    }
    window.location.href = new_url;
    window.location.reload(true);
  }
}