# StormGlass-API
Twisted agent script for StromGlass API requests.

# **How to run:**
> git clone https://github.com/romagb/StormGlass-API.git

> cd StormGlass-API

> python stormglass_req.py `parameters for request`, F.E.: `airTemperature pressure`

By default this script returns data for 5 cities:
* Kyiv
* Lviv
* Paris
* Austin
* New York

If you want to get data for any other point, you should change `lattitude` and `longitude` in `stormglass_req.py` or `stormglassReq_gen.py` file for particular city.
