const formatter = gantt.ext.formatters.durationFormatter({
    // default values
    enter: "hour",
    store: "hour",
    format: "auto",
    short: false,
    minutesPerHour: 60,
    hoursPerDay: 8,
    hoursPerWeek: 40,
    daysPerMonth: 22,
    daysPerYear: 365,
    labels: {
        minute: {
            full: "minute",
            plural: "minutes",
            short: "min"
        },
        hour: {
            full: "hour",
            plural: "hours",
            short: "h"
        },
        day: {
            full: "day",
            plural: "days",
            short: "d"
        },
        week: {
            full: "week",
            plural: "weeks",
            short: "wk"
        },
        month: {
            full: "month",
            plural: "months",
            short: "mon"
        },
        year: {
            full: "year",
            plural: "years",
            short: "y"
        }
    }
});