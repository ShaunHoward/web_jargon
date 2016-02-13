/**
 * Called from the background page.
 */
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (typeof window[request.func] == 'function') {
      window[request.func]();
    } else{
      sendResponse({msg: "not found"}); 
    }   
  });


function _askForAudio(){
  alert("asking in popup");
  //$("document").append("<webview src='chrome-extension://"+chrome.runtime.id+"/requestAudio.html' width='640' height='480'></webview>");
  //$("document").append("<webview src='google.com' width='640' height='480'></webview>");

}


function appendToLinks(){
    $("a").append("yep");
}

function scrollDown(){
  var current = $(document).scrollTop();
  var dest = current + $(window).height();
  _scrollVertical(dest);
}

function scrollUp(){
  var current = $(document).scrollTop();
  var dest = current - $(window).height();
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

function _addBox(){
  $('html').append('<div>heyoooooo</div>');
  alert("done");
}
