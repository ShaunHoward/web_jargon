/**
 * The background page controls extension-level, window-level, and high-level tab functions
 * Functions starting with underscore(_) are not callable by the api. They are helper-functions only.
 */

// states of the extension's operation -- based on server connectivity, command matching, other system issues
var states = Object.freeze({READY: 1, BUSY: 2, ERROR: 3});
var current_state = states.READY;

// success and failure noises for the status of an action
var audio_success = new Audio();
audio_success.src = "audio/success.mp3";
var audio_fail = new Audio();
audio_fail.src = "audio/fail.mp3";

// phrases to start web jargon listening -- system stops listening after reasonable pause
var startPhrases = ["web jargon", "browser", "chrome"];

// Globally store server information as well as notification options
var server;
var audioResponse;
var textResponse;

// load options into global variables
_loadOptions();

// whether to keep listening in the web speech API, always true for our extension
var keepListening = true;

// whether permission has been granted to the microphone by the user
var permission_granted = false;

// instantiate a new web speech api recognition object
var recognition = new webkitSpeechRecognition();
// include all results
recognition.continuous = true;
recognition.interimResults = true;

// define a speech recognition error callback
recognition.onerror = function(event) {
  //check if microphone is available and permission has not already been granted
  if(event.error == 'not-allowed' && permission_granted == false){
   permission_granted = true;
   _getAudioPermission();
  }
}

// define a speech recognition result callback
recognition.onresult = function(event) {
  // process the final command transcript received from the web speech api
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    if (event.results[i].isFinal) {
      var command = event.results[i][0].transcript;
      // send command data to be processed, executed and user notified
      _processExecuteAndNotify(command);
    }
  }
}

// define a speech recognition end callback
recognition.onend = function() {
  // either restart listening or set non-listening state
  if(keepListening){
    _startRecognition();
  } else{
    listening = false;
  }
}

// load options on start if last state was error state, otherwise no other necessary actions
recognition.onstart = function(){
  if (current_state == states.ERROR) {
    _loadOptions();
  }
}

/**
 * Define extension helper functions.
 */
function _startRecognition(){
  recognition.start();
}

// used to give permission to the extension for web speech microphone access
function _getAudioPermission(){
  window.open("chrome-extension://"+chrome.runtime.id+"/additional/requestAudio.html");
}

/**
 * Loads or sets default values for user options.
 * Tries to ping the API server in order to assure connection is properly configured.
 * Handles state transition from ready to error if connection is unavailable.
 */
function _loadOptions(){
  //set option defaults if necessary
  if(localStorage["serverURL"] == undefined){
    localStorage["serverURL"] = "http://localhost:8080/WebJargon";
  }
  if(localStorage["audioResponse"] == undefined){
    localStorage["audioResponse"] = true;
  }
  if(localStorage["textResponse"] == undefined){
    localStorage["textResponse"] = true;
  }

  // load options saved by user
  server = localStorage["serverURL"];
  audioResponse = localStorage["audioResponse"] == "false" ? false : true;
  textResponse = localStorage["textResponse"] == "false" ? false : true;

  // set up request object for pinging the API server
  var sendData = new Object();
  sendData.command = "test";
  sendData.url = "test";

  // generate random session id key
  var key = 31 * Math.random();
  sendData.session_id = key;

  /**
   * Attempt to post to the API server configured with the extension via options,
   * set ready or error state based on response.
   */
  $.post( server, JSON.stringify(sendData), function( data ) {
    var ret_id = JSON.parse(data)["session_id"];
    // validate that session id key received is the same generated in order to set ready state
    if(key == ret_id){
      _setReady();
    } else {
      // set error state since response was invalid
      _setError();
    }
  })
  .fail(function() {
    // failure to connect to server results in error state being set
    _setError();
  });
}

// used to set the extension toolbar icon
function _setIcon(file){
  chrome.browserAction.setIcon({
    path: file
  });
}

// set the states of the system
function _setReady(){
  _setIcon("popup/plugin_ready.png");
  current_state = states.READY;
}
function _setBusy(){
  _setIcon("popup/plugin_busy.png");
  current_state = states.BUSY;
}
function _setError(){
  _setIcon("popup/plugin_error.png");
  current_state = states.ERROR;
}

/**
 * Handles action request processing, sending a request to the API server,
 * extracting the request and executing it as well as notifying the user.
 */
