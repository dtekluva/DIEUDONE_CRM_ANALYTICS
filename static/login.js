let email = document.getElementById("user")
let pass = document.getElementById("pass")
let trigger = document.getElementById("trigger")

trigger.addEventListener("click", function(){
    if (email.value == ""){
        alert("invalid email")
    }
    else if (pass.value == ""){
        alert("invalid pass")
    }
    else if (email.value == "eze.ifechi@stu.cu.edu.ng" && pass.value == "1802240cu"){
        window.location.replace("/static/dashboard.html")
    }
    else{
        alert("Invalid login details")
    }

})