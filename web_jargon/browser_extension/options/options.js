var backgroundPage = chrome.extension.getBackgroundPage();

function save_options() {
  var serverURL = document.getElementById('serverURL').value;
  var audioResponse = document.getElementById('audioResponse').checked;
  var textResponse = document.getElementById('textResponse').checked;
  localStorage["serverURL"] = serverURL;
  localStorage["audioResponse"] = audioResponse;
  localStorage["textResponse"] = textResponse;
  backgroundPage._loadOptions();
  msg("saved");
}

function restore_options() {
  var ar = localStorage["audioResponse"] == "false" ? false : true;
  var tr = localStorage["textResponse"] == "false" ? false : true;
  document.getElementById('serverURL').value = localStorage["serverURL"];
  document.getElementById('audioResponse').checked = ar;
  document.getElementById('textResponse').checked = tr;
}

function msg(str){
  var msg = document.getElementById('msg');
  msg.innerHTML = str;
  setTimeout(function() {
    msg.innerHTML = '';
  }, 750);
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);
