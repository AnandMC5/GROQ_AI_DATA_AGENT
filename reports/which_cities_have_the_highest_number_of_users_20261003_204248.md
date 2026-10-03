# Data Analysis Report  

## Executive Summary  
The analysis shows that **Toronto** has the highest number of users in the dataset, with **1,283** users. The top eight cities are all within a relatively narrow range, each hosting between **1,198** and **1,283** users.

## Business Question  
*Which cities have the highest number of users?*

## Analysis Performed  
The `public.users` table was grouped by **city** and the number of rows (users) per city was counted. The results were sorted in descending order of user count, and the top records were returned.

## SQL Query  

```sql
SELECT
    city,
    COUNT(*) AS user_count
FROM
    public.users
GROUP BY
    city
ORDER BY
    user_count DESC
LIMIT 10;
```

## Results  

| City      | User Count |
|-----------|------------|
| Toronto   | 1,283 |
| Montreal  | 1,279 |
| Ottawa    | 1,264 |
| Edmonton  | 1,253 |
| Halifax   | 1,252 |
| Vancouver | 1,239 |
| Winnipeg  | 1,232 |
| Calgary   | 1,198 |

## Key Findings  

- **Toronto** leads with the highest user count (1,283).  
- The top eight cities are all within **85 users** of each other, indicating a relatively even distribution among major Canadian cities.  
- No city outside the listed eight appears in the top 10, suggesting that user concentration is primarily in these urban centers.  

## Conclusion  
Based on the supplied data, Toronto is the city with the most users, followed closely by Montreal and Ottawa. The user base is fairly evenly distributed across the eight leading Canadian cities identified.