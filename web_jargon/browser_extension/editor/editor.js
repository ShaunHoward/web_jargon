/**
The editor controls tab-specific functions. It receives commands from the background page.
*/
var zoomLevel = .25;
var currentZoom = parseInt($('body').css('zoom'));//TODO css is not updated after a zoom
var lastEditedInput = null;

//from https://css-tricks.com/snippets/jquery/make-jquery-contains-case-insensitive/
$.expr[":"].containsci = $.expr.createPseudo(function(arg) {
  return function( elem ) {
    return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
  };
});

/**
 * Called from the background page.
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

function appendToLinks(){
  $("a").append("yep");
}

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

function zoomIn(amount, context){
  if (context == "D") {
    var tb = $("viewer-toolbar");
  } else {
    var dec_amount = amount / 100;
    _setZoom(currentZoom + dec_amount);
  }
}

function zoomOut(amount, context){
  if (context == "D") {
    //alert($("#zoom-out-button").find("div").attr("id"));
  } else {
    var dec_amount = amount / 100;
    _setZoom(currentZoom - dec_amount);
  }
}

function click(str){
  var b = $("a:containsci("+str+")").first();
  if(b[0] == undefined){
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

function enterText(str){
  lastEditedInput.val(str);
}

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

function submitText(){
  if (lastEditedInput != null) {
    lastEditedInput.closest('form').submit();
  }
}

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
