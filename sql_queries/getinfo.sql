-- -- SELECT * from parameter_09_1
-- -- where signal='buy';


-- -- select    CURRENT_TIMESTAMP;


-- SELECT * from parameter
-- where change='02_03'
-- -- where coin LIKE '%USDT' and signal= 'buy'
-- order by   coin ASC;


-- select * from parameter where change='09_1' and coin like '%USDT'
-- order by coin ASC;


-- select * from parameter where time_fetch>2021-10-19 and change='01_02' and coin like '%USDT'
-- ORDER by time_fetch DESC;


select time_fetch,present,signal from parameter
where   change!='0_01' and coin like 'ETHUSDT'
group by present
order by time_fetch ASC;


select COUNT(*) from parameter
where   change!='0_01' 
and signal='buy' and coin like '%BTC'

select COUNT(coin),coin FROM
parameter
group by coin
ORDER by COUNT(coin) DESC;


select time_fetch,present,signal from parameter
where    coin like 'POLYUSDT' and signal='sell'
group by present
order by time_fetch ASC;


select * from parameter where coin='NEARBNB';


SELECT * from parameter
group by present


select COUNT(*),coin from parameter
group by coin;

create table tmp(
    time NUMBER
);
insert into tmp values(strftime('%s', 'now'));
select * from tmp;

select strftime('%s', 'now') as timestamp;


drop table tmp;


select time_fetch,present,coin,change,signal,(select LEAD(signal,1) over (order by time_fetch ASC)  as helper from parameter) from parameter
where ((select LEAD(signal,1) over (order by time_fetch ASC)  as helper from parameter)='buy' and coin='BTCUSDT') or ((select LEAD(signal,1) over (order by time_fetch ASC)  as helper from parameter))='sell'
order by time_fetch ASC;

select  present,change,signal from parameter
WHERE coin="ETHUSDT" 
order by change ASC;


select change,max(all_things) FROM 
(SELECT COUNT(*),change,coin as all_things from parameter
where coin="BTCUSDT" 
group by change
order by change DESC)
group by change;


select change,count(change) from parameter
where count(change)>max(count(change))
group by change
order by change DESC;



select coin,signal,change, max(all_signals)
from (select count(change) as all_signals from parameter
group by change
order by all_signals DESC)
order by change;

select * from parameter
WHERE coin="LTCBTC" and change='1_2'
order by time_fetch ASC;


select max(total) from (
select change,count(change) as total from parameter
group by change
order by total DESC);



select coin , change,counts from (
select coin,change,count() as counts from parameter
group by coin)
order by counts DESC;


select *,count(*) from parameter
where coin="NMRUSDT" and change='1_2';



select *,count(change) from parameter
where coin="NMRUSDT"
and (select count(change),coin from parameter group by coin)
;


select coin ,total from(
select count(*) as total,coin from parameter
where change=max(count(select count(*) from parameter group by coin))
 group by coin);


select changes_in_each_coin from (
select coin,change,count(change) as changes_in_each_coin
from parameter
group by coin)
order by changes_in_each_coin DESC;


select * from parameter
where coin="1INCHBTC";


select coin,total,change from (
select coin, change,count(coin) as total from (
select coin, change,count(change) as changes_in from parameter
group by coin)
group by change)
order by total DESC;



SELECT change,max(total),coin from (
select coin,change,count(change) as total from (
select coin, change from parameter group by coin)
group by change
order by change DESC);



select coin,change,count(in(select change from parameter group by coin)) from parameter
group by coin;


select coin,change,count(change) from parameter
where coin="NMRUSDT" and change="1_2"

select coin,change,signal from parameter
where signal in('buy','sell');


select coin,change,count(change) from parameter
where coin in(select coin from parameter group by coin)
group by coin;


select change,count(*) as count_of_changes from parameter
where coin in(select coin from parameter group by coin)
group by change;

select change,count(*) as count_of from parameter
WHERE change="01_02";


select coin,count(*) as count_of_changes from parameter
where coin in(select coin from parameter group by coin)
group by coin;


select coin,change,counts from (
select change,coin,max(counted) as counts from (
select coin,change,count(*) as counted from parameter
where coin in(select coin from parameter group by coin)
group by change))
group by coin;



select change ,max(num1) from (
select coin,change,count(change) num1 from
parameter where coin in(select coin from parameter group by coin)
group by change)
group by coin;


select change,count(change)
 FROM parameter
 where change="1_2";

select coin,max(itis) from (
select coin,count(change) itis from parameter
where change="1_2"
group by coin);


select coin,count(*) as numberofsignals,sum(numberofsignals) from parameter
group by coin
order by numberofsignals DESC;

select to_check,count(*) from parameter
group by to_check


select sql
from sqlite_master
where name = "parameter"


select to_check,present,check_with from parameter
group by check_with
order by count(*) DESC;

select sum(changes_in) from (
select change,count(change) as changes_in from parameter
group by change
order by count(change) DESC);

SELECT count(*) from
parameter;

select change,count(change) as changes_in from parameter
group by change
order by count(change) DESC

select time_fetch,change from parameter


SELECT time_fetch,signal,change from parameter
WHERE coin="BTCUSDT" and change='3_4';

--select coin , change from parameter table in which 
--each coin has multiple changes values and some of them are equal
--show change value of each coin with max number of repeations each

select count(*),symbol from buy_sell_signals
where symbol = "ETHUSDT"
group by symbol
order by count(*) DESC;

select * from buy_sell_signals
where symbol = "ETHUSDT" or symbol="BTCUSDT" or symbol="SOLUSDT";


select *,count(*)/2000 from parameter;

select * from buy_sell_signals where symbol = "ETHUSDT" ;

select * from parameter where coin = "ETHUSDT";


select * from buy_sell_signals;


select count(*),change from parameter 
group by change
order by count(change) DESC;


SELECT * FROM parameter
WHERE coin="ETHUSDT" and change='1_2';

SELECT COUNT(*),change FROM parameter
GROUP by change
ORDER by count(change) DESC;


SELECT *,count(*) FROM buy_sell_signals
GROUP by upper
ORDER by count(*) DESC;


--alter the column coin in parameter table
ALTER TABLE parameter
RENAME COLUMN coin TO market_pair;

--ALTER the COLUMN symbol in buy_sell_signals table to market_pair
ALTER TABLE buy_sell_signals
RENAME COLUMN symbol TO market_pair;

--Add new columns upper and lower in parameter table and DELETE chande column in parameter table
ALTER TABLE parameter
ADD COLUMN upper TEXT;
ALTER TABLE parameter
ADD COLUMN lower TEXT;
ALTER TABLE parameter
DROP COLUMN change;



--find time taken for each signal in buy_sell_signals table
select * from buy_sell_signals;

SELECT max(time),min(time) FROM buy_sell_signals;

--sum of all the values of to_check in buy_sell_signals table where market_pair = "ETHUSDT" and upper = "0.3" and lower = "0.2"
select count(to_check)*(1000/100)+1000 from buy_sell_signals
where market_pair = "SHIBUSDT" and upper = "0.3" and lower = "0.2";

select count(to_check) from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "0.4" and lower = "0.3";

select count(to_check) from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "0.5" and lower = "0.4";

select count(to_check) from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "0.6" and lower = "0.5";

select count(to_check) from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "0.7" and lower = "0.6";

select count(to_check) from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "0.8" and lower = "0.7";

select count(to_check) from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "0.9" and lower = "0.8";

select * from buy_sell_signals
where market_pair = "ETHUSDT" and upper = "1.0" and lower = "0.9";


