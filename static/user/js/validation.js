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
      password: "<i>Please enter the Name</i>",
      email: {
        required: "<i>Please provide your email to login</i>",
        email: "<i>Your email address must be in the format of name@domain.com</i>"
      },
      phone: "<i>Please enter the Contact Number</i>",
      address1: "<i>Please enter the Address 1</i>",
      country: "<i>Please enter the Country</i>",
      state: "<i>Please enter the State</i>",
      city: "<i>Please enter the City</i>",
    }
  })