/**
 * Called when a command is recieved from the server
 */
function executeCommand(command){
  alert("executing "+command);
  chrome.tabs.executeScript(null, { code: "appendToLinks();"});
}

function appendToLinks(){
    $("a").append("yep");
}

function createTab(){
  chrome.tabs.create({ url: "http://cnn.com" });
}
