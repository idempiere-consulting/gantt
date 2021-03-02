   drop VIEW lit_gantt_resass_v  
   CASCADE;
create or replace view lit_gantt_resass_v as 

 
 SELECT 10000000::numeric + h.s_resourceassignment_id AS lit_gantt_resass_v_id,
    10000000::numeric + h.s_resourceassignment_id AS id,
    coalesce(NULLIF(h.name,''),h.description) AS text,
    h.assigndatefrom AS start_date,
    --h.assigndateto   AS end_date,
    -- sono costretto a scegliere solo 2 valori tra i tre:
    -- start date,end_date, duration
    -- infatti il dhtmlx calcola il terzo a partire dai due forniti
    NULL::timestamp without time zone AS end_date,
    h.s_resource_id AS owner,
    h.s_resource_id,
    h.c_contactactivity_id + 90000000::numeric AS parent,
    /*     CASE
            WHEN h.isconfirmed = 'Y'::bpchar THEN '1'::text
            WHEN h.isconfirmed = 'N'::bpchar THEN '0'::text
            ELSE '0.5'::text
        END  */
    h.percent::TEXT AS progress,
    's_resourceassignment'::text AS table_from,
    'task'::text AS type,
    '0'::text AS sortorder,
    h.isactive,
    h.updated,
    h.updatedby,
    h.ad_client_id,
    h.qty AS duration,
    COALESCE(h.description, h.name) AS description,
    ''::character varying AS ctype,
    'http://173.249.60.71:6080/webui/index.zul?Action=Zoom&AD_Table_ID=485&Record_ID='||h.s_resourceassignment_id as idlink
   FROM s_resourceassignment h
    where date_part('year'::text, assigndatefrom) > '2020'
   /*AND
    date_part('month'::text, assigndatefrom) = '01'
   
    AND
    h.ad_client_id=1000006
 */    
    --WHERE s_resourceassignment_id=1003049
UNION
 SELECT 90000000::numeric + c.c_contactactivity_id AS lit_gantt_resass_v_id,
    90000000::numeric + c.c_contactactivity_id AS id,
    (c.documentno::text || ' '::text) || c.name::text AS text,
    c.startdate AS start_date,
    COALESCE(c.enddate, date(c.startdate + '08:00:00'::interval)::timestamp without time zone) AS end_date,
    c.salesrep_id AS owner,
    c.salesrep_id AS s_resource_id,
    0 AS parent,
    '0.5'::text AS progress,
    'c_contactactivity'::text AS table_from,
    'task'::text AS type,
    '0'::text AS sortorder,
    c.isactive,
    c.updated,
    c.updatedby,
    c.ad_client_id,    
    NULL::numeric AS duration,
    c.description,
    c.contactactivitytype AS ctype,
    'http://173.249.60.71:6080/webui/index.zul?Action=Zoom&AD_Table_ID=53354&Record_ID'||c.c_contactactivity_id as idlink
   FROM c_contactactivity c
     --JOIN r_status r ON c.r_status_id = r.r_status_id
  WHERE   date_part('year'::text, c.startdate)= '2020'/*
      AND
   date_part('month'::text, c.startdate) = '01'
   
         AND

    c.ad_client_id=1000006
     and c_contactactivity_id=1002341*/
  ORDER BY start_date;
