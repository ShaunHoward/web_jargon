/**
The editor controls tab-specific functions. It receives commands from the background page.
*/
var zoomLevel = .25;
var currentZoom = parseInt($('body').css('zoom'));//TODO css is not updated after a zoom

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

function _addBox(str){
  $('html').append('<div style="position:absolute;color:white;background-color:black;right:30px;top:30px;width:100px;height:60px;">'+str+'</div>');
}
