//function Delegate() {
//    var self = this;
//
//    var request = function request(method, url, data = null, callback = null) {
//        var xhttp = new XMLHttpRequest();
//        xhttp.onreadystatechange = function() {
//            if (xhttp.readyState == 4) {
//                if (xhttp.status == 200) {
//                    // Action to be performed when the document is read;
//                    if (callback) { callback(JSON.parse(xmlHttp.responseText)); }
//                } else {
//                    // TODO: Form proper response
//                    return xmlHttp.status;
//                }
//            }
//        };
//        xhttp.open(method, url, true);
//        xhttp.send(null);
//    }
//
//}
