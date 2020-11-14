
var resourcesStore = gantt.createDatastore({
	name: gantt.config.resource_store,
	type: "treeDatastore",
	initItem: function (item) {
        console.log('item',item)
		item.parent = item.parent || gantt.config.root_id;
		item[gantt.config.resource_property] = item.parent;
		item.open = true;
		return item;
	}
});



resourcesStore.attachEvent("onParse", function(){
    console.log('sono denttro');
	var risorse = [];
	resourcesStore.eachItem(function(res){
        console.log(res)
		if(!resourcesStore.hasChild(res.id)){
			var copy = gantt.copy(res);
			copy.key = res.id;
			copy.label = res.text;
			risorse.push(copy);
		}
	});
    gantt.updateCollection("risorse", risorse);
    console.log(risorse)
});
