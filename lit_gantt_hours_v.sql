  drop VIEW lit_gantt_hours_v  CASCADE;
create or replace view lit_gantt_hours_v as 
-- 
SELECT 10000000::numeric + h.lit_hour_id AS lit_gantt_hours_v_id,
    10000000::numeric + h.lit_hour_id AS id,
    h.name AS text,
    h.dateworkstart AS start_date,
    h.dateworkstart + '01:00:00'::interval hour * h.qty::double precision AS end_date,
    --to_char(h.dateworkstart, 'yyyy-mm-dd hh24:mi:ss'::text) AS start_date2,
    --to_char(h.dateworkstart + '01:00:00'::interval hour * h.qty::double precision, 'yyyy-mm-dd hh24:mi:ss'::text) AS end_date2,
    --coalesce (h.dateworkstart,date (h.dateworkstart + interval '1000 year')) AS coalesceenddate,
    h.salesrep_id AS owner,
    h.salesrep_id AS s_resource_id,
    h.c_contactactivity_id + 90000000::numeric AS parent,
        CASE
            WHEN h.isconfirmed = 'Y'::bpchar THEN '1'::text
            WHEN h.isconfirmed = 'N'::bpchar THEN '0'::text
            ELSE '0.5'::text
        END AS progress,
    'lit_hour'::text AS table_from,
    'task'::text AS type,
    '0'::text AS sortorder,
    h.isactive  AS isactive,
    1000006 AS ad_client_id,
    h.updated,
    h.updatedby
   FROM lit_hour h
  WHERE h.name IS NOT NULL AND h.dateworkstart::timestamp > (NOW() - INTERVAL '333 days' )
  and
   h.name IS NOT NULL AND h.dateworkstart::timestamp < (NOW() - INTERVAL '332 days' )
   and h.isactive='Y'
UNION
 SELECT 90000000::numeric + c.c_contactactivity_id AS lit_gantt_hours_v_id,
    90000000::numeric + c.c_contactactivity_id AS id,
    (c.documentno::text || ' '::text) || c.name::text AS text,
    c.startdate AS start_date,
    --c.enddate AS end_date,
      --to_char(c.startdate, 'yyyy-mm-dd hh24:mi:ss'::text) AS start_date2,
      --to_char(c.enddate, 'yyyy-mm-dd hh24:mi:ss'::text) AS end_date2,
      coalesce (enddate,date (startdate + interval '8 HOUR')) AS end_date,
      c.salesrep_id AS owner,
      c.salesrep_id AS s_resource_id,
      0 AS parent,
      '0.5'::text AS progress,
      'c_contactactivity'::text AS table_from,
      'project'::text AS type,
      '0'::text AS sortorder,
      c.isactive AS isactive,
      1000006 AS ad_client_id,
      c.updated,
      c.updatedby
   FROM c_contactactivity c
     JOIN r_status r ON c.r_status_id = r.r_status_id
  --WHERE c.name IS NOT NULL  AND c.startdate::timestamp > NOW() - INTERVAL '333 days'
  --where start_date::timestamp > NOW() - INTERVAL '33 days'
  --and
 --c.name IS NOT NULL  AND c.startdate::timestamp > NOW() - INTERVAL '332 days'
 where  (enddate - startdate) > interval '33 days'

  --where start_date < NOW() - INTERVAL '32 days'
  order by start_date asc;
-- è agganciato il trigger per "scivere" sulla vista, verificare funzionamento  
--Triggers:
  --  test_it2 INSTEAD OF UPDATE ON lit_gantt_hours_v FOR EACH ROW EXECUTE FUNCTION test_trigger()

