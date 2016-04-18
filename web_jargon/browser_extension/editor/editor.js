/**
The editor controls tab-specific functions. It receives commands from the background page.
*/
var zoomLevel = .25;
var currentZoom = parseInt($('body').css('zoom'));//TODO css is not updated after a zoom
var lastEditedInput = null;
var url = null;

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
      url = request.url;
      window[request.func].apply(null, request.params);
    } else{
      //sendResponse({msg: "not found"}); 
    }   
  });

function appendToLinks(){
    $("a").append("yep");
}

function scrollDown(num){
  if(num == undefined){
    num = 1;
  }
  var current = $(document).scrollTop();
  var dest = current + ($(window).height())*num;
  _scrollVertical(dest);
}

function scrollUp(num){
  if(num == undefined){
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

function zoomIn(amount){
  var dec_amount = amount / 100;
  _setZoom(currentZoom + dec_amount);
}

function zoomOut(amount){
  var dec_amount = amount / 100;
  _setZoom(currentZoom - dec_amount);
}

function click(str){
  var b = $("a:containsci("+str+")").first();
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

  if(e.val() == undefined){
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
  if(lastEditedInput != null){
    lastEditedInput.closest('form').submit();
  }
}

function playVideo(){
  var doc = $(window).scrollTop();
  $("button[aria-label='Play']").each(function(){
    var relative = $(this).offset().top - doc;
    if(relative > 0){
      $(this).click();
      return false;
    }
  });
}

function pauseVideo(){
  var doc = $(window).scrollTop();
  $("button[aria-label='Pause']").each(function(){
    var relative = $(this).offset().top - doc;
    if(relative > 0){
      $(this).click();
      return false;
    }
  });
}

function nextVideo(){
  var doc = $(window).scrollTop();
  $("a[title='Next']").each(function(){
    var relative = $(this).offset().top - doc;
    if(relative > 0){
      window.location.href = $(this).attr("href");
      return false;
    }
  });
}

function openFullscreen(){
  var doc = $(window).scrollTop();
  $("button[aria-label='Full screen']").each(function(){
    var relative = $(this).offset().top - doc;
    if(relative > 0){
      $(this).click();
      return false;
    }
  });
}

function closeFullscreen(){
  var doc = $(window).scrollTop();
  $("button[aria-label='Exit full screen']").each(function(){
    var relative = $(this).offset().top - doc;
    if(relative > 0){
      $(this).click();
      return false;
    }
  });
}

function playMusic(is_spotify){
  var is_spotify = _getBool(is_spotify);
  if(is_spotify){
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
  if(is_spotify){
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
  if(is_spotify){
    var frame = $("#app-player");
    var contents = frame.contents();
    var btn = contents.find("button[id='next']");
    btn.click();
  } else {
    $(".skipButton").click();
  }
}

function searchMusic(is_spotify, artist, album, song, type){
  var is_spotify = _getBool(is_spotify);
  if(is_spotify){
    if (type=="artist"){
      // do artist search
    } else if (type == "album") {
      //do album search
    } else if (type == "song") {
      //do song search
    } else {
      //do search using all input
      window.location.href = "http://play.spotify.com/search/" + [artist, album, song].join(" ");
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
