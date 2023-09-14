<img src=https://s11.gifyu.com/images/S4EID.gif alt="Parsing_Tgstat">
-----------------------------------------------

Chrome Version 116 REQUIRED

-----------------------------------------------
Start command examples:

python tgstat_parser.py -o 1 (for one keyword)
python tgstat_parser.py -o 2 (for 2 keywords)

You can add as much keywords as you need, browser will run in multiple threads

-----------------------------------------------
Instance settings:
-----------------------------------------------
(-k) keyword: Keyword for searching groups (REQUIRED)

default: None

example: -k Culture

-----------------------------------------------
(-fn) filename: Name of the output file

default: None

example: -fn channels_culture

-----------------------------------------------
(--subs) subs: Amount of subscribers (min, max)

default: None (no subs filter)

example: --subs (100, 500)

-----------------------------------------------
(--grps_amount) grps_amount: MAX Amount of groups for search

default: None (all groups)

example: --grps_amount 100

-----------------------------------------------
(--region) region: Channel Region for search

default: Russia

example: --region Africa

-----------------------------------------------
(--verify) verify: Only Verified groups

default: None

example: --verify True

-----------------------------------------------
(--output) output: Output file format (json, csv)

default: json

example: --output csv

-----------------------------------------------
(--runmode) runmode: Run mode (Window or Headless)

default: Window

example: --runmode headless
