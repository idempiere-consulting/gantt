gantt.plugins({
    auto_scheduling: true
});

gantt.templates.scale_cell_class = function (date) {
    if (!gantt.isWorkTime(date)) {
        return "weekend";
    }
};
gantt.templates.timeline_cell_class = function (item, date) {
    if (!gantt.isWorkTime(date)) {
        return "weekend";
    }
};

gantt.config.work_time = true;


gantt.config.auto_scheduling = true;
gantt.config.auto_scheduling_strict = true;
gantt.config.auto_scheduling_compatibility = true;

gantt.config.date_format = "%d-%m-%Y";

gantt.config.start_date = new Date(2020, 3, 1);
gantt.config.end_date = new Date(2020, 2, 1);


gantt.attachEvent("onBeforeAutoSchedule", function () {
    gantt.message("Recalculating project schedule...");
    return true;
});
gantt.attachEvent("onAfterTaskAutoSchedule", function (task, new_date, constraint, predecessor) {
    if(task && predecessor){
        gantt.message({
            text: "<b>" + task.text + "</b> has been rescheduled to " + gantt.templates.task_date(new_date) + " due to <b>" + predecessor.text + "</b> constraint",
            expire: 4000
        });
    }
});
