There are a number of ways to get NOAA GEFS data, here I have some code for two 
methods. One is a direct download from AWS and extraction using {stars} in R. The
other is using the Python module herbie, which is more efficient for the 0.25 
degree resolution that we need for our purposes. 

For now, this is just code to grab data at SMR, but could be more generalized. Note,
you can also get HRRR and NAM forecasts from herbie, both of which have a higher
resolution but a shorter forecast period (48 and 72h respectively).

Newer version `multiprocess_herbie_2022.py` uses the multiprocessing module to more
efficiently download and process data. Now that we're aquiring all 3h forecasts for all 
ensemble members, this is a much more efficient way to get the data, reducing compute 
from roughly 10 days to 17 hours. 

For operational use, we'll multiprocess on the member, not the date, to reduce 1.75h 
processing time for operationalization.