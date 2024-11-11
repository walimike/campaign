# campaign
To run this script here is what to do
-> Setup a virtual env with python 3
-> pip install -r requirements.txt
-> python run.py --date_from 2018-12-31 --date_to 2019-01-01

Imagine the data from the s3 files were in 2 tables: cost_report and revenue_report. Write an SQL query that
returns the same output as the python script.
```
WITH merged_data AS (
  SELECT
    r.data_date,
    r.campaign_id,
    r.campaign_name,
    r.revenue,
    c.cost,
    c.clicks  -- Using clicks directly from cost_report
  FROM
    revenue_report r
  JOIN
    cost_report c
  ON
    r.data_date = c.data_date AND r.campaign_id = c.campaign_id
  WHERE
    r.data_date >= '2018-12-31' AND r.data_date <= '2019-01-01'  -- Replace with desired dates
),

calculated_metrics AS (
  SELECT
    data_date,
    campaign_id,
    campaign_name,
    revenue,
    cost,
    clicks,
    (revenue - cost) AS total_profit,
    (revenue / NULLIF(clicks, 0)) AS UV,                -- Revenue per click
    (cost / NULLIF(clicks, 0)) AS CPC,                  -- Cost per click
    ((revenue / NULLIF(clicks, 0)) / NULLIF((cost / NULLIF(clicks, 0)), 0)) AS ROI  -- Return on investment
  FROM
    merged_data
)

SELECT
  TO_CHAR(data_date, 'YYYY/MM/DD') AS date,             -- Format date for output
  campaign_id,
  campaign_name,
  SUM(revenue) AS total_revenue,                         -- Total revenue
  SUM(cost) AS total_cost,                               -- Total cost
  SUM(total_profit) AS total_profit,                     -- Total profit
  SUM(clicks) AS total_clicks,                           -- Total clicks
  AVG(CPC) AS avg_cpc,                                   -- Average cost per click
  AVG(ROI) AS total_roi,                                 -- Average ROI
  AVG(revenue) AS hourly_avg_revenue                     -- Average hourly revenue
FROM
  calculated_metrics
GROUP BY
  TO_CHAR(data_date, 'YYYY/MM/DD'), campaign_id, campaign_name
ORDER BY
  date, campaign_id;
```

Improvements to be made
- Better error handling for wrong inputs
- Writing of tests