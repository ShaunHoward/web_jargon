var backgroundPage = chrome.extension.getBackgroundPage();

/**
 * Interrupts extension button text input form to manually post to server
 */
$("#textInput").submit(function( event ) {
  //backgroundPage._doCommand("click",["gaming"]);
  var server = "http://localhost:8080/";
  var inputText = $("input:first").val();
  event.preventDefault();
  $.post( server, inputText, function( data ) {
    addLine(data);
    var commands = JSON.parse(data)["actions"];
    var msg = backgroundPage._doCommand(commands, params);
  })
  .fail(function() {
    addLine("could not connect");
  });
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
