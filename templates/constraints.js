gantt.templates.task_class = function (st, end, item) {
			childrens=gantt.getChildren(item.id).length ? "gantt_project" : "";
/* 			console.log('item',item)
			console.log('children',childrens)
			console.log('gantt',gantt)
 */			// console.log('children',childrens)
			return childrens;
		};
		gantt.init("gantt_here");

		function limitMoveLeft(task, limit) {
			var dur = task.end_date - task.start_date;
			task.end_date = new Date(limit.end_date);
			task.start_date = new Date(+task.end_date - dur);
		}

		function limitMoveRight(task, limit) {
			var dur = task.end_date - task.start_date;
			task.start_date = new Date(limit.start_date);
			task.end_date = new Date(+task.start_date + dur);
		}

		function limitResizeLeft(task, limit) {
			task.end_date = new Date(limit.end_date);
		}

		function limitResizeRight(task, limit) {
			task.start_date = new Date(limit.start_date)
		}

		gantt.attachEvent("onTaskDrag", function (id, mode, task, original, e) {
			
			var parent = task.parent ? gantt.getTask(task.parent) : null,
				children = gantt.getChildren(id),
				modes = gantt.config.drag_mode;

			var limitLeft = null,
				limitRight = null;

			if (!(mode == modes.move || mode == modes.resize)) return;

			if (mode == modes.move) {
				limitLeft = limitMoveLeft;
				limitRight = limitMoveRight;
			} else if (mode == modes.resize) {
				limitLeft = limitResizeLeft;
				limitRight = limitResizeRight;
			}

			//check parents constraints
			if (parent && +parent.end_date < +task.end_date) {
				limitLeft(task, parent);
			}
			if (parent && +parent.start_date > +task.start_date) {
				limitRight(task, parent);
			}

			//check children constraints
			for (var i = 0; i < children.length; i++) {
				var child = gantt.getTask(children[i]);
				if (+task.end_date < +child.end_date) {
					limitLeft(task, child);
				} else if (+task.start_date > +child.start_date) {
					limitRight(task, child)
				}
			}


		});

