(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')
  
  
  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()

const doc = document.getElementsByClassName('collapsible')

      for (let i = 0; i < doc.length; i++) {
        doc[i].addEventListener('click', function () {
          this.classList.toggle('active')
          let content = this.nextElementSibling
          if (content.style.display === 'block') {
            content.style.display = 'none'
          } else {
            content.style.display = 'block'
          }
        })
      }
