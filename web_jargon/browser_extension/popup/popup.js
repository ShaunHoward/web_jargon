var backgroundPage = chrome.extension.getBackgroundPage();

/**
 * Interrupts extension button text input form to manually post to server
 */
$("#textInput").submit(function( event ) {
  backgroundPage.doCommand("createTab", ["cnn"]);
  /*var server = "http://localhost:8080/";
  var inputText = $("input:first").val();
  event.preventDefault();
  $.post( server, inputText, function( data ) {
  $("#JargonPopup").append("</br>"+data);
  var commands = JSON.parse(data)["actions"];
  var msg = backgroundPage.doCommand(commands);
  });*/
});

$("#listenButton").click(function( event ) {
  //event.preventDefault();
  if (!('webkitSpeechRecognition' in window)) {
    upgrade();
  } else{
    backgroundPage._startListening();
  }
});