function _processExecuteAndNotify(command){
  // clean command of whitespace
  command = command.trim();
  console.log(command);

  // try to find a start phrase in the command input
  for(p in startPhrases){
    // determine if a wake word phrase was spoken
    var phrase = startPhrases[p];
    var i = command.indexOf(phrase);
    // only send the web action sequence if a wake word phrase was spoken
    if(i >= 0){
      // sends the command text to the api
      var request_start = i + phrase.length;
      var request_end = command.length;
      // send the action request sub-sequence to the server API for text processing, then execute and notify of status
      _sendExecuteAndNotify(command.substring(request_start, request_end).trim());
      return;
    }
  }
}

/**
 * Sends the given action command request to the API server,
 * attempts to execute the received web action sequence,
 * and notifies the user of success or error based on desired options.
 */
function _sendExecuteAndNotify(action_command_request){
  chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
    var url;
    // either get the current url or assume google.com
    if (tabs != undefined) {
        url = tabs[0].url;
    } else {
        url = "www.google.com";
    }

    // generate random sha256 session id key
    var key = sha256digest((Math.random()*31*23).toString(36));

    // set busy state since extension is reaching out to API server
    _setBusy();

    // create data object to send to the API server
    var sendData = new Object();
    sendData.command = action_command_request;
    sendData.url = url;
    sendData.session_id = key;

    // attempt to post an action request to the API server
    $.post( server, JSON.stringify(sendData), function( data ) {
      // expect json, but if html received, server is not configured properly
      if (data != undefined && data.indexOf("<!DOCTYPE html>") < 0) {
        console.log(data);
      } else {
        console.log("server needs to be configured...make sure to save configuration options!");
        return;
      }

      // validate return id matches generated id
      var ret_id = JSON.parse(data)["session_id"];
      if(key != ret_id){
        return; //unknown response
      }

      // extract command from action request
      var cmd = JSON.parse(data)["action"];
      if(cmd == null){
        // handle empty command
        _onError("command not found");
        return;
      }

      // extract response information
      var func = cmd["action"];
      var params = cmd["arg_list"];
      var context = cmd["context"];

      // attempt to execute the command via the provided function call, argument list and browsing context
      var msg = _doCommand(func, params, context);

      // set plugin back to ready state since action has returned
      _setReady();

      // check if command returned successfully or set error state
      if (msg != "error"){
        _onSuccess(action_command_request, func, params);
      } else {
        _onError("error executing action, please try again...");
      }
    })
    .fail(function() {
      _onError("could not connect to server...");
      _setError();
    });
  });
}

// used to notify the user of erroneous action execution
function _onError(msg){
  if(audioResponse){
    audio_fail.play();
  }
  if(textResponse){
    _doCommand("_addMessage",[msg]);
  }
}

// used to notify the user of successful action execution
function _onSuccess(inputStr, func, params){
  if(audioResponse){
    audio_success.play();
  }
  if(textResponse){
    _doCommand("_addMessage",[func]);
  }
}

/**
 * Executes input command.
 * Checks background page functions first, then checks current tab functions.
 */
function _doCommand(cmd, params, context){
  if (typeof window[cmd] == 'function') {
    params.push(context)
    window[cmd].apply(null, params);
    return;
  }
  //if function not found in background page, check content script
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {func: cmd, params: params}, function(response) {
      if(response){
        return response;
      } else {
        return "error";
      }
  });
});
}

/**
 * Closes the tab at the specified index from the leftmost tab starting with choice 1 and ending at
 * the number of open tabs.
 */
function _closeTabAtIndex(tabIndex) {
  chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
    if (0 < tabIndex && tabIndex <= tabs.length) {
      chrome.tabs.remove(tabs[tabIndex-1].id);
    }
  });
}

/**
 * Switches to the tab at the specified index from the leftmost tab with choices starting at 1 and
 * ending at the number of open tabs.
 */
function _switchToTabAtIndex(index) {
  chrome.tabs.query({currentWindow: true}, function (tabs) {
    if (0 < tabId && tabId <= tabs.length){
      chrome.tabs.update(tabs[tabId-1].id, {active: true});
    }
  });
}

/**
 * Either resolves the given input to a valid url or creates a Google search string to search the given input.
 * :param input: the input query text as is
 * :param url: the url created from the given input query text
 * :param curr_tab: the currently open tab id
 */
