navigator.webkitGetUserMedia({
      audio: true,
    }, function(stream) {
      stream.stop();
      alert("granted");
      //permission granted
      }, function() {
      //permission rejected
  });

var backgroundPage = chrome.extension.getBackgroundPage();
backgroundPage.startListening();
close();
