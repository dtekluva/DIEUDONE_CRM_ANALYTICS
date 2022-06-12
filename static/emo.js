let triggerBtn = document.getElementById("trigger");
let textArea = document.getElementById("textArea");
let sentiment = document.getElementById("sentiment");


postToServer = function(text){
    // Options to be given as parameter
    // in fetch for making requests
    // other then GET
    
    let options = {
        method: 'GET',
        headers: {
            'Content-Type':'application/json;charset=utf-8'
        }
    }
    // Fake api for making post requests
    let fetchRes = fetch("http://134.209.196.208/test?text=" + text, options);
    // let fetchRes = fetch("http://localhost:8000/test?text=" + text, options);

    fetchRes.then(res =>
        res.json()).then(d => {
            console.log(d)
            sentiment.innerText = d.data.Predicted_sentiment
            return d
        })
}

triggerBtn.addEventListener("click", function(e) {
    // alert("WOW..!! this is old");
    console.log(textArea.value)

    let text = textArea.value
    if (text == ""){
        alert("Text area Cannot Be empty")
        return;
    };

    if (text.length < 15){
        alert("Enter at least 15 characters")
        return;
    }
    let response = postToServer(text);

})

