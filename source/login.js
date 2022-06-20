import axios from 'axios';
import { getCookie, sameOrigin } from './helpers';

document.addEventListener("DOMContentLoaded", function () {

  // Get form
  var loginForm = document.getElementById('login-form');
  var username = document.getElementById("inputUsername");
  var password = document.getElementById("inputPassword");
  var formErrors = document.getElementById("errors");

  loginForm.addEventListener('submit', function (e) {

    console.log(username.value + ", " + password.value);
    console.log("Trying to submit!")

    e.preventDefault();
    var csrftoken = getCookie("csrftoken")
    var requestOptions = {
      headers: {
        "X-CSRFToken": csrftoken,
        "content-type": "application/json"
      },
      method: "post",
      data: {
        "username": username.value,
        "password": password.value
      },
      url: '/admin/login/'
    }
    axios(requestOptions)
      .then(response => {
        if ("errors" in response.data) {
          formErrors.innerHTML = response.data["errors"]
        } else {
          window.location = response.data['redirect_url']
        }
      })
      .catch(error => {
        formErrors.innerHTML = error
        console.log(error);
      });
  })
}, false);
