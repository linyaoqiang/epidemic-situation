/* global $ */
var login = document.querySelector('.login')
var loginForm = document.querySelector('.login-form')
var register = document.querySelector('.register')
var registerForm = document.querySelector('.register-form')

// 点击登录注册切换
login.onclick = function () {
  console.log(login.classList)
  if (!login.classList.contains('active')) {
    login.classList.add('active')
    loginForm.classList.add('active')
    register.classList.remove('active')
    registerForm.classList.remove('active')
  }
}
register.onclick = function () {
  if (!register.classList.contains('active')) {
    register.classList.add('active')
    registerForm.classList.add('active')
    login.classList.remove('active')
    loginForm.classList.remove('active')
  }
}

