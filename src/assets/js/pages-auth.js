/**
 *  Pages Authentication
 */

'use strict';
const formAuthentication = document.querySelector('#formAuthentication');
const btnSubmit = document.getElementById('btnSubmit');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const numeralMask = document.querySelectorAll('.numeral-mask');

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    // Form validation for Add new record
    if (formAuthentication) {
      const fv = FormValidation.formValidation(formAuthentication, {
        fields: {
          username: {
            validators: {
              notEmpty: {
                message: 'Будь ласка ввведіть логін'
              },
              stringLength: {
                min: 4,
                message: 'Логін має бути більш ніж 4 символа'
              }
            }
          },
          email: {
            validators: {
              notEmpty: {
                message: 'Будь ласка введіть свій email'
              },
              emailAddress: {
                message: 'Будь ласка введіть вірний email'
              }
            }
          },
          'email-username': {
            validators: {
              notEmpty: {
                message: 'Будь ласка введіть логін / username'
              },
              stringLength: {
                min: 4,
                message: 'Логін має бути більш ніж 4 символа'
              }
            }
          },
          password: {
            validators: {
              notEmpty: {
                message: 'Будь ласка введіть пароль'
              },
              stringLength: {
                min: 4,
                message: 'Пароль має бути більш ніж 4 символа'
              }
            }
          },
          'confirm-password': {
            validators: {
              notEmpty: {
                message: 'Повторіть пароль'
              },
              identical: {
                compare: function () {
                  return formAuthentication.querySelector('[name="password"]').value;
                },
                message: 'Паролі не співпадають'
              },
              stringLength: {
                min: 4,
                message: 'Пароль має бути більш ніж 4 символа'
              }
            }
          },
          terms: {
            validators: {
              notEmpty: {
                message: 'Будь ласка, погодьтеся з умовами'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-5'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });

      if (btnSubmit && btnText && btnLoader) {
        // Show loading state on form submission
        btnSubmit.addEventListener('click', function (event) {
          event.preventDefault(); // Prevent default form submission

          // Check if the form is valid
          fv.validate().then(function (status) {
            if (status === 'Valid') {
              // If the form is valid, show loading state
              btnSubmit.classList.add('disabled');
              btnText.textContent = 'Відправка email... ';
              btnLoader.classList.remove('visually-hidden');
            }
          });
        });
      }
    }

    // Verification masking
    if (numeralMask.length) {
      numeralMask.forEach(e => {
        new Cleave(e, {
          numeral: true
        });
      });
    }
  })();
});
