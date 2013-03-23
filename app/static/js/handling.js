myFunction = function() {
  var query = document.getElementById("query").value;
  var num = document.getElementById("phone_number").value;
  var responseField = document.getElementById("response");

  var img = document.createElement("img");
  img.src = "images/loading.gif";

  var xhr = createXHR();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      //responseField.value = xhr.responseText;
      showPanel(xhr.responseText)
    }
  }

  var fieldNameElement = document.getElementById("putresponse");
  clearResponseDiv();
  fieldNameElement.appendChild(img);
  
  xhr.open('POST', '/sms?Body=' + query + "&From=" + num, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.send();
}

function showPanel(fieldName) {
  var fieldNameElement = document.getElementById("putresponse");
  clearResponseDiv();
  fieldNameElement.appendChild(fieldNameElement.ownerDocument.createTextNode(fieldName));
}

function clearResponseDiv() {
  var fieldNameElement =  document.getElementById("putresponse");
  while(fieldNameElement.childNodes.length >= 1) {
    fieldNameElement.removeChild(fieldNameElement.firstChild);
  }
}