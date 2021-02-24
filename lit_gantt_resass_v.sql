   drop VIEW lit_gantt_resass_v  CASCADE;
create or replace view lit_gantt_resass_v as 

 
 SELECT 10000000::numeric + h.s_resourceassignment_id AS lit_gantt_resass_v_id,
    10000000::numeric + h.s_resourceassignment_id AS id,
    h.description AS text,
    h.assigndatefrom AS start_date,
    NULL::timestamp without time zone AS end_date,
    h.s_resource_id AS owner,
    h.s_resource_id,
    h.c_contactactivity_id + 90000000::numeric AS parent,
        CASE
            WHEN h.isconfirmed = 'Y'::bpchar THEN '1'::text
            WHEN h.isconfirmed = 'N'::bpchar THEN '0'::text
            ELSE '0.5'::text
        END AS progress,
    's_resourceassignment'::text AS table_from,
    'task'::text AS type,
    '0'::text AS sortorder,
    h.isactive,
    1000006 AS ad_client_id,
    h.updated,
    h.updatedby,
    h.qty AS duration,
    h.name AS description,
    ''::character varying AS ctype
   FROM s_resourceassignment h
   where date_part('year'::text, assigndatefrom)<= '2004'
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
    'project'::text AS type,
    '0'::text AS sortorder,
    c.isactive,
    1000006 AS ad_client_id,
    c.updated,
    c.updatedby,
    NULL::numeric AS duration,
    c.description,
    c.contactactivitytype AS ctype
   FROM c_contactactivity c
     JOIN r_status r ON c.r_status_id = r.r_status_id
  WHERE c.c_contactactivity_id = 1002093::numeric
  ORDER BY 4;
