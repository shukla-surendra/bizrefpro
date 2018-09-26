$("#profileForm").validate({
    rules: {
      name: "required",
      email: {
        required: true,
        email: true
      },
      phone: "required",
      address1: "required",
      country: "required",
      state: "required",
      city: "required",
    },
    messages: {
      password: "Please enter the Name",
      email: {
        required: "Please provide your email to login",
        email: "Your email address must be in the format of name@domain.com"
      },
      phone: "Please enter the Contact Number",
      address1: "Please enter the Address 1",
      country: "Please select the Country",
      state: "Please select the State",
      city: "Please enter the City",
    }
  })