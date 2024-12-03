from herbie import Herbie
from metpy.units import units
import pandas as pd
import numpy as np
import xarray
import itertools
import time
import multiprocessing
from functools import partial

point = pd.DataFrame.from_dict({
  "longitude": [-105.85], 
  "latitude": [40.22], 
  "stid": ["smr"]
  }, 
  orient="columns")

def get_data(df, point):
    extracted = df.herbie.pick_points(points = point, method = "nearest")
    return extracted.to_dataframe()

def get_gefs025(date, member, fxx, point):
    dt = str(date + " 06:00") # 6UTC is approximately midnight here
    H = Herbie(dt, model='gefs', product="atmos.25", member = member, fxx = fxx, verbose=False)
    ds = H.xarray("[U|V]GRD|TMP|TMIN|TMAX|RH|DSWRF")
    result = [get_data(df, point) for df in ds]
    result = pd.concat(result, axis=1)
    unknown_positions = [i for i, col in enumerate(result.columns) if 'unknown' in col.lower()]
    new_names = ["tmax", "tmin"]
    rename_dict = {result.columns[pos]: new_name for pos, new_name in zip(unknown_positions, new_names)}
    result = result.rename(columns=rename_dict)
    cols = result.columns
    mask = ~cols.duplicated(keep='first')
    result = result.loc[:, mask]
    return result

def get_gefs025_for_date(date, member_list, fxx_list, point):
    print(f"Beginning extraction of forecasts for {date}")
    results = []
    try:
        for member, fxx in itertools.product(member_list, fxx_list):
            result = get_gefs025(date, member, fxx, point)
            results.append(result)
        
        final_result = pd.concat(results, keys=[(m, f) for m, f in itertools.product(member_list, fxx_list)])
        
        output_path = f"/Users/steeleb/Documents/GitHub/ATS-Data-Driven-Forecasting/data/herbie_extraction/GEFS_2023/GEFS_p25_{date}.csv"
        final_result.to_csv(output_path, index=False)
        print(f"Successfully saved data for {date}")
        return None
    except Exception as e:
        print(f"Error processing date {date}: {str(e)}")
        return date

def process_all_dates(date_sequence, member_list, fxx_list, point):
    num_processes = multiprocessing.cpu_count() - 1
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        process_func = partial(get_gefs025_for_date, member_list=member_list, fxx_list=fxx_list, point=point)
        results = pool.map(process_func, date_sequence)
    
    missing_dates = [date for date in results if date is not None]
    with open('/Users/steeleb/Documents/GitHub/ATS-Data-Driven-Forecasting/data/herbie_extraction/missing_dates.txt', 'w') as f:
        for date in missing_dates:
            f.write(f"{date}\n")

if __name__ == '__main__':
    DATESEQUENCE = [date.strftime('%Y-%m-%d') for date in pd.date_range("2023-06-01", "2023-10-15")]
    member_list  = ("c00", "p01", "p02", "p03", "p04", "p05", "p06",
                    "p07", "p08", "p09", "p10", "p11", "p12", "p13", 
                    "p14", "p15", "p16", "p17", "p18", "p19", "p20",
                    "p21", "p22", "p23", "p24", "p25", "p26", "p27",
                    "`p28", "p29", "p30")
    fxx_list = list(np.arange(0, 169, 3, dtype="object"))
    process_all_dates(DATESEQUENCE, member_list, fxx_list, point)


""" if __name__ == '__main__':
    # list missing dates
    missing_dates = ("2023-06-19", "2023-06-20", "2023-06-22","2023-07-04", "2023-07-17",
                     "2023-07-25", "2023-07-06", "2023-09-19", "2023-09-21", "2023-09-22", 
                     "2023-09-24", "2023-09-25", "2023-09-27", "2023-09-28", "2023-09-30", 
                     "2023-10-01")
    # create pandas dates from missing dates
    leftover = [date.strftime('%Y-%m-%d') for date in pd.to_datetime(missing_dates)]
    DATESEQUENCE = [date.strftime('%Y-%m-%d') for date in pd.date_range("2023-10-03", "2023-10-15")]
    # add leftover to datesequence
    DATESEQUENCE.extend(leftover)
    member_list  = ("c00", "p01", "p02", "p03", "p04", "p05", "p06",
                    "p07", "p08", "p09", "p10", "p11", "p12", "p13", 
                    "p14", "p15", "p16", "p17", "p18", "p19", "p20",
                    "p21", "p22", "p23", "p24", "p25", "p26", "p27",
                    "p28", "p29", "p30")
    fxx_list = list(np.arange(0, 169, 3, dtype="object"))
    process_all_dates(DATESEQUENCE, member_list, fxx_list, point)
"""