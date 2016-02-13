/**
The backgroud page controls extension-level, window-level, and high-level tab functions
Functions starting with underscore(_) are not callable by the api. They are helper-functions only
*/

/**
Opens a new tab with the input url
*/
function createTab(u){
  chrome.tabs.create({ url: "http://www."+u+".com" });
}

/**
Closes a tab
if input is number: Closes via index from left (0-start)
if input is string: Closes tabs which contain input string
*/
function closeTab(tabId){
  if(typeof tabId != "string"){
    chrome.tabs.query({index: tabId, currentWindow: true}, function (tabs) {
      chrome.tabs.remove(tabs[0].id);
    });
  } else{
  //tab id is a string
  chrome.tabs.query({currentWindow: true}, function (tabs) {
    for (t in tabs){
      if(tabs[t].title.match(new RegExp(tabId))){
        chrome.tabs.remove(tabs[t].id);
      }
    }
  });
  }
}

/**
Switches active tab
if input is number: Chooses via index from left (0-start)
if input is string: Chooses first tab which contains input string
*/
function switchTab(tabId){
  if(typeof tabId != "string"){
    chrome.tabs.query({index: tabId, currentWindow: true}, function (tabs) {
      chrome.tabs.update(tabs[0].id, {active: true});
    });
  } else{
  //tab id is a string
  chrome.tabs.query({currentWindow: true}, function (tabs) {
    for (t in tabs){
      if(tabs[t].title.match(new RegExp(tabId))){
        chrome.tabs.update(tabs[t].id, {active: true});
      }
    }
  });
  }

  chrome.tabs.update(window.tabs[i].id, {active: true});
}

/**
Exectues input command
Checks background page functions first, then checks current tab functions
*/
function _doCommand(cmd, params){
  if (typeof window[cmd] == 'function') { 
    if(params.length == 0){
      window[cmd]();
    } else{
      window[cmd](params[0]);
    }
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

function _getAudioPermission(){
  alert("asking for permission");
  window.open("chrome-extension://"+chrome.runtime.id+"/additional/requestAudio.html");
}

function _startListening(){
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
