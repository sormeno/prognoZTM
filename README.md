# prognoZTM

#### prognoZTM is demo project for recruitment purposes. It hasn't got any commercial uses.

General goal of the project is to find public transport bottlenecks in any city.
##### Project has got 3 main parts:
- gathering live data (using Python)
- storing and processing gathered data (in MySQl database)
- display processed data (using Django) #TODO



##### Features:
- gather transport data from any city that shares live data through Web API 
- gather weather data through Web API (from any provider)
- gather traffic data using Selenium and image analysis
- use multithreading to gather data in independent threads
- write data to any database
- in case of failure save unwritten data to badfile
- error handling to provide continous running
- loggig for errors and warnings analysis 
- easy extendable with other APIs and database tables
- keep credentials in save KeePass database

##### In current setup (Warsaw, PL) following data sources are used:
- https://api.um.warszawa.pl/api/action/busestrams_get/ (public transport vehicles live position - refreshed every 30s)
- http://api.openweathermap.org/data/2.5/weather (weather live data - refreshed every 30min)
- https://www.google.com/maps (traffic live data - refreshed every 30min)

**Other data sources (other cities data) can be easily applied to this project.**


##### Waiting for development:
- track DB definition on github
- DB procedures for calculating data from staging layer
- preapre frontend layer (display analysed data)
