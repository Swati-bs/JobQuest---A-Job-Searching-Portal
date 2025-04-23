// document.addEventListener('DOMContentLoaded', function () {
//     const locationTypeField = document.querySelector('#id_location_type');  // Location type dropdown
//     const locationField = document.querySelector('#id_location');          // Location text input

//     function toggleLocationField() {
//         if (locationTypeField.value === 'Remote') {
//             locationField.disabled = true;  // Disable location input for "Remote"
//             locationField.value = '';      // Clear the field
//         } else {
//             locationField.disabled = false;  // Enable location input otherwise
//         }
//     }

//     // Trigger toggle function on load and change event
//     toggleLocationField();
//     locationTypeField.addEventListener('change', toggleLocationField);
// });