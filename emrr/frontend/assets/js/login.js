function check() {
  event.preventDefault();
  var form = document.forms["login"];
  if (form.userid.value == "pf900" && form.pswrd.value == "password") {
    window.open('/pf900_pid/index.htm', '_self')
  } else if (form.userid.value == "pf350a" && form.pswrd.value == "password") {
    window.open('/pf350a_pid/index.htm', '_self')
  } else {
    alert("Error: Wrong username or password")
  }
}