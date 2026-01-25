-- Active: 1769327443937@@127.0.0.1@3306@supply_chain
select *from supply_chain

-- Data understanding
-- check total records
-- check unique skus
-- check missing values in key columns

select count(*) as total_records
from supply_chain

select DISTINCT SKU 
from supply_chain


select 
    sum(CASE WHEN 'Product type' is null then 1 else 0 end) as missing_product,
    sum(case when 'location' is null then 1 else 0 end) as missing_location,
    sum(case when 'Number of products sold' is null then 1 else 0 end) as missing_sold_product
from supply_chain     