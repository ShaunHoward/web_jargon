function _getAudioPermission(){
  alert("asking for permission");
  window.open("chrome-extension://"+chrome.runtime.id+"/requestAudio.html");
}

function createTab(){
  chrome.tabs.create({ url: "http://www.cnn.com" });
}

function testEditor(cmd){
  if (typeof window[cmd] == 'function') { 
    window[cmd]();
    return;
  }
  //if function not found in backgound page, check content script
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {func : cmd}, function(response) {
      if(response.msg){
        alert(response.msg);
      }
  });
});
}

function startListening(){
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onerror = function(event) {
    //check if microphone is available
    if(event.error == 'not-allowed'){
      _getAudioPermission();
    }
  }
  recognition.onresult = function(event) {
    var final_transcript = "";
    var interim_transcript = "";
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
	alert(event.results[i][0].transcript);
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    
  }
  recognition.start();
}

