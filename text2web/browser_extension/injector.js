alert("hihi");
(function (chrome) {
    var js = document.createElement('script');
    js.type = 'text/javascript';
    js.src = chrome.extension.getURL('inject.js');
    document.getElementsByTagName('head')[0].appendChild(js);
}(chrome));
