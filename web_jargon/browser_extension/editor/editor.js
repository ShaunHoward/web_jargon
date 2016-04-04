/**
The editor controls tab-specific functions. It receives commands from the background page.
*/
var zoomLevel = .25;
var currentZoom = parseInt($('body').css('zoom'));//TODO css is not updated after a zoom
var lastEditedInput = null;

/**
 * Called from the background page.
 */
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (typeof window[request.func] == 'function') {
      window[request.func].apply(null, request.params);
    } else{
      sendResponse({msg: "not found"}); 
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

function zoomIn(){
  _zetZoom(currentZoom + zoomLevel);
}

function zoomOut(){
  _zetZoom(currentZoom - zoomLevel);
}

function click(str){
  var b = $("a:contains("+str+")").first();
  b[0].click();
}

function enterText(str){
  lastEditedInput.val(str);
}

function selectElement(name){
  var e = $("input[placeholder*='"+name+"']");
  lastEditedInput = e;
  e.focus();
}

function submitText(){
  if(lastEditedInput != null){
    lastEditedInput.closest('form').submit();
  }
}

function playVideo(){
  $("button[aria-label='Play']").click();
}

function pauseVideo(){
  $("button[aria-label='Pause']").click();
}

function openFullscreen(){
  $("button[title='Full screen']").click();
}

function closeFullscreen(){
  $("button[title='Exit full screen']").click();
}

function playMusic(){
  var frame = $("#app-player");
  var contents = frame.contents();
  var btn = contents.find("button[id='play-pause']");
  btn.click();
}

function pauseMusic(){
  var frame = $("#app-player");
  var contents = frame.contents();
  var btn = contents.find("button[id='play-pause']");
  btn.click();
}

function nextSong(){
  var frame = $("#app-player");
  var contents = frame.contents();
  var btn = contents.find("button[id='next']");
  btn.click();
}

function searchMusic(artist, album, song){
  lastEditedInput = $(".form-control");
  lastEditedInput.val(artist+" "+album+" "+song);
  submitText();
}

function goToPage(num){
  window.location.href = window.location.href+"#page="+num;
}

function _zetZoom(z){
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

function addMessage(str){
  /*$('html').append('<div style="position:fixed;color:white;background-color:black;right:5px;top:5px;width:100px;height:60px;z-index:1000;">'+str+'</div>');*/
  $('<div id="WebJargonInfo" style="position:fixed;color:white;background-color:black;right:5px;top:5px;width:100px;height:60px;z-index:1000;">'+str+'</div>').appendTo('html');
  $("#WebJargonInfo").fadeOut(2000, function(){
    $("#WebJargonInfo").remove();
  });
}
