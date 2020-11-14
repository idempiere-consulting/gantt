
 gantt.config.lightbox.sections = [
 {name: "description", height: 38, map_to: "text", type: "textarea", focus: true},
 {name: "owner_id", height: 22, map_to: "owner_id", type: "select", options: gantt.serverList("options", [
    {key: 1000004, label: "Marco"},
    {key: 1000005, label: "Andrea"},
    {key: 1000006, label: "Mauro"}])},
 {name: "type", height: 22, map_to: "type", type: "select", options: gantt.serverList("options", [
    {key: 'project', label: "project"},
    {key: 'task', label: "task"},
    {key: 'milestone', label: "milestone"}]


 )},
	{name: "time", type: "duration", map_to: "auto"}
];
