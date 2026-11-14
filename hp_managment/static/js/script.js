document.addEventListener("DOMContentLoaded", function () {

    // Prevent selecting past appointment dates
    const dateInput = document.getElementById("appointment_date");

    if (dateInput) {
        const today = new Date();
        const localDate = new Date(
            today.getTime() - today.getTimezoneOffset() * 60000
        ).toISOString().split("T")[0];

        dateInput.min = localDate;
    }

    // Confirm appointment cancellation
    const cancelForms = document.querySelectorAll(
        'form[action*="cancel-appointment"]'
    );

    cancelForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm(
                "Are you sure you want to cancel this appointment?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

});