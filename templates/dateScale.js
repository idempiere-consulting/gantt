

function setScaleConfig(value) {
  switch (value) {
    case "1":
      gantt.config.scale_unit = "day";
      gantt.config.step = 1;
      gantt.config.date_scale = "%d %M";
      gantt.config.subscales = [];
      gantt.config.scale_height = 27;
      gantt.templates.date_scale = null;
      break;
    case "2":
      var weekScaleTemplate = function (date) {
        var dateToStr = gantt.date.date_to_str("%d %M");
        var startDate = gantt.date.week_start(new Date(date));
        var endDate = gantt.date.add(gantt.date.add(startDate, 1, "week"), -1, "day");
        return dateToStr(startDate) + " - " + dateToStr(endDate);
      };

      gantt.config.scale_unit = "week";
      gantt.config.step = 1;
      gantt.templates.date_scale = weekScaleTemplate;
      gantt.config.subscales = [
        {unit: "day", step: 1, date: "%D"}
      ];
      gantt.config.scale_height = 50;
      break;
    case "3":
      gantt.config.scale_unit = "month";
      gantt.config.date_scale = "%F, %Y";
      gantt.config.subscales = [
        {unit: "day", step: 1, date: "%j, %D"}
      ];
      gantt.config.scale_height = 50;
      gantt.templates.date_scale = null;
      break;
    case "4":
      gantt.config.scale_unit = "year";
      gantt.config.step = 1;
      gantt.config.date_scale = "%Y";
      gantt.config.min_column_width = 50;

      gantt.config.scale_height = 90;
      gantt.templates.date_scale = null;


      gantt.config.subscales = [
        {unit: "month", step: 1, date: "%M"}
      ];
      break;
  }
}

setScaleConfig('4');
gantt.render();
function customSetScale(value){
  setScaleConfig(value);
  gantt.render();
  gantt.message({ text: "imposto la scala", expire: 1000 });

}

//gantt.config.autosize = "xy";
gantt.config.row_height =40 ;
function rowHeightDecrease(){
  if(gantt.config.row_height > 20){
    gantt.config.row_height = gantt.config.row_height-10;
  }
  gantt.render()
}
function rowHeightIncrease(){
  if(gantt.config.row_height < 100){
    gantt.config.row_height = gantt.config.row_height+10;
  }
  gantt.render()
}


