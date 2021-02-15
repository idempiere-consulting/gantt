 -- drop VIEW lit_gantt_resources_v  CASCADE;
create or replace view lit_gantt_resources_v as 
SELECT s_resource.s_resource_id AS lit_gantt_resources_v_id,
    s_resource.s_resource_id AS id,
    s_resource.value AS text,
    s_resource.name,
    s_resource.s_resourcetype_id,
    s_resource.m_warehouse_id,
    s_resource.isavailable,
    s_resource.ad_client_id,
    s_resource.ad_org_id,
    s_resource.created,
    s_resource.updated,
    s_resource.createdby,
    s_resource.updatedby,
    s_resource.isactive,
    ''::text AS parent,
    t.DailyCapacity AS dailycapacity
   FROM s_resource s_resource
   JOIN s_resource     r on r.s_resource_id     = s_resource.s_resource_id
   JOIN s_resourcetype t on t.s_resourcetype_id = r.s_resourcetype_id

  WHERE s_resource.ad_client_id = 1000006::numeric;