function _resolveOrSearch(input, url, curr_tab){
  // initialize input and url if undefined
  if (input == undefined){
    input = "";
  }
  if (url == undefined) {
    url = "";
  }

  // attempt to create a valid, normal url using http://www.website.com format
  var url = _norm_url(input);

  // perform a get request on the designated url
  $.get(url, function () {
    // finish opening the url if it exists
    _finishOpeningURL(url, curr_tab);
  }).fail(function () {
    // finish opening a google search of the original input query
    _finishOpeningURL("http://www.google.com/#q=" + input, curr_tab);
  });
}

/**
 * Either opens the specified url in the current tab or in a new tab.
 * Note the url must be valid in order to properly open or an error will be given.
 */
function _finishOpeningURL(input_url, currentTab){
  if(currentTab){
    // open the url in the current open tab
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
      chrome.tabs.update(tabs[0].id, {url: input_url});
    });
  } else {
    // open the url in a new tab
    chrome.tabs.create({url: u});
  }
}

/**
 * Define supported web actions via the global background page for the extension.
 */

/**
 * Attempts to open a given string as a url or applies a google search to the text.
 * Attempts to convert the input into a URL string to resolve to an actual host,
 * otherwise, searches Google for the provided text.
 */
function openURL(input, currentTab){
  if (input == undefined){
    // set default destination as google.com
    input = "google";
  }
  // either resolve the input domain name/url or create a google search
  output = _resolveOrSearch(input, currentTab);
}

/**
 * Opens a new tab with the specified input text.
 */
function openTab(input){
  openURL(input, false);
}

/**
 * Closes an open tab based on either the index from the leftmost tab starting at one or
 * a unique substring of the desired tab name.
 * If tabId is number: Closes tab at the specified index from leftmost tab (one to number of tabs open)
 * If tabId is string: Closes tabs which contain input string
*/
function closeTab(tabId){
  // do not execute action if tab id is undefined
  if(tabId == undefined){
    return;
  }

  // either close tab at index or with name containing substring
  if (typeof(tabId) == "number") {
    // close tab at specified index
    _closeTabAtIndex(tabId);
  } else if (typeof(tabId) == "string") {
    chrome.tabs.query({currentWindow: true}, function (tabs) {
      // close all tabs containing the specified substring
      for (t in tabs){
        // normalize case of text for substring matching
        lower_title = tabs[t].title.toLowerCase();
        if(lower_title.indexOf(tabId) > -1){
          // close the tab if match found
          chrome.tabs.remove(tabs[t].id);
        }
      }
    });
  }
  return;
}

/**
 * Switches between open tabs based on either the index from the leftmost tab starting at one or
 * a unique substring of the desired tab name.
 * If tabId is number: Switches to tab at the specified index from leftmost tab (one to number of tabs open)
 * If tabId is string: Switches to the first active tab that contains the input string id
*/
function switchTab(tabId){
  // do not execute action if tab id is undefined
  if(tabId == undefined){
    return;
  }
  // switch to a different tab via tab id number or substring
  if (typeof(tabId) == "number") {
    // switch to tab at specified index
    _switchToTabAtIndex(tabId);
  } else if (typeof(tabId) == "string") {
    // open the first tab including the input string id
    chrome.tabs.query({currentWindow: true}, function (tabs) {
      for (t in tabs){
        // normalize case of title
        lower_title = tabs[t].title.toLowerCase();
        if(lower_title.indexOf(tabId) > -1){
          // switch to matching tab and leave loop
          chrome.tabs.update(tabs[t].id, {active: true});
          break;
        }
      }
    });
  }
  return;
}

// used to display the options page for the extension
function displaySetup(){
  if (chrome.runtime.openOptionsPage) {
    // New way to open options pages, if supported (Chrome 42+).
    chrome.runtime.openOptionsPage();
  } else {
    // Reasonable fallback to open html options page
    window.open(chrome.runtime.getURL('options.html'));
  }
}

// toggle display of the html help page based on current web page context and input command
function displayHelp(show, context){
  var show = (show === "true");
  if (show == true) {
    chrome.tabs.create({ url: "/html_help_pages/"+context+"_help_page.html" });
  } else {
    closeTab("help_page");
  }
}

// start speech recognition once everything is defined
_startRecognition();
