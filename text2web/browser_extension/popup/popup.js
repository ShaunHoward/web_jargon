/**
 * Interrupts extension button text input form to manually post to server
 */
$( "#textInput" ).submit(function( event ) {
  var server = "http://localhost:8080/";
  var inputText = $("input:first").val();
  event.preventDefault();
  $.post( server, inputText, function( data ) {
    if(typeof data == "string"){
      $("#JargonPopup").append("</br>"+data);
    } else{
      for(command in JSON.parse(data)){
        executeCommand(command);
      }
    }
  });
  //executeCommand("dostuff");//TODO remove
});
