var backgroundPage = chrome.extension.getBackgroundPage();

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
  var msg = backgroundPage.testEditor(commands);
  });
});

$("#listenButton").click(function( event ) {
  //event.preventDefault();
  if (!('webkitSpeechRecognition' in window)) {
    upgrade();
  } else{
    backgroundPage.startListening();
  }
});

$("#optionsButton").click(function( event ) { 
  alert("opening options");
  if (chrome.runtime.openOptionsPage) {
    // New way to open options pages, if supported (Chrome 42+).
    chrome.runtime.openOptionsPage();
  } else {
    // Reasonable fallback.
    window.open(chrome.runtime.getURL('options.html'));
  }
});
