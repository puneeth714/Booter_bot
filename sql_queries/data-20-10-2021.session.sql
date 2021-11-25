select time_fetch,present,signal from parameter
where  signal='buy';

select time_fetch,present,signal from parameter
where signal='sell';


select count(*) , coin from parameter
group by coin
order by count(*) DESC;

-- Language: sql

--group coins with maximum count of change attribute
select count(*) , coin from parameter
group by coin
order by count(*) DESC;