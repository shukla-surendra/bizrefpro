$("#signinForm").validate({
  rules: {
    password: "required",
    email: {
      required: true,
      email: true
    },
      address1: "required",
      country: "required",
      state: "required",
      city: "required",
      pincode: "required",
  },
  messages: {
    password: "Please enter the password",
    email: {
      required: "Please provide your email to login",
      email: "Your email address must be in the format of name@domain.com"
    }
  }
})

$.validator.addMethod("pwcheck", function(value) {
  /* return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
       && /[a-z]/.test(value) // has a lowercase letter
       && /[A-Z]/.test(value) // has a lowercase letter
       && /\d/.test(value) // has a digit*/
  strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{4,})");
  return strongRegex.test(value)
},'Password must contain at least 1 uppercase, digit and special char');

$("#signUpForm").validate({
  rules: {
    name: "required",
    password: {required:true, pwcheck:true},
      cpassword: {required:true, equalTo:"#password"},
    email: {
      required: true,
      email: true
    },
    phone:"required",
      state:"required"
  },
  messages: {
    name: "Please Provide your name",
    password:{required:"Please enter the password"},
      cpassword:{required:"Please confirm the above password"},
    email: {
      required: "Please provide your email to signup",
      email: "Your email address must be in the format of name@domain.com"
    },
    phone:"Please Provide your Contact Number",
      state:"Please select the state"
  }
});

$("#resetPasswordForm").validate({
  rules: {
    password: {required:true, pwcheck:true},
      cpassword: {required:true, equalTo:'#password'},

  },
  messages: {
    password:{required:"Please enter the password"},
      cpassword:{required:"Please re-enter the password"},
  }
})

