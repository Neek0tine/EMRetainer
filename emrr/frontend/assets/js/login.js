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

function togglePasswordVisibility() {
  var passwordInput = document.getElementById("InputPassword");
  var eyeIcon = document.getElementById("eyeIcon");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      eyeIcon.classList.remove("fa-eye");
      eyeIcon.classList.add("fa-eye-slash");
  } else {
      passwordInput.type = "password";
      eyeIcon.classList.remove("fa-eye-slash");
      eyeIcon.classList.add("fa-eye");
  }
}