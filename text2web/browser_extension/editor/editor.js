/**
 * Called when a command is recieved from the server
 */
function executeCommand(command){
  alert("executing "+command);
  chrome.tabs.executeScript(null, { code: command.func=";"/*"scrollUp();"*/});
}

function appendToLinks(){
    $("a").append("yep");
}

function createTab(){
  chrome.tabs.create({ url: "http://cnn.com" });
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
