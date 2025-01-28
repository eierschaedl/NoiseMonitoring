/*!
* Start Bootstrap - Scrolling Nav v5.0.6 (https://startbootstrap.com/template/scrolling-nav)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-scrolling-nav/blob/master/LICENSE)
*/
//
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // File upload validation script
    function validateAudio() {
        const fileInput = document.getElementById("audioUpload");
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        // Check file type
        const allowedTypes = ["audio/mp3", "audio/wav"];
        if (!allowedTypes.includes(file.type)) {
            alert("Only MP3 and WAV files are allowed.");
            return;
        }

        // Check file size (max 10MB)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            alert("File size exceeds 10MB. Please select a smaller file.");
            return;
        }

        // Check file duration (max 5 minutes)
        const audio = new Audio(URL.createObjectURL(file));
        audio.onloadedmetadata = function() {
            const duration = audio.duration; // in seconds
            if (duration > 300) { // 5 minutes = 300 seconds
                alert("Audio duration exceeds 5 minutes. Please select a shorter file.");
            } else {
                alert("File is valid! Proceeding with upload...");
                // Here you can add your upload functionality
            }
        };
    }

    // Assign the validateAudio function to the upload button
    const uploadButton = document.querySelector('.upload-button-category');
    if (uploadButton) {
        uploadButton.addEventListener('click', validateAudio);
    }
});
