document.addEventListener('DOMContentLoaded', () => {

    const editPhone = document.querySelector('.edit-phone');

    const phoneText = document.getElementById('phone-text');
    const phoneInput = document.getElementById('phone-input');

    editPhone.addEventListener('click', () => {

        if(phoneInput.style.display === 'block') {

            phoneText.innerText = phoneInput.value;

            phoneText.style.display = 'block';
            phoneInput.style.display = 'none';

        } else {

            phoneText.style.display = 'none';
            phoneInput.style.display = 'block';
        }

    });

});