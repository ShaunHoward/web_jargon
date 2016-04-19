/**
The background page controls extension-level, window-level, and high-level tab functions
Functions starting with underscore(_) are not callable by the api. They are helper-functions only.
*/
var states = Object.freeze({READY: 1, BUSY: 2, ERROR: 3});
var state = states.READY;

var audio_success = new Audio();
audio_success.src = "audio/success.mp3";
var audio_fail = new Audio();
audio_fail.src = "audio/fail.mp3";

var startPhrases = ["web jargon", "browser", "chrome"];

var server;
var audioResponse;
var textResponse;
_loadOptions();

var keepListening = true;
var asked = false;

var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

recognition.onerror = function(event) {
  //check if microphone is available
  if(event.error == 'not-allowed' && asked == false){
   asked = true;
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
  chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
    var url;
    if (tabs != undefined) {
        url = tabs[0].url;
    } else {
        url = "www.google.com";
    }
    var key = (Math.random()*1e20).toString(36);
    _setBusy();
    var sendData = new Object();
    sendData.command = str;
    sendData.url = url;
    sendData.session_id = key;
    $.post( server, JSON.stringify(sendData), function( data ) {
      // expect json, but if html received, server is not configured properly
      if (data != undefined && data.indexOf("<!DOCTYPE html>") < 0) {
        console.log(data);
      } else {
        console.log("server needs to be configured...make sure to save configuration options!");
        return;
      }
      var ret_id = JSON.parse(data)["session_id"];
      if(key != ret_id){
        return; //unknown response
      }
      var cmd = JSON.parse(data)["action"];
      if(cmd == null){
        _onError("command not found");
        return;
      }
      var func = cmd["action"];
      var params = cmd["arg_list"];
      var context = cmd["context"];
      var msg = _doCommand(func, params, context);
      _setReady();
      if (msg != "error"){
        _onSuccess(str, func, params);
      } else {
        _onError("error executing action, please try again...");
        _setError();
      }
    })
    .fail(function() {
      _onError("could not connect to server...");
      _setError();
    });
  });
}

function _onError(msg){
  if(audioResponse){
    audio_fail.play();
  }
  if(textResponse){
    _doCommand("_addMessage",[msg]);
  }
}

function _onSuccess(inputStr, func, params){
  if(audioResponse){
    audio_success.play(); 
  }
  if(textResponse){
    _doCommand("_addMessage",[func]);
  }
}

function openURL(u, currentTab){
  if (u == undefined){
    u = "google";
  }
  // either resolve the input domain name/url or create a google search
  u = _resolveOrSearch(u, currentTab);
}

function _norm_url(u) {
  u = u.trim();
  var http = "http://";
  var www = "www.";
  var com = ".com";

  // add www. to front of url to go to the world-wide web
  if (u.indexOf(www) < 0) {
    u = www.concat(u);
  }
  // add http:// to front of url to go to correct protocol
  if (u.indexOf(http) < 0) {
    u = http.concat(u);
  }

  // try to find .com or ..*{2,3}
  matches = u.match("\\.[a-z]{2,3}$");
  if (matches == undefined) {
    // if no match was found, add .com to give url a chance
    u = u.concat(com);
  }
  return u;
}

function openTab(u){
  openURL(u, false);
}

/**
Closes a tab
if input is number: Closes via index from left (0-start)
if input is string: Closes tabs which contain input string
*/
function closeTab(tabId){
  // do not execute action if tab id is undefined
  if(tabId == undefined){
    return;
  }
  if (typeof(tabId) == "number") {
    _closeTabAtIndex(tabId);
  } else if (typeof(tabId) == "string") {
    //tab id is a string
    chrome.tabs.query({currentWindow: true}, function (tabs) {
      for (t in tabs){
        lower_title = tabs[t].title.toLowerCase();
        if(lower_title.indexOf(tabId) > -1){
          chrome.tabs.remove(tabs[t].id);
        }
      }
    });
  }
  return;
}

/**
Switches active tab
if input is number: Chooses via index from left (0-start)
if input is string: Chooses first tab which contains input string
*/
function switchTab(tabId){
  // do not execute action if tab id is undefined
  if(tabId == undefined){
    return;
  }
  if (typeof(tabId) == "number") {
    chrome.tabs.query({currentWindow: true}, function (tabs) {
        if (0 < tabId && tabId <= tabs.length){
           chrome.tabs.update(tabs[tabId-1].id, {active: true});
        }
    });
  } else if (typeof(tabId) == "string") {
      //tab id is a string
      chrome.tabs.query({currentWindow: true}, function (tabs) {
        for (t in tabs){
          lower_title = tabs[t].title.toLowerCase();
          if(lower_title.indexOf(tabId) > -1){
            chrome.tabs.update(tabs[t].id, {active: true});
          }
        }
      });
  }
  return;
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

function displayHelp(show, context){
  var show = (show === "true");
  if (show == true) {
      chrome.tabs.create({ url: "/html_help_pages/"+context+"_help_page.html" });
  } else {
     closeTab("help_page");
  }
}

function _closeTabAtIndex(tabIndex) {
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
      if (0 < tabIndex && tabIndex <= tabs.length) {
        chrome.tabs.remove(tabs[tabIndex-1].id);
      }
    });
}

/**
Executes input command
Checks background page functions first, then checks current tab functions
*/
function _doCommand(cmd, params, context){
  params.push(context);
  if (typeof window[cmd] == 'function') {
    window[cmd].apply(null, params);
    return;
  }
  //if function not found in background page, check content script
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {func : cmd, params : params}, function(response) {
      if(response){
        return response;
      } else {
        return "error";
      }
  });
});
}

function _getAudioPermission(){
  window.open("chrome-extension://"+chrome.runtime.id+"/additional/requestAudio.html");
}

function _loadOptions(){
  //set defaults if needed
  if(localStorage["serverURL"] == undefined){
    localStorage["serverURL"] = "http://localhost:8080/WebJargon";
  }
  if(localStorage["audioResponse"] == undefined){
    localStorage["audioResponse"] = true;
  }
  if(localStorage["textResponse"] == undefined){
    localStorage["textResponse"] = true;
  }
  server = localStorage["serverURL"];
  audioResponse = localStorage["audioResponse"] == "false" ? false : true;
  textResponse = localStorage["textResponse"] == "false" ? false : true;

  //ping server
  var key = 1234;
  var sendData = new Object();
  sendData.command = "test";
  sendData.url = "test";
  sendData.session_id = key;
  $.post( server, JSON.stringify(sendData), function( data ) {
    var ret_id = JSON.parse(data)["session_id"];
    if(key != ret_id){
      return; //unknown response
    }
    _setReady();
  })
  .fail(function() {
    _setError();
  });
}

function _getURL(name){
  var fullURL = "http://www."+name+".com";
  //alert(_websiteExists(fullURL));
  return _websiteExists(fullURL) ? fullURL : "http://www.google.com/#q="+name;
}

function _resolveOrSearch(input, url, curr_tab){
  if (input == undefined){
    input = "";
  }
  if (url == undefined) {
    url = "";
  }
  // normalize url
  var url = _norm_url(input);
  $.get(url, function () {
    // url exists
    _finishOpeningURL(url, curr_tab);
  }).fail(function () {
    // need to do a google search
    _finishOpeningURL("http://www.google.com/#q=" + input, curr_tab);
  });
}

function _finishOpeningURL(u, currentTab){
  if(currentTab){
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
      chrome.tabs.update(tabs[0].id, {url: u});
    });
  } else {
    chrome.tabs.create({url: u});
  }
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
