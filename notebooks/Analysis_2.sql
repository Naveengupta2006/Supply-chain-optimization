-- Active: 1769327443937@@127.0.0.1@3306@supply_chain
select * from supply_chain

-- SKU-Level Demand Analysis
--  Total sales by SKU

select 'SKU', sum('Number of products sold') as total_unit_sold, sum('Revenue generated') as total_revenue
from supply_chain
group by 'SKU'
order by total_unit_sold desc

-- product type demand analysis
select 'Product type', sum('Number of products sold') as total_units_sold, sum('Revenue generated') as total_revenue
from supply_chain
group by 'Product type'
order by  total_units_sold

--location based analysis
select "Location", sum('Number of products sold') as total_units_sold, sum('Revenue generated') as total_revenue
FROM supply_chain
group by "Location"
order by total_units_sold

-- customer demographic demand analysis
select 'Customer Demographics', sum('Number of products sold') as total_units_solds, sum('Revenue generated') as total_revenue
from supply_chain
group by 'Customer Demographics'
order by total_units_solds desc

-- forecast gap identification
SELECT
  'SKU',
  'Location',
  SUM('Number of products sold') AS total_sales,
  AVG('Stock levels') AS avg_stock
FROM supply_chain
GROUP BY sku, location
HAVING SUM('Number of products sold') > AVG('Stock levels');


--Overstock Identification

SELECT
  'SKU',
  'Location',
  AVG('Stocks levels') AS avg_stock,
  SUM('Number of products sold') AS total_sales
FROM supply_chain
GROUP BY sku, location
HAVING AVG('Stocks levels') > SUM('Number of products sold');
