var session = ''
function login() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("login").innerHTML = this.responseText.split('$')[1];
      session = this.responseText.split('$')[0]
    }
  };
  var us = document.getElementById("usernamel").value;
  var ps = document.getElementById("passwordl").value;
  xhttp.open("POST", "/login/"+ us +"/" + ps, true);
  xhttp.send();
}

function signup() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("signup").innerHTML = this.responseText;
    }
  };
//  alert(this.responseText)
  var us = document.getElementById("username").value;
  var ps = document.getElementById("password").value;
  xhttp.open("POST", "/signup/"+ us +"/" + ps, true);
  xhttp.send();
}

function create() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("create-room").innerHTML = this.responseText;
    }
  }  
  var caller = session
  var callee = document.getElementById("callee").value;
  xhttp.open("POST", "/create/"+ caller +"/" + callee, true);
  xhttp.send();
}
function rooms() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("rooms").innerHTML = this.responseText;
    }
  }  
  xhttp.open("POST", "/rooms/", true);
  xhttp.send();
}

