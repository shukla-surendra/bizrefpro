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


$("#signUpForm").validate({
  rules: {
    name: "required",
    password: "required",
    email: {
      required: true,
      email: true
    },
    phone:"required"
  },
  messages: {
    name: "Please Provide your name",
    password: "Please enter the password",
    email: {
      required: "Please provide your email to signup",
      email: "Your email address must be in the format of name@domain.com"
    },
    phone:"Please Provide your Contact Number"
  }
})