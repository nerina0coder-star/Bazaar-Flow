var password1 = document.getElementById('password');
var passwordC = document.getElementById('confirmPassword');

function validatePassword() {
	if (password1.value !== passwordC.value
	&& password1.value !== '' &&
	passwordC.value != '') {
		document.getElementById(
		'higherPasswordMatch'
		).className = "alert alert-danger alert-dismissable show fade";
		document.getElementById(
		'passwordMatch'
		).innerText =
		"رمز عبور با رمز عبور تاییدی مطابقت ندارد ";
		return false;
	} else if (password1.value == '') {
		document.getElementById(
		"higherPasswordMatch"
		).className = "alert alert-danger alert-dismissable fade show";
		document.getElementById(
		"passwordMatch"
		).innerText = "رمز عبور وارد نشده است";
		return false;
	} else if (passwordC.value == '') {
		document.getElementById(
		"higherPasswordMatch"
		).className = "alert alert-danger alert-dismissable fade show";
		document.getElementById(
		"passwordMatch"
		).innerText = "رمز عبور تایید نشده است";
		return false;
	}
	document.getElementById('higherPasswordMatch').className = ''
	return true;
}

function validateEtc() {
	if (document.getElementById('username').value == '' ||
	document.getElementById('email').value == '') {
		document.getElementById('higherEtcError').
		className = "alert alert-danger alert-dismissable show fade";
		var uname = document.getElementById('username');
		var email = document.getElementById('email')
		
		const err = document.getElementById('etcError');
		if (uname.value == '' && email.value == '') {
			err.innerText =
			"نام کاربری و ایمیل خیالی است";
		} else if (uname.value == '') {
			err.innerText = 
			"نام کاربری خالی است";
		} else {
			err.innerText =
			"ایمیل خالی است";
		}
		return false;
	}
	document.getElementById('higherEtcError').className = ''
	return true;
}

function validateForm () {
	return validateEtc() || validatePassword();
}