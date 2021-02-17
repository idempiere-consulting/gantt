select c.columnname
from  WS_WebServiceFieldInput fin
join ad_column c on c.ad_column_id=fin.ad_column_id
join  WS_WebServicetype ws on ws.WS_WebServicetype_id=fin.WS_WebServicetype_id
where  ws.value='putActivity' ;

select c.columnname
from  WS_WebServiceFieldOutput fout
join ad_column c on c.ad_column_id=fout.ad_column_id
join  WS_WebServicetype ws on ws.WS_WebServicetype_id=fout.WS_WebServicetype_id
where  ws.value='getTasks' ;

