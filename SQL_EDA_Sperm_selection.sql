create database icsi_dataset;
/* Importing the dataset through import wizard */

select * from sperm_selection;
/*Changed the datatype of selection_date to date*/

-- Rectifying typo: --
update sperm_selection
set Embryologist_ID = replace(Embryologist_ID, 'EMBA','EMB_A')
WHERE Embryologist_ID = 'EMBA';

select distinct Embryologist_ID from sperm_selection;

update sperm_selection
set Motility_Pattern = replace(Motility_Pattern, 'Progresive','Progressive')
where Motility_Pattern = 'Progresive';

select distinct Motility_Pattern from sperm_selection;


-- Rectifying Formatting mistakes: --
update sperm_selection
set Patient_ID = concat('PT', substring(Patient_ID, 2))
where Patient_ID not like 'PT%' AND Patient_ID LIKE 'P%';

select distinct Patient_ID from sperm_selection;

-- 1st moment business decision: --
-- Mean: --
select 
avg(Sperm_Concentration_M_per_ml) as mean_sperm_concentration,
avg(Total_Motility_Percent) as mean_total_motility,
avg(Progressive_Motility_Percent) as mean_progressive_motility,
avg(Normal_Morphology_Percent) as mean_morphology,
avg(Embryologist_Experience_Years) as mean_embryologist_years,
avg(Selection_Time_Seconds) as mean_selection_time
from sperm_selection;

-- Median: --
-- 1
select avg(Sperm_Concentration_M_per_ml) as median_of_sperm_concentration
from(
select Sperm_Concentration_M_per_ml,
	row_number()over(order by Sperm_Concentration_M_per_ml) as rn,
    count(*) over() as total
from sperm_selection
) t
where rn in ((total+1) div 2, (total+2) div 2);

-- 2
select avg(Total_Motility_Percent) as median_of_total_motility
from(
select Total_Motility_Percent,
	row_number()over(order by Total_Motility_Percent) as rn,
    count(*) over() as total
from sperm_selection
) t
where rn in ((total+1) div 2, (total+2) div 2);

-- 3
select avg(Progressive_Motility_Percent) as median_of_progressive_motility
from(
select Progressive_Motility_Percent,
	row_number()over(order by Progressive_Motility_Percent) as rn,
    count(*) over() as total
from sperm_selection
) t
where rn in ((total+1) div 2, (total+2) div 2);
 
 -- 4
select avg(Normal_Morphology_Percent) as median_of_morphology
from(
select Normal_Morphology_Percent,
	row_number()over(order by Normal_Morphology_Percent) as rn,
    count(*) over() as total
from sperm_selection
) t
where rn in ((total+1) div 2, (total+2) div 2);

-- 5
select avg(Embryologist_Experience_Years) as median_of_embryologist_year
from(
select Embryologist_Experience_Years,
	row_number()over(order by Embryologist_Experience_Years) as rn,
    count(*) over() as total
from sperm_selection
) t
where rn in ((total+1) div 2, (total+2) div 2);

-- 6
select avg(Selection_Time_Seconds) as median_of_Selection_Time
from(
select Selection_Time_Seconds,
	row_number()over(order by Selection_Time_Seconds) as rn,
    count(*) over() as total
from sperm_selection
) t
where rn in ((total+1) div 2, (total+2) div 2);

-- Mode: --
select Motility_Pattern as Mode_motility, count(*) freq
from sperm_selection
group by Motility_Pattern
order by freq desc
limit 1;

select Head_Shape_Score , count(*) freq
from sperm_selection
group by Head_Shape_Score
order by freq desc
limit 1;

select Acrosome_Status , count(*) freq
from sperm_selection
group by Acrosome_Status
order by freq desc
limit 1;

select Midpiece_Assessment , count(*) freq
from sperm_selection
group by Midpiece_Assessment
order by freq desc
limit 1;

select Tail_Assessment , count(*) freq
from sperm_selection
group by Tail_Assessment
order by freq desc
limit 1;

select Vacuoles_Present , count(*) freq
from sperm_selection
group by Vacuoles_Present
order by freq desc
limit 1;

select Fertilization_Success , count(*) freq
from sperm_selection
group by Fertilization_Success
order by freq desc
limit 1;

