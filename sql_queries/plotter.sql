-- select time_fetch,present,signal from parameter 
-- where coin='POLYUSDT';

-- select time_fetch,present,signal from parameter 
-- where signal='buy' and coin='ADAUSDT' ;

-- select time_fetch,present,signal from parameter
-- where signal='sell' and coin='ADAUSDT';



-- select time_fetch,present,signal from parameter
-- where signal='buy' and change='01_02';
-- select time_fetch,present,signal from parameter
-- where  signal='sell' and change='01_02';

-- select * from parameter
-- where   signal='buy';
-- select * from parameter
-- where   signal='sell';


-- select time_fetch,present,signal,LEAD(signal,1) over(order by time_fetch) as next_is from parameter
-- where coin='BTCUSDT' and signal!=(SELECT LEAD(signal,1) over(order by time_fetch) as next_is from parameter);

-- select time_fetch,change from parameter;

-- select coin ,count(*)from parameter
-- group by coin
-- order by count(*);

-- select * from buy_sell_signals;

-- select * from parameter;

-- select * from buy_sell_signals;

-- SELECT * FROM parameter WHERE signal='buy' and change='01_02';
-- SELECT * FROM parameter WHERE signal='sell' and change='01_02';
-- SELECT * FROM parameter WHERE signal='buy' and change='02_03';
-- SELECT * FROM parameter WHERE signal='sell' and change='02_03';
-- SELECT * FROM parameter WHERE signal='buy' and change='03_04';
-- SELECT * FROM parameter WHERE signal='sell' and change='03_04';
-- SELECT * FROM parameter WHERE signal='buy' and change='04_05';
-- SELECT * FROM parameter WHERE signal='sell' and change='04_05';
-- SELECT * FROM parameter WHERE signal='buy' and change='05_06';
-- SELECT * FROM parameter WHERE signal='sell' and change='05_06';
-- SELECT * FROM parameter WHERE signal='buy' and change='06_07';
-- SELECT * FROM parameter WHERE signal='sell' and change='06_07';
-- SELECT * FROM parameter WHERE signal='buy' and change='07_08';
-- SELECT * FROM parameter WHERE signal='sell' and change='07_08';
-- SELECT * FROM parameter WHERE signal='buy' and change='08_09';
-- SELECT * FROM parameter WHERE signal='sell' and change='08_09';


-- select * from buy_sell_signals where change='01_02';
-- select * from parameter where change='02_03';
-- select * from parameter where change='03_04';
-- select * from parameter where change='04_05';
-- select * from parameter where change='05_06';
-- select * from parameter where change='06_07';
-- select * from parameter where change='07_08';
-- select * from parameter where change='08_09';


-- SELECT * from buy_sell_signals where change='01_02';
-- SELECT * from buy_sell_signals where change='02_03';
-- SELECT * from buy_sell_signals where change='03_04';
-- SELECT * from buy_sell_signals where change='04_05';
-- SELECT * from buy_sell_signals where change='05_06';
-- SELECT * from buy_sell_signals where change='06_07';
-- SELECT * from buy_sell_signals where change='07_08';
-- SELECT * from buy_sell_signals where change='08_09';


SELECT * FROM parameter WHERE signal='buy' and change='01_02';
SELECT * FROM parameter WHERE signal='sell' and change='01_02';