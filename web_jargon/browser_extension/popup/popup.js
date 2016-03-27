var backgroundPage = chrome.extension.getBackgroundPage();

/**
 * Interrupts extension button text input form to manually post to server
 */
$("#textInput").submit(function( event ) {
  //backgroundPage._doCommand("click",["gaming"]);
  var inputText = $("input:first").val();
  event.preventDefault();
  backgroundPage._sendText(inputText);
});

$("#listenButton").click(function( event ) {
  //event.preventDefault();
  if (!('webkitSpeechRecognition' in window)) {
    upgrade();
  } else{
    backgroundPage._toggleListening();
  }
});

function addLine(str){
  $("#JargonPopup").append("</br>"+str);
}
