  drop VIEW lit_gantt_resources_v  CASCADE;
create or replace view lit_gantt_resources_v as 
SELECT r.s_resource_id AS lit_gantt_resources_v_id,
    r.s_resource_id AS key,
    r.value AS label,
    r.name,
    r.s_resourcetype_id,
    r.m_warehouse_id,
    r.isavailable,
    r.ad_client_id,
    r.ad_org_id,
    r.created,
    r.updated,
    r.createdby,
    r.updatedby,
    r.isactive,
    ''::text AS parent,
    t.DailyCapacity AS dailycapacity
   FROM s_resource r
 
   JOIN s_resourcetype t on t.s_resourcetype_id = r.s_resourcetype_id

  WHERE r.ad_client_id = 1000000::numeric;
