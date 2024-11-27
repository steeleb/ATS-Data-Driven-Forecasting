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
    dt = date 
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

def get_gefs025_control_for_date(date, member_list, fxx_list, point):
    print(f"Beginning extraction of forecasts for {date}")
    results = []
    fn_date = str(date).replace(" ", "_").replace(":", "-")
    try:
        for member, fxx in itertools.product(member_list, fxx_list):
            result = get_gefs025(date, member, fxx, point)
            results.append(result)
        final_result = pd.concat(results, keys=[(m, f) for m, f in itertools.product(member_list, fxx_list)])
        output_path = f"/Users/steeleb/Documents/GitHub/ATS-Data-Driven-Forecasting/data/herbie_extraction/debias/GEFS_p25_control_{fn_date}.csv"
        final_result.to_csv(output_path, index=False)
        print(f"Successfully saved data for {date}")
        return None
    except Exception as e:
        print(f"Error processing date {date}: {str(e)}")
        return date

def process_all_dates(date_sequence, fxx_list, point):
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        process_func = partial(get_gefs025_control_for_date, member_list=["c00"], fxx_list=fxx_list, point=point)
        results = pool.map(process_func, date_sequence)
    missing_dates = [date for date in results if date is not None]
    with open('/Users/steeleb/Documents/GitHub/ATS-Data-Driven-Forecasting/data/herbie_extraction/debias/missing_dates_control.txt', 'a') as f:
        for date in missing_dates:
            f.write(f"{date}\n")

if __name__ == '__main__':
    fxx_list = list(np.arange(0, 4, 3, dtype="object"))
    DATESEQUENCE = pd.date_range("2020-06-01", "2020-10-15", freq="6H")
    process_all_dates(DATESEQUENCE, fxx_list, point)
    DATESEQUENCE = pd.date_range("2021-06-01", "2021-10-15", freq="6H")
    process_all_dates(DATESEQUENCE, fxx_list, point)
    DATESEQUENCE = pd.date_range("2022-06-01", "2022-10-15", freq="6H")
    process_all_dates(DATESEQUENCE, fxx_list, point)
    DATESEQUENCE = pd.date_range("2023-06-01", "2023-10-15", freq="6H")
    process_all_dates(DATESEQUENCE, fxx_list, point)
    DATESEQUENCE = pd.date_range("2024-06-01", "2024-10-15", freq="6H")
    process_all_dates(DATESEQUENCE, fxx_list, point)

