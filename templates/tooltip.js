gantt.plugins({
    tooltip: true
});
gantt.attachEvent("onGanttReady", function(){
    var tooltips = gantt.ext.tooltips;
    tooltips.tooltip.setViewport(gantt.$task_data);
});
