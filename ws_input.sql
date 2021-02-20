select c.columnname as mustIN
from  WS_WebServiceFieldInput fin
join ad_column c on c.ad_column_id=fin.ad_column_id
join  WS_WebServicetype ws on ws.WS_WebServicetype_id=fin.WS_WebServicetype_id
where  ws.value='putHourDettaglio' ;
/* 
select c.columnname as mustOUT
from  WS_WebServiceFieldOutput fout
join ad_column c on c.ad_column_id=fout.ad_column_id
join  WS_WebServicetype ws on ws.WS_WebServicetype_id=fout.WS_WebServicetype_id
where  ws.value='getTasks' ;

select column_name as mustEXIST from information_schema.columns 
where table_name='c_contactactivity' 
    and is_nullable='NO' 
    and column_default is  null 
    and column_name not in ('ad_client_id','ad_org_id','createdby','updatedby');
 */