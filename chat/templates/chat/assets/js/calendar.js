document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var titleEl = document.getElementById('calendar-title');
    var dateInput = document.getElementById('calendar-date-input');

    const isMobile = window.innerWidth < 768;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: false,
        initialView: isMobile ? 'listDay' : 'dayGridWeek',
        eventDidMount: function () {
            titleEl.innerText = calendar.view.title;
        },
        datesSet: function () {
            titleEl.innerText = calendar.view.title;
        },
        dayHeaderContent: function (args) {
            const date = args.date;
            const weekday = date.toLocaleDateString('en-US', { weekday: 'short' });
            const day = date.getDate();
            return {
                html: `<span class="fc-weekday d-block fw-normal h6 mb-0 text-uppercase">${weekday}</span><span class="fc-day d-block fw-bold h1 mb-0">${day}</span>`
            };
        },
        events: 'https://fullcalendar.io/api/demo-feeds/events.json'
    });

    calendar.render();

    // Navigation
    document.getElementById('prevBtn').addEventListener('click', function () {
        calendar.prev();
    });

    document.getElementById('nextBtn').addEventListener('click', function () {
        calendar.next();
    });

    // Flatpickr popup for both desktop and mobile
    let fpInstance = null;

    titleEl.addEventListener('click', function () {
        // Always destroy previous instance if it exists
        if (fpInstance) {
            fpInstance.destroy();
        }

        // Create new Flatpickr popup on hidden input
        fpInstance = flatpickr(dateInput, {
            defaultDate: calendar.getDate(),
            onChange: function (selectedDates) {
                if (selectedDates[0]) {
                    calendar.gotoDate(selectedDates[0]);
                }
            },
            onClose: function () {
                fpInstance = null;
            }
        });

        fpInstance.open(); // 👈 Open manually
    });
});

// Set default date and time
document.addEventListener("DOMContentLoaded", function () {
    // Set today's date
    const dateInput = document.getElementById("event-date");
    dateInput.value = new Date().toISOString().split("T")[0];

    // Set default time to 12:00
    const timeInput = document.getElementById("event-time");
    timeInput.value = "12:00";
});