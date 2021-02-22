	// scale settings
	gantt.config.scales = [
		{unit: "month", step: 1, format:"%M %Y"},
		{unit: "day", step: 1, format: "%d, %l"},
		{unit: "hour", step: 1, format: "%H"},
	];
	gantt.config.scale_height = 20 * 3;
	gantt.config.min_column_width = 18;
	gantt.ignore_time = function(date) {
		return !gantt.isWorkTime(date, "hour");
	};

/* 	// work time and duration
	gantt.config.duration_unit = "minute";
	gantt.config.work_time = true;
	gantt.config.time_step = 15;
	gantt.config.round_dnd_dates = false;
	gantt.config.open_tree_initially = true;
 */
	// work time and duration
	gantt.config.duration_unit = "hour";
	gantt.config.work_time = true;
	gantt.config.time_step = 1;
	gantt.config.round_dnd_dates = false;
	gantt.config.open_tree_initially = true;


	gantt.setWorkTime({hours: [9, 13, 14, 18]});//global working hours. 8:00-12:00, 13:00-17:00

	// formatting durations
	var dayFormatter = gantt.ext.formatters.durationFormatter({
		enter: "day", 
		store: "minute", 
		format: "day",
		hoursPerDay: 8,
		hoursPerWeek: 40,
		daysPerMonth: 30,
		short: false	
	});
	var hourFormatter = gantt.ext.formatters.durationFormatter({
		enter: "hour", 
		store: "minute", 
		format: "hour",
		short: true	
	});
	var autoFormatter = gantt.ext.formatters.durationFormatter({
		enter: "hour", 
		store: "hour", 
		format: "auto"
	});

	var textEditor = {type: "text", map_to: "text"};
	var dateEditor = {type: "date", map_to: "start_date", min: new Date(2018, 0, 1), max: new Date(2019, 0, 1)};
	var durationEditor = {type: "duration", map_to: "duration", formatter: autoFormatter, min:0, max:1000};
	var dayDurationEditor = {type: "duration", map_to: "duration", formatter: dayFormatter, min:0, max:1000};
	var hourDurationEditor = {type: "duration", map_to: "duration", formatter: hourFormatter, min:0, max:1000};

	gantt.config.columns = [
		{name: "text", tree: true, width: 170, resize: true},//, editor: textEditor},
		{name: "start_date", align: "center", resize: true, editor: dateEditor},
		{name: "duration", label:"Duration", resize: true, align: "center", template: function(task) {
			return autoFormatter.format(task.duration);
		}, editor: durationEditor, width: 100},
		{name: "hourDuration", label:"Duration (hours)", resize: true, align: "center", template: function(task) {
			return hourFormatter.format(task.duration);
		}, editor: hourDurationEditor, width: 100},
		{name: "dayDuration", label:"Duration (days)", resize: true, align: "center", template: function(task) {
			return dayFormatter.format(task.duration);
		}, editor: dayDurationEditor, width: 100},
		{name: "add", width: 44}
	];
	gantt.config.lightbox.sections = [
		{name: "description", height: 70, map_to: "text", type: "textarea", focus: true},
		{name: "time", type: "duration",  height: 170,map_to: "auto", formatter: autoFormatter}
	];

	gantt.templates.timeline_cell_class = function (task, date) {
		var css = [];

		if (!gantt.isWorkTime(date, 'day')) {
			css.push("week_end");
		}

		return css.join(" ");
	};

