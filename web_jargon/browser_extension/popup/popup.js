var backgroundPage = chrome.extension.getBackgroundPage();

/**
 * Interrupts extension button text input form to manually post to server
 */
$("#textInput").submit(function( event ) {
  var inputText = $("input:first").val();
  event.preventDefault();
  backgroundPage._sendExecuteAndNotify(inputText);
});

$("#settings").click(function( event ) {
  chrome.runtime.openOptionsPage(); 
});

function addLine(str){
  $("#JargonPopup").append("</br>"+str);
}
