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
