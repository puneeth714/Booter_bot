SELECT * from buy_sell_signals;

select time,to_check,upper,lower,time_taken from buy_sell_signals
where symbol='ETHUSDT';


select * from parameter
where coin='ETHUSDT';

select time,symbol ,count(*) from buy_sell_signals
group by symbol
order by count(*) desc;

select * from buy_sell_signals where symbol="TRXBTC"
order by time;

select symbol ,time from buy_sell_signals
where symbol="ETHUSDT";

select * from parameter
where coin='BTCUSDT';