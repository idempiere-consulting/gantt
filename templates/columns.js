var textEditor = { type: "text", map_to: "text" };
var constraintTypeEditor = {
			type: "select", map_to: "constraint_type", options: [
				{ key: "asap", label: gantt.locale.labels.asap },
				{ key: "alap", label: gantt.locale.labels.alap },
				{ key: "snet", label: gantt.locale.labels.snet },
				{ key: "snlt", label: gantt.locale.labels.snlt },
				{ key: "fnet", label: gantt.locale.labels.fnet },
				{ key: "fnlt", label: gantt.locale.labels.fnlt },
				{ key: "mso", label: gantt.locale.labels.mso },
				{ key: "mfo", label: gantt.locale.labels.mfo }
			]
		};
    // gantt.getConstraintType("11000001")
    
    var constraintTypes = gantt.config.constraint_types
    gantt.config.columns = [
    // {name:"text",       label:"Task name",  width:"*", tree:true,resize: true ,editor:textEditor},
    {name: "text", label: "Task name", tree: true, width: 230, template: function (task) {
      p=task.progress;
      pf=parseFloat(p);
      pt=pf.toString() + "%"
      if (p == "0")
				return "<div class='zero'>" + task.text + " Da Iniziare  </div>";
      if (pf <= 0.1 )
        return "<div class='progress'>" + task.text + " Iniziato </div>";
       
			if (p == "1")
        return "<div class='finito'>" + task.text + " Completo  </div>";
      
			return task.text + " (" + pt + ")";
		}},
    {name:"start_date", label:"Start time", align:"center", width:80 },
    /* {name:"duration",   label:"Duration",   align:"center", width:30 }, */
    // {name:"S_Resource_ID",      label:"Owner",   align:"center", width:60 },
    /* {
				name: "constraint_type", align: "center", width: 30, template: function (task) {
          console.log('provo a verificare il tipo di constartin')
				return gantt.locale.labels[gantt.getConstraintType(task)];
			}, resize: true, editor: constraintTypeEditor
     */{name:"add",        label:"",           width:44 }
];
