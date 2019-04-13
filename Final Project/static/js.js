function check(form)/*function to check userid & password*/
{
 /*the following code checkes whether the entered userid and password are matching*/
 if(form.userid.value == "guest" && form.pswrd.value == "guest")
  {
    window.open('entry.html')/*opens the target page while Id & password matches*/
  }
 else
 {
   alert("Error Password or Username")/*displays error message*/
  }
  document.getElementById('loginform').style.visibility = 'hidden'
}