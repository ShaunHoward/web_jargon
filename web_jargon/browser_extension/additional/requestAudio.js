var backgroundPage = chrome.extension.getBackgroundPage();

navigator.webkitGetUserMedia({
      audio: true,
    }, function(stream) {
      //granted
      stream.stop();
      backgroundPage._startRecognition();
      close();
      }, function() {
      //denied
      backgroundPage._denyAudioPermission();
      close();
  });
