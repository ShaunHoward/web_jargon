function testRequest(){
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
