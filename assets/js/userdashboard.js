document.addEventListener('DOMContentLoaded', () => {

    const editPhone = document.querySelector('.edit-phone');
    const editEmail = document.querySelector('.edit-email');

    const phoneText = document.getElementById('phone-text');
    const phoneInput = document.getElementById('phone-input');

    const emailText = document.getElementById('email-text');
    const emailInput = document.getElementById('email-input');

    // Phone edit functionality
    editPhone.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent event bubbling

        // close email first
        emailText.style.display = 'block';
        emailInput.style.display = 'none';

        phoneText.style.display = 'none';
        phoneInput.style.display = 'block';

        phoneInput.focus();
    });

    editEmail.addEventListener('click', (e) => {

    e.stopPropagation();

    // close phone first
    phoneText.style.display = 'block';
    phoneInput.style.display = 'none';

    emailText.style.display = 'none';
    emailInput.style.display = 'block';

    emailInput.focus();

});
    // Click outside 
    document.addEventListener('click', () => {
        // save changes
        phoneText.innerText = phoneInput.value;

        emailText.innerText = emailInput.value;

        // close both inputs
        phoneText.style.display = 'block';
        phoneInput.style.display = 'none';
        
        emailText.style.display = 'block';
        emailInput.style.display = 'none';

    });
    
    // Prevent closing when clicking inside input fields
    phoneInput.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent event bubbling
    });

    emailInput.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent event bubbling
    });

});
