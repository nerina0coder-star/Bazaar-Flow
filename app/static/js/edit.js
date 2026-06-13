var password1 = document.getElementById('new_password');
var passwordC = document.getElementById('confirm_password');

function validatePassword() {
	if (password1.value !== passwordC.value
	&& password1.value !== '' &&
	passwordC.value != '') {
		document.getElementById(
		'higherPasswordMatch'
		).className = "custom-alert alert-danger-custom";
		document.getElementById(
		'passwordMatch'
		).innerText =
		"رمز عبور با رمز عبور تاییدی مطابقت ندارد ";
		return false;
	} else if (passwordC.value == '' && password1.value !== '') {
		document.getElementById(
		"higherPasswordMatch"
		).classList.remove("d-none");
		document.getElementById(
		"passwordMatch"
		).innerText = "رمز عبور تایید نشده است";
		return false;
	}
	document.getElementById('higherPasswordMatch').classList.add("d-none")
	return true;
}

function validateEtc() {
	if (document.getElementById('username').value == '' ||
	document.getElementById('email').value == '') {
		document.getElementById('higherEtcError').
		className = "custom-alert alert-danger-custom";
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
                const h = document.getElementById("higherEtcError");
                h.className = "custom-alert alert-danger-custom";
                h.style = "";
		return false;
	}
	const h =document.getElementById('higherEtcError');
        h.className = '';
        h.style = "display: none;";
	return true;
}

function validateForm () {
	return validateEtc() || validatePassword();
}
