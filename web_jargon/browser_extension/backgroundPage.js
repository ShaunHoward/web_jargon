/**
The background page controls extension-level, window-level, and high-level tab functions
Functions starting with underscore(_) are not callable by the api. They are helper-functions only.
*/

var states = Object.freeze({READY: 1, BUSY: 2, ERROR: 3});
var state = states.READY;

var server = "http://localhost:8080/";

var listening = false;
var keepListening = true;

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
      //alert(event.results[i][0].transcript);
      var str = event.results[i][0].transcript;
      _sendText(str);
    } else {
      interim_transcript += event.results[i][0].transcript;
    }
  }
}
recognition.onend = function() {
  if(keepListening){
    recognition.start();
  } else{
    listening = false;
  }
}
recognition.onstart = function(){
  listening = true;
}

function _sendText(str){
  _setBusy();
  $.post( server, str, function( data ) {
    var commands = JSON.parse(data)["actions"];
    for(c of commands){
      var func = c["action"];
      var params = c["arguments"]; 
      alert(str);
      //alert(data);
      var msg = _doCommand(func, params);
      _doCommand("addMessage",[func]);
    }
    _setReady();
  })
  .fail(function() {
    _setError();
    _doCommand("addMessage",["Could not connect to server"]);
  });

}

function openUrl(u, currentTab){
  if(!currentTab){
   openTab(u);
   return;
  }
  chrome.tabs.query({index: tabId, currentWindow: true}, function (tabs) {
    chrome.tabs.update(tabs[0].id, {url:  "http://www."+u+".com"});
  });
}

function openTab(u){
  if (u == undefined){
    u = "google";
  }
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
Executes input command
Checks background page functions first, then checks current tab functions
*/
function _doCommand(cmd, params){
  if (typeof window[cmd] == 'function') { 
    window[cmd].apply(null, params);
    return;
  }
  //if function not found in backgound page, check content script
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {func : cmd, params : params}, function(response) {
      if(response.msg){
        //nothing
      }
  });
});
}

function _getAudioPermission(){
  window.open("chrome-extension://"+chrome.runtime.id+"/additional/requestAudio.html");
}

function _toggleListening(){
  if(listening){
    keepListening = false;
    recognition.stop();
  } else{
    recognition.start();
  }
}

function _setIcon(file){
  chrome.browserAction.setIcon({
    path: file
  });
}
function _setReady(){
  _setIcon("popup/plugin_ready.png");
  state = states.READY;
}
function _setBusy(){
  _setIcon("popup/plugin_busy.png");
  state = states.BUSY;
}
function _setError(){
  _setIcon("popup/plugin_error.png");
  state = states.ERROR;
}
