create TABLE parameter_.1(
    present FLOAT,
    check_with FLOAT,
    to_check FLOAT,
    signal VARCHAR
);



insert into parameter_0_01 values(0.6244,0.6239,0.0050768737988380885,'sell');
drop table *;

SELECT name FROM sqlite_master WHERE type='table' AND name='parameter_2';




INSERT INTO parameter_01_02 (present, check_with, to_check, signal)
VALUES (
    'present:FLOAT',
    'check_with:FLOAT',
    'to_check:FLOAT',
    'signal:VARCHAR'
  );


  INSERT INTO parameter_01_02 (present, check_with, to_check, signal)
  VALUES (
      '1',
      '1',
      '1',
      'signal:CHAR'
    );


create table buy_sell_signals(
  time TIMESTAMP,
  symbol VARCHAR,
  upper_side VARCHAR,
  lower_side VARCHAR,
  time_taken NUM

);


drop table buy_sell_signals;


SELECT * FROM parameter

group by check_with
order by time_fetch;






insert into buy_sell_signals values(CURRENT_TIMESTAMP,'BNBETH','0.01','0.02','3.1844537258148193');


INSERT INTO buy_sell_signals (time, symbol, upper, lower, time_taken)
VALUES (
    'CURRENT_TIMESTAMP',
    'BNBETH',
    '0.01',
    '0.02',
    '3.1844537258148193'
  );


select * from buy_sell_signals;


drop table buy_sell_signals;