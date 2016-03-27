/**
 * Code from google API docs. 
 * https://developer.chrome.com/extensions/optionsV2
 */

// Saves options to chrome.storage.sync.
function save_options() {
  var serverURL = document.getElementById('serverURL').value;
  chrome.storage.sync.set({
    serverURL: sserverURL
  }, function() {
    // Update status to let user know options were saved.
    var msg = document.getElementById('msg');
    status.textContent = 'Options saved.';
    setTimeout(function() {
      status.textContent = '';
    }, 750);
  });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
  // Use default value color = 'red' and likesColor = true.
  chrome.storage.sync.get({
    serverURL: "http://localhost:8080/",
  }, function(items) {
    document.getElementById('serverURL').value = items.serverURL;
  });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);
