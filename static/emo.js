let triggerBtn = document.getElementById("trigger");
let textArea = document.getElementById("textArea");
let sentiment = document.getElementById("sentiment");
let name = document.getElementById("name");
let email = "";
let lga = "";
let total = 1;
let negative_count = 1;
let positive_count = 1;

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
            if (d.data.Predicted_sentiment == "Negative"){
                negative_count ++;
            }else{
                positive_count ++;

            }
            total++;
            positivity = (positive_count/negative_count) * 100
            console.log(positivity)
            if (total > 10 & positivity < 80){
                sendEmail();
                 Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: `Hello, Your entries are over ${(100-positivity).toLocaleString()}% negative comments.`,
                    footer: '<a href="">You will be redirected to a psychiatrist. Please check you email</a>'
                  })
                }
                
                return d
            })
        }

    sendEmail = function(text){
    // Options to be given as parameter
    // in fetch for making requests
    // other then GET
    
    let options = {
        method: 'GET',
        headers: {
            'Content-Type':'application/json;charset=utf-8'
        }
    }

    lga = (findGetParameter("lga"))
    email = (findGetParameter("email"))
    // Fake api for making post requests
    let fetchRes = fetch("http://134.209.196.208/send_mail?lga="+ lga + "&email=" + email, options);
    // let fetchRes = fetch("http://localhost:8000/send_mail?lga="+ lga + "&email=" + email, options);

    fetchRes.then(res =>
        res.json()).then(d => {
            console.log(d)
            if (0){
                 Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: `Hello, Your entries are over ${(100-positivity).toLocaleString()}% negative comments.`,
                    footer: '<a href="">You will be redirected to a psychiatrist. Please check you email</a>'
                  })
                }
                
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

function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

name.innerText = (findGetParameter("email").split("@")[0])
