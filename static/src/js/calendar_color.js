odoo.define('book_management.calendar_custom_color', function (require) {
    "use strict";

    var CalendarView = require('web.CalendarView');

    CalendarView.include({
        // Override the method that gets the event's color
        _getEventColor: function (event) {
            // Customize colors based on state
            if (event.state === 'ongoing') {
                return "#FF0000";  // Red for 'ongoing'
            } else if (event.state === 'returned') {
                return "#00FF00";  // Green for 'returned'
            } else if (event.state === 'waiting') {
                return "#FFFF00";  // Yellow for 'waiting for approval'
            } else if (event.state === 'draft') {
                return "#0000FF";  // Blue for 'draft'
            } else if (event.state === 'rejected') {
                return "#FF00FF";  // Magenta for 'rejected'
            } else if (event.state === 'completed') {
                return "#FFA500";  // Orange for 'completed'
            } else if (event.state === 'canceled') {
                return "#808080";  // Gray for 'canceled'
            } else {
                return "#0000FF";  // Default color (blue)
            }
        },
    });
});
