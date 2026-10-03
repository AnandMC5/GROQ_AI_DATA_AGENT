# Data Analysis Report  

## Executive Summary  
The analysis shows which riders have taken the most trips. Mary Nelson leads the list with **14 rides**, followed by William Burns and Kimberly Kelly, each with **11 rides**.

## Business Question  
**Which users have taken the most rides?**

## Analysis Performed  
A join between the **rides** and **users** tables was used to count how many rides each user (identified by `rider_id`) has taken. The counts were grouped by user details, ordered from highest to lowest, and the top 10 riders were returned.

## SQL Query  

```sql
SELECT
    u.user_id,
    u.first_name,
    u.last_name,
    COUNT(r.ride_id) AS ride_count
FROM
    public.rides AS r
JOIN
    public.users AS u
    ON u.user_id = r.rider_id
GROUP BY
    u.user_id,
    u.first_name,
    u.last_name
ORDER BY
    ride_count DESC
LIMIT 10;
```

## Results  

| Rank | User ID | First Name | Last Name | Ride Count |
|------|---------|------------|-----------|------------|
| 1 | 9571 | Mary | Nelson | 14 |
| 2 | 3966 | William | Burns | 11 |
| 3 | 2135 | Kimberly | Kelly | 11 |
| 4 | 8067 | Melanie | Beck | 10 |
| 5 | 5455 | Nicholas | Chapman | 10 |
| 6 | 2119 | Edward | Shaffer | 10 |
| 7 | 1287 | Robert | Anderson | 9 |
| 8 | 8039 | Dwayne | Rodriguez | 9 |
| 9 | 193 | Richard | Phillips | 9 |
|10 | 971 | Robert | Mack | 9 |

## Key Findings  

- **Top rider:** Mary Nelson with 14 rides.  
- Two riders (William Burns, Kimberly Kelly) are tied for second place with 11 rides each.  
- Three riders (Melanie Beck, Nicholas Chapman, Edward Shaffer) each have 10 rides.  
- The remaining four riders in the top‑10 have 9 rides each.

## Conclusion  
Based on the current ride data, Mary Nelson is the most frequent rider, and a small group of users (2‑3 individuals) account for the next highest ride totals. These insights can help focus loyalty or reward programs on the most active customers.