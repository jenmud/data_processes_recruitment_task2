# Data Processes Recruitment - Sport Stats

This is a script that does some json and xml parsing of sport stats and
generate a summary and additional stats like market price percentage.

## Requirements

The script requires the sample files

* [options.json](https://raw.githubusercontent.com/jenmud/data_processes_recruitment_task2/master/options.json)
* [options.xml](https://raw.githubusercontent.com/jenmud/data_processes_recruitment_task2/master/options.xml)

## Usage

```bash
$ python stats.py -h
usage: stats.py [-h] [--comp-dump FILENAME] [--comp NAME] [--options]
                [--summary] [--least-market-percentage]
                [--largest-market-percentage]
                FILENAME

Generate a stat reports.

positional arguments:
  FILENAME              File containing statics. Supported files as JSON and
                        XML.

optional arguments:
  -h, --help            show this help message and exit
  --comp-dump FILENAME  File to dump competition market prices to. --comp must
                        be given for dump to work.
  --comp NAME           Competition name to search for.
  --options             Show how many options are available.
  --summary             Show a complete summary report.
  --least-market-percentage
                        Show the markets with the least market percentage
  --largest-market-percentage
                        Show the markets with the largest market percentage
```

## Tasks

### How many actual options are available?

To get how many options there are run the script with the `--options` command line flag.

Example using JSON

```bash
$ python stats.py options.json --options
Available options: 543
```


Example using XML

```bash
$ python stats.py options.xml --options
Available options: 543
```

### Calc the Super Rugby market percentage and save it to a csv file

The this option save the output to a csv with the following fields

```
Game,Closes,Name,Calculated Market Percentage
```

```bash
$ python stats.py options.json --comp "Super Rugby" --comp-dump output.csv
```

Example CSV output

```
Game,Closes,Name,Calculated Market Percentage                                                                                                         [28/374]
Highlanders v Sharks,2016-04-22 19:35:00,Match Result,0.010987789987789987
Highlanders v Sharks,2016-04-22 19:35:00,Head to Head-Live betting,0.010702702702702703
Highlanders v Sharks,2016-04-22 19:35:00,Points Start,0.0106951871657754
Highlanders v Sharks,2016-04-22 19:35:00,Winning Team & Margin,0.011764982523496456
Highlanders v Sharks,2016-04-22 19:35:00,Half/Full Time Double,0.012206966692092551
Highlanders v Sharks,2016-04-22 19:35:00,Tri-Bet,0.011157078215901745
2016 Super Rugby,2016-04-22 19:36:00,Outright Winner,0.012167146650133878
2016 Super Rugby,2016-04-22 19:36:00,Pick The Finalists,0.019305001819755183
2016 Super Rugby,2016-04-22 19:36:00,Winning Nationality,0.011253534388847922
2016 Super Rugby,2016-04-22 19:36:00,To Make The Final,0.024067541463318395
2016 Super Rugby,2016-04-22 19:36:00,To Make The Semi-Final,0.04690633346885531
2016 Super Rugby,2016-04-22 19:36:00,To Make The Quarter-Final,0.08749978664888482
2016 Super Rugby,2016-04-22 19:36:00,Regular Season Winner,0.012658695649518784
2016 Super Rugby,2016-04-22 19:36:00,Australasian Group Winner,0.01218546301398927
2016 Super Rugby,2016-04-22 19:36:00,South African Group Winner,0.011589852413381826
2016 Super Rugby,2016-04-22 19:36:00,New Zealand Conference Winner,0.011791556114136759
2016 Super Rugby,2016-04-22 19:36:00,Australia Conference Winner,0.01115220410215326
2016 Super Rugby,2016-04-22 19:36:00,Africa 1 Conference Winner,0.010873173970783533
2016 Super Rugby,2016-04-22 19:36:00,Africa 2 Conference Winner,0.011277105807998258
2016 Super Rugby,2016-04-22 19:36:00,Blues Stage of Elimination,0.011816330885468585
2016 Super Rugby,2016-04-22 19:36:00,Chiefs Stage of Elimination,0.011921985815602838
2016 Super Rugby,2016-04-22 19:36:00,Crusaders Stage of Elimination,0.011967032967032967
2016 Super Rugby,2016-04-22 19:36:00,Highlanders Stage of Elimination,0.011915786827551534
2016 Super Rugby,2016-04-22 19:36:00,Hurricanes Stage of Elimination,0.011915786827551534
2016 Super Rugby,2016-04-22 19:36:00,Blues Regular Season Wins,0.022437927579239233
2016 Super Rugby,2016-04-22 19:36:00,Chiefs Regular Season Wins,0.022345192953487886
2016 Super Rugby,2016-04-22 19:36:00,Crusaders Regular Season Wins,0.022422430510665805
2016 Super Rugby,2016-04-22 19:36:00,Highlanders Regular Season Wins,0.022574813482434994
2016 Super Rugby,2016-04-22 19:36:00,Hurricanes Regular Season Wins,0.022616156117581634
Rebels v Cheetahs,2016-04-22 21:45:00,Match Result,0.01098901098901099
Rebels v Cheetahs,2016-04-22 21:45:00,Head to Head-Live betting,0.010724289715886355
Rebels v Cheetahs,2016-04-22 21:45:00,Points Start,0.0106951871657754
Rebels v Cheetahs,2016-04-22 21:45:00,Winning Team & Margin,0.011760396466278819
Rebels v Cheetahs,2016-04-22 21:45:00,Half/Full Time Double,0.012199780611545316
Rebels v Cheetahs,2016-04-22 21:45:00,Tri-Bet,0.01111111111111111
Sunwolves v Jaguares,2016-04-23 04:00:00,Match Result,0.01095292252550317
Sunwolves v Jaguares,2016-04-23 04:00:00,Head to Head,0.01072595281306715
Sunwolves v Jaguares,2016-04-23 04:00:00,Points Start,0.0106951871657754
Sunwolves v Jaguares,2016-04-23 04:00:00,Winning Team & Margin,0.011677892000472645
Sunwolves v Jaguares,2016-04-23 04:00:00,Half/Full Time Double,0.012216349440033651
Sunwolves v Jaguares,2016-04-23 04:00:00,Tri-Bet,0.011223474801061006
Hurricanes v Chiefs,2016-04-23 19:35:00,Match Result,0.011089166089166089
Hurricanes v Chiefs,2016-04-23 19:35:00,Head to Head-Live betting,0.010702838827838828
Hurricanes v Chiefs,2016-04-23 19:35:00,Winning Team & Margin,0.011754132806764385
Hurricanes v Chiefs,2016-04-23 19:35:00,Half/Full Time Double,0.012213729365263892
Hurricanes v Chiefs,2016-04-23 19:35:00,Tri-Bet,0.011172161172161172
Force v Waratahs,2016-04-23 21:45:00,Match Result,0.011093770841670002
Force v Waratahs,2016-04-23 21:45:00,Head to Head-Live betting,0.010748299319727893
Force v Waratahs,2016-04-23 21:45:00,Points Start,0.0106951871657754
Force v Waratahs,2016-04-23 21:45:00,Winning Team & Margin,0.01176039646627882
Force v Waratahs,2016-04-23 21:45:00,Half/Full Time Double,0.012199780611545316
Force v Waratahs,2016-04-23 21:45:00,Tri-Bet,0.01111111111111111
Stormers v Reds,2016-04-24 01:00:00,Match Result,0.010963669348227366
Stormers v Reds,2016-04-24 01:00:00,Head to Head-Live betting,0.0107543194268858
Stormers v Reds,2016-04-24 01:00:00,Points Start,0.0106951871657754
Stormers v Reds,2016-04-24 01:00:00,Winning Team & Margin,0.011715213169869286
Stormers v Reds,2016-04-24 01:00:00,Half/Full Time Double,0.01226601264002839
Stormers v Reds,2016-04-24 01:00:00,Tri-Bet,0.011173160173160173
Kings v Lions,2016-04-24 03:10:00,Head to Head,0.010679127725856698
Kings v Lions,2016-04-24 03:10:00,Points Start,0.010683760683760684
Kings v Lions,2016-04-24 03:10:00,Winning Team & Margin,0.011754334989629108
Kings v Lions,2016-04-24 03:10:00,Half/Full Time Double,0.012214882943143813
Kings v Lions,2016-04-24 03:10:00,Tri-Bet,0.011141242937853107
Brumbies v Crusaders,2016-04-24 18:05:00,Match Result,0.01106060606060606
Brumbies v Crusaders,2016-04-24 18:05:00,Head to Head-Live betting,0.010718294051627384
Brumbies v Crusaders,2016-04-24 18:05:00,Points Start,0.010702838827838828
Brumbies v Crusaders,2016-04-24 18:05:00,Winning Team & Margin,0.011724245253657018
Brumbies v Crusaders,2016-04-24 18:05:00,Half/Full Time Double,0.012229509379509378
Brumbies v Crusaders,2016-04-24 18:05:00,Tri-Bet,0.01112708719851577
```

### Generate a summary of all sports, and a summary of all available markets

The following option will print the summary to screen in the format

```
<Sport Name>
  <Market Name>: <Total Count>
```

```bash
$ python stats.py options.json --summary
American Football
  Super Bowl 51 Winner: 1
Aussie Rules
  Head to Head: 4
  Points Start: 9
  Top 8 Finish: 1
  Outright Winner: 1
  1st Scoring Play: 9
  Winning Team & Margin: 9
  Head to Head-Live betting: 5
  1st Scoring Play-2nd Half: 9
Baseball
  2016 World Series-Outright Winner: 1
  Run Line: 7
  Total Combined Runs: 7
  American League Winner: 1
  1st Innings Betting: 2
  Head to Head: 5
  National League Winner: 1
  Head to Head-Live betting: 2
Basketball
  Half/Full Time Double: 3
  Western Conference Winner: 1
  Points Start: 3
  Series Winner: 8
  Total Combined Points: 3
  NBA Championship Winner: 1
  Eastern Conference Winner: 1
  Head to Head-Live betting: 3
  Correct Series Score: 8
  Winning Team & Margin: 3
Boxing
  Head to Head: 2
Cricket
  KOLKATA Top Runscorer: 1
  Head to Head: 1
  KINGS XI Top Runscorer: 1
  Outright Winner: 1
Cycling
  Outright Winner: 1
Darts
  Outright Winner (5/2/16-20/05/16): 1
FOB Racing
  Futures Win: 2
  Most NZ Wins (2015/16 Season): 1
  2015/16 NZ Season: 1
Football
  Half/Full Time Double: 9
  Total Goals-1st Half: 1
  Head to Head-Live Now: 1
  1st Half Betting: 9
  Handicap: 13
  Handicaps: 9
  Exact Score: 9
  Total Goals-Live Now: 1
  Winner of Match: 4
  Head to Head-Live betting: 7
  Total Goals: 22
  1st Goal/Result: 9
  Time of 1st Goal: 7
  Total Corners-Live Now: 1
  Total Goals-1st Half-Live Now: 1
  Winning Margin: 9
  Head to Head: 75
  Score Betting: 9
  Outright Winner: 12
Golf
  Will Lydia Ko Win Another Major in 2016?: 1
  Outright Winner: 2
Ice Hockey
  Goal Start: 7
  Western Conference Winner: 1
  Serries Winner: 1
  Series Winner: 7
  Stanley Cup Winner: 1
  Total Combined Goals: 7
  Head to Head: 7
  Eastern Conference Winner: 1
  Correct Series Score: 8
Mixed Martial Arts
  Head to Head: 3
Motorcycling
  Outright Winner: 1
Motorsport
  Drivers Championship: 1
  Outright Winner: 1
  Constructors Championship: 1
Rugby League
  Grand Final Winner (Oct 2016): 1
  Grand Final Winner: 1
Rugby Union
  Half/Full Time Double: 8
  Regular Season Winner: 1
  Tri-Bet: 8
  Correct Test Series Score: 1
  Chiefs Regular Season Wins: 1
  Winning Nationality: 1
  Gold Medal Winner: 1
  New Zealand Conference Winner: 1
  Africa 2 Conference Winner: 1
  Head to Head-Live betting: 6
  Winning Team & Margin: 8
  To Make The Semi-Final: 1
  Hurricanes Stage of Elimination: 1
  Pick The Finalists: 1
  Match Result: 7
  Highlanders Regular Season Wins: 1
  Crusaders Stage of Elimination: 1
  To Make The Quarter-Final: 1
  Blues Stage of Elimination: 1
  Blues Regular Season Wins: 1
  Australasian Group Winner: 1
  To Make The Final: 1
  Crusaders Regular Season Wins: 1
  Hurricanes Regular Season Wins: 1
  Test Series Winner: 1
  Outright Winner: 6
  Highlanders Stage of Elimination: 1
  Points Start: 8
  Chiefs Stage of Elimination: 1
  South African Group Winner: 1
  Africa 1 Conference Winner: 1
  Head to Head: 3
  Australia Conference Winner: 1
Snooker
  Head to Head: 6
Surfing
  Outright Winner: 2
Tennis
  Head to Head: 48
  Outright Winner: 3
  Total Games in Match: 25
```

### What option has the smallest market percentage and the largest?


Getting the largets with flag `--largest-market-percentage` or `--largest` for shorthand

```bash
$ python stats.py options.json --largest
Competition with the largest market price: Super Rugby
```


Getting the smallest with flag `--least-market-percentage` or `--least` for shorthand

```bash
$ python stats.py options.json --least
Competition with the least market price: NBA Playoffs-Rd 1 Series
```
