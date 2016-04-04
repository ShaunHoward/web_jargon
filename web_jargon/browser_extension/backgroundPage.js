/**
The background page controls extension-level, window-level, and high-level tab functions
Functions starting with underscore(_) are not callable by the api. They are helper-functions only.
*/

var states = Object.freeze({READY: 1, BUSY: 2, ERROR: 3});
var state = states.READY;

var startPhrases = ["web jargon", "browser", "chrome"];
var stopPhrases = ["stop web jargon", "stop listening"];

var server = localStorage["serverURL"];//"http://localhost:8080/";

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
      var str = event.results[i][0].transcript;
      _processText(str);
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
}

_startRecognition();

function _processText(str){
  str = str.trim();
  console.log(str);
  for(p in startPhrases){
    var phrase = startPhrases[p];
    var i = str.indexOf(phrase);
    if(i >= 0){
      var end = i+phrase.length;
      _sendText(str.substring(end, str.length));
      return;
    }
  }
}

function _sendText(str){
  _setBusy();
  $.post( server, str, function( data ) {
    console.log(data);
    var cmd = JSON.parse(data)["action"];
    var func = cmd["action"];
    var params = cmd["arg_list"]; 
    var msg = _doCommand(func, params);
    _doCommand("addMessage",[func]);
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
  chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
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
  if(tabId == undefined){
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
      chrome.tabs.remove(tabs[0].id);
    });
  }
  else if(typeof tabId != "string"){
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
  if(tabId == undefined){
    return;
  }
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

function displaySetup(){
   if (chrome.runtime.openOptionsPage) {
    // New way to open options pages, if supported (Chrome 42+).
    chrome.runtime.openOptionsPage();
  } else {
    // Reasonable fallback.
    window.open(chrome.runtime.getURL('options.html'));
  }
}

function displayHelp(){
  chrome.tabs.create({ url: "help.html" });
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
      if(response && response.msg){
        return response.msg;
      }
  });
});
}

function _getAudioPermission(){
  window.open("chrome-extension://"+chrome.runtime.id+"/additional/requestAudio.html");
}

function _startRecognition(){
  recognition.start();
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
