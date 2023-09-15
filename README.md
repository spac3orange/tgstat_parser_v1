![me](https://github.com/spac3orange/tgstat_parser_v1/blob/master/example.gif)

-----------------------------------------------
Simple script for parsing channels from tgstat.com

Based on Selenium

Output in JSON or CSV

Chrome Version 116 REQUIRED

-----------------------------------------------

After the first launch of the script, the tgstat.com page will be opened, on which you will need to log in through the Telegram client

When you log in to the site script will collect cookies and save them in the folder /cookies

Authorization will no longer be required when the script is restarted

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