-- 2nd moment business decision: --
-- Variance: --
select
variance(Sperm_Concentration_M_per_ml) as var_sperm_concentration,
variance(Total_Motility_Percent) as var_total_motility,
variance(Progressive_Motility_Percent) as var_progressive_motility,
variance(Normal_Morphology_Percent) as var_morphology,
variance(Embryologist_Experience_Years) as var_embryologist_years,
variance(Selection_Time_Seconds) as var_selection_time
from sperm_selection;

-- Stanndard Deviation: --
select
stddev(Sperm_Concentration_M_per_ml) as stddev_sperm_concentration,
stddev(Total_Motility_Percent) as stddev_total_motility,
stddev(Progressive_Motility_Percent) as stddev_progressive_motility,
stddev(Normal_Morphology_Percent) as stddev_morphology,
stddev(Embryologist_Experience_Years) as stddev_embryologist_years,
stddev(Selection_Time_Seconds) as stddev_selection_time
from sperm_selection;

-- Range: --
select
max(Sperm_Concentration_M_per_ml) - min(Sperm_Concentration_M_per_ml) as range_sperm_con,
max(Total_Motility_Percent) - min(Total_Motility_Percent) as range_total_motility,
max(Progressive_Motility_Percent) - min(Progressive_Motility_Percent) as range_progressive_m,
max(Normal_Morphology_Percent) - min(Normal_Morphology_Percent) as range_normal_m,
max(Embryologist_Experience_Years) - min(Embryologist_Experience_Years) as range_ex_years,
max(Selection_Time_Seconds) - min(Selection_Time_Seconds) as range_selection_time
from sperm_selection;

-- 3rd moment business decision: --
-- Skewness & Kurtosis: --
-- 1
select
    (
        sum(power(Sperm_Concentration_M_per_ml - (select avg(Sperm_Concentration_M_per_ml) from sperm_selection), 3)) / 
        (count(*) * power((select stddev(Sperm_Concentration_M_per_ml) from sperm_selection), 3))
    ) AS skewness,
    (
        (sum(power(Sperm_Concentration_M_per_ml - (select avg(Sperm_Concentration_M_per_ml) from sperm_selection), 4)) / 
        (count(*) * power((select stddev(Sperm_Concentration_M_per_ml) from sperm_selection), 4))) - 3
    ) as kurtosis
    from sperm_selection;
    
    -- 2 
select
    (
        sum(power(Total_Motility_Percent - (select avg(Total_Motility_Percent) from sperm_selection), 3)) / 
        (count(*) * power((select stddev(Total_Motility_Percent) from sperm_selection), 3))
    ) as skewness,
    (
        (sum(power(Total_Motility_Percent - (select avg(Total_Motility_Percent) from sperm_selection), 4)) / 
        (count(*) * power((select stddev(Total_Motility_Percent) from sperm_selection), 4))) - 3
    ) as kurtosis
    from sperm_selection;
    
    -- 3
select
    (
        sum(power(Progressive_Motility_Percent - (select avg(Progressive_Motility_Percent) from sperm_selection), 3)) / 
        (count(*) * power((select stddev(Progressive_Motility_Percent) from sperm_selection), 3))
    ) as skewness,
    (
        (sum(power(Progressive_Motility_Percent - (select avg(Progressive_Motility_Percent) from sperm_selection), 4)) / 
        (count(*) * power((select stddev(Progressive_Motility_Percent) from sperm_selection), 4))) - 3
    ) as kurtosis
    from sperm_selection;
    
    -- 4 
select
    (
        sum(power(Normal_Morphology_Percent - (select avg(Normal_Morphology_Percent) from sperm_selection), 3)) / 
        (count(*) * power((select stddev(Normal_Morphology_Percent) from sperm_selection), 3))
    ) as skewness,
    (
        (sum(power(Normal_Morphology_Percent - (select avg(Normal_Morphology_Percent) from sperm_selection), 4)) / 
        (count(*) * power((select stddev(Normal_Morphology_Percent) from sperm_selection), 4))) - 3
    ) as kurtosis
    from sperm_selection;
    
    /*---------------------------------------------------------------------------------------------------------------------------------------*/