triggerBtn = document.getElementById("trigger");
textArea = document.getElementById("textArea");


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

    fetchRes.then(res =>
        res.json()).then(d => {
            console.log(d)
        })
}
triggerBtn.addEventListener("click", function(e) {
    // alert("WOW..!! this is old");
    console.log(textArea.value)
    let text = textArea.value
    postToServer(text);
})

