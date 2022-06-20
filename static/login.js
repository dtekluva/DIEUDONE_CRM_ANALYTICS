let email = document.getElementById("user")
let pass = document.getElementById("pass")
let lga = document.getElementById("lga")

let trigger = document.getElementById("trigger")
trigger.addEventListener("click", function(){
    if (email.value == ""){
        alert("invalid email")
    }
    else if (pass.value == ""){
        alert("invalid pass")
    }
    else if (lga.value == "Please pick your LGA"){
        alert("Please Pick an LGA")
    }
    else if (email.value == "eze.ifechi@stu.cu.edu.ng" && pass.value != "1802240cu" || email.value != "" && pass.value != ""){
        window.location.replace(`/static/dashboard.html?email=${email.value}&lga=${lga.value}`)
    }
    else{
        alert("Invalid login details")
    }

})