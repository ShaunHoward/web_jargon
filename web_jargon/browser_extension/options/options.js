
function save_options() {
  var serverURL = document.getElementById('serverURL').value;
  //msg(serverURL);
  localStorage["serverURL"] = serverURL;
  msg(localStorage["serverURL"]);
}

function restore_options() {
  document.getElementById('serverURL').value = localStorage["serverURL"];
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
