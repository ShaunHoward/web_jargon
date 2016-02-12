/**
 * Interrupts extension button text input form to manually post to server
 */
$("#textInput").submit(function( event ) {
  var server = "http://localhost:8080/";
  var inputText = $("input:first").val();
  event.preventDefault();
  $.post( server, inputText, function( data ) {
  $("#JargonPopup").append("</br>"+data);
  var commands = JSON.parse(data)["actions"];
  var msg = chrome.extension.getBackgroundPage().testEditor(commands);
  });
});
