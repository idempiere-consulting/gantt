drop VIEW lit_gantt_project2_v  CASCADE;
create or replace view lit_gantt_project2_v as 
 SELECT (1::character varying::text || c_project.c_project_id::character varying::text)::numeric AS lit_gantt_project2_v_id,
    c_project.c_project_id,
    0 AS c_projectphase_id,
    0 AS c_projecttask_id,
    0 AS c_projectline_id,
    c_project.datecontract AS start_date,
    c_project.datefinish AS end_date,
    c_project.name AS text,
    c_project.progress,
    '0'::text AS parent,
    c_project.sortorder,
        CASE
            WHEN c_project.projectlinelevel = 'P'::bpchar THEN 'project'::text
            WHEN c_project.projectlinelevel = 'T'::bpchar THEN 'task'::text
            WHEN c_project.projectlinelevel = 'M'::bpchar THEN 'milestone'::text
            ELSE NULL::text
        END AS type,
    c_project.s_resource_id,
    c_project.isactive,
    c_project.ad_client_id,
    c_project.lit_gantt_constraint_type AS constraint_type,
    c_project.lit_gantt_constraint_date AS constraint_date,
    'c_project'::text AS table_from
   FROM c_project
  WHERE c_project.isactive = 'Y'::bpchar
UNION
 SELECT (2::character varying::text || c_projectphase.c_projectphase_id::character varying::text)::numeric AS lit_gantt_project2_v_id,
    0 AS c_project_id,
    c_projectphase.c_projectphase_id,
    0 AS c_projecttask_id,
    0 AS c_projectline_id,
    c_projectphase.startdate AS start_date,
    c_projectphase.enddate AS end_date,
    c_projectphase.name AS text,
    c_projectphase.progress,
    1::character varying::text || c_projectphase.c_project_id::character varying::text AS parent,
    c_projectphase.seqno AS sortorder,
    c_projectphase.type,
    c_projectphase.s_resource_id,
    c_projectphase.isactive,
    c_projectphase.ad_client_id,
    c_projectphase.lit_gantt_constraint_type AS constraint_type,
    c_projectphase.lit_gantt_constraint_date AS constraint_date,
    'c_projectphase'::text AS table_from
   FROM c_projectphase
  WHERE c_projectphase.isactive = 'Y'::bpchar
UNION
 SELECT (3::character varying::text || c_projecttask.c_projecttask_id::character varying::text)::numeric AS lit_gantt_project2_v_id,
    0 AS c_project_id,
    0 AS c_projectphase_id,
    c_projecttask.c_projecttask_id,
    0 AS c_projectline_id,
    c_projecttask.assigndatefrom AS start_date,
    c_projecttask.assigndateto AS end_date,
    c_projecttask.name AS text,
    c_projecttask.progress,
    2::character varying::text || c_projecttask.c_projectphase_id::character varying::text AS parent,
    c_projecttask.seqno AS sortorder,
    c_projecttask.type,
    c_projecttask.s_resource_id,
    'Y'::character varying AS isactive,
    c_projecttask.ad_client_id,
    c_projecttask.lit_gantt_constraint_type AS constraint_type,
    c_projecttask.lit_gantt_constraint_date AS constraint_date,
    'c_projecttask'::text AS table_from
   FROM c_projecttask
  WHERE c_projecttask.isactive = 'Y'::bpchar
UNION
 SELECT (4::character varying::text || c_projectline.c_projectline_id::character varying::text)::numeric AS lit_gantt_project2_v_id,
    0 AS c_project_id,
    0 AS c_projectphase_id,
    0 AS c_projecttask_id,
    c_projectline.c_projectline_id,
    c_projectline.assigndatefrom AS start_date,
    c_projectline.assigndateto AS end_date,
    c_projectline.description AS text,
    '1'::character varying AS progress,
    3::character varying::text || c_projectline.c_projecttask_id::character varying::text AS parent,
    c_projectline.line AS sortorder,
    c_projectline.type,
    c_projectline.s_resource_id,
    c_projectline.isactive,
    c_projectline.ad_client_id,
    c_projectline.lit_gantt_constraint_type AS constraint_type,
    c_projectline.lit_gantt_constraint_date AS constraint_date,
    'c_projectline'::text AS table_from
   FROM c_projectline
  WHERE c_projectline.isactive = 'Y'::bpchar AND c_projectline.c_projecttask_id IS NOT NULL;


