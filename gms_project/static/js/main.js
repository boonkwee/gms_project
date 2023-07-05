// const date = new Date();
// document.querySelector('.year').innerHTML = date.getFullYear();
document.addEventListener('DOMContentLoaded', function() {
    const date = new Date();
    const yearElement = document.querySelector('.year');
    if (yearElement) {
      yearElement.innerHTML = date.getFullYear();
    }
  });

setTimeout(function() {
    $('#messages').fadeOut('slow');
}, 3000);

function submitForm() {
  const form = document.getElementById('default_form');
  const fields = form.querySelectorAll('input, textarea, select');

  fields.forEach(function(field) {
    field.value = '';
  });
}