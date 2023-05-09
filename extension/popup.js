document.addEventListener("DOMContentLoaded", function() {
    var myButton = document.getElementById("myButton");
    myButton.addEventListener("click", function() {
      var question = document.getElementById("question").value;
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(tabs[0].id, {code: 'encodeURIComponent(document.body.innerText)'}, function(result) {
          var text = result[0];
          console.log(text); // log the extracted text to the console
          var urlEncodedText = encodeURIComponent(text);
          var base64EncodedText = btoa(urlEncodedText); // encode the text in base64
          var data = {corpus: base64EncodedText, question: question};
          fetch("http://127.0.0.1:5000/answer", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
              "Content-Type": "application/json"
            }
          })
          .then(function(response) {
            return response.json();
          })
          .then(function(data) {
            document.getElementById("answer").textContent = data.answer;
          })
          .catch(function(error) {
            console.log(error);
          });
        });
      });
    });
  });
  