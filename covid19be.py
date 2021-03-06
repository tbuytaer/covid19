import pandas as pd
import numpy as np


# Data helpers -===============================================================

def consolidate(v1, v2):
    v1 = {k:v for k, v in v1}
    v2 = {k:v for k, v in v2}
    v2.update(v1)
    return [(k, v) for k, v in v2.items()]

def load_data():
    # The data is fetched directly from Sciensao's spreadsheet, and 
    # consolidated with @vdwnico's original values for the beginning of 
    # the time-series.
    
    # Hospitalizations
    nico_hosps = [
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), 
        (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 27), (15, 97), (16, 163), 
        (17, 265), (18, 368), (19, 496), (20, 649), (21, 842), (22, 1097), (23, 1381), (24, 1644), 
        (25, 1881), (26, 2138), (27, 2718), (28, 3072), (29, 3644), (30, 4081), (31, 4474), (32, 4886), 
        (33, 4979), (34, 5210), (35, 5362), (36, 5497), (37, 5514), (38, 5606), (39, 5744), (40, 5699), 
        (41, 5597), (42, 5618), (43, 5645), (44, 5419), (45, 5423), (46, 5536), (47, 5515), (48, 5309), 
        (49, 5161), (50, 5069), (51, 4871), (52, 4920), (53, 4976), (54, 4765), (55, 4527)] # last == April 22

    df = pd.read_excel("https://epistat.sciensano.be/Data/COVID19BE.xlsx", sheet_name="HOSP")
    sciensano_hosps = df.groupby("DATE")["TOTAL_IN"].sum()   # start on March 15
    last_date = sciensano_hosps.index[-1]
    sciensano_hosps = [(i+17, v) for i, v in enumerate(sciensano_hosps)]
    hosps = consolidate(sciensano_hosps, nico_hosps)
    
    new_in = df.groupby("DATE")["NEW_IN"].sum()
    new_in = [(i+17, v) for i, v in enumerate(new_in)]
    new_in = consolidate(new_in, [(i,0) for i in range(1, 17)])
    
    new_out = df.groupby("DATE")["NEW_OUT"].sum()
    new_out = [(i+17, v) for i, v in enumerate(new_out)]
    new_out = consolidate(new_out, [(i,0) for i in range(1, 17)])
    
    # ICUs
    nico_icus = [
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), 
        (9, 0), (10, 0), (11, 0), (12, 0), (13, 2), (14, 15), (15, 24), (16, 33), 
        (17, 53), (18, 79), (19, 100), (20, 130), (21, 164), (22, 238), (23, 290), (24, 322), 
        (25, 381), (26, 474), (27, 605), (28, 690), (29, 789), (30, 867), (31, 927), (32, 1021), 
        (33, 1088), (34, 1144), (35, 1205), (36, 1245), (37, 1261), (38, 1267), (39, 1260), (40, 1276), 
        (41, 1285), (42, 1278), (43, 1262), (44, 1232), (45, 1234), (46, 1226), (47, 1204), (48, 1182), 
        (49, 1140), (50, 1119), (51, 1081), (52, 1071), (53, 1079), (54, 1020), (55, 993)] 

    df = pd.read_excel("https://epistat.sciensano.be/Data/COVID19BE.xlsx", sheet_name="HOSP")
    sciensano_icus = df.groupby("DATE")["TOTAL_IN_ICU"].sum()   # start on March 15
    sciensano_icus = [(i+17, v) for i, v in enumerate(sciensano_icus)]
    icus = consolidate(sciensano_icus, nico_icus)
    
    # Daily deaths
    nico_deaths = [
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), 
        (9, 0), (10, 0), (11, 0), (12, 0), (13, 1), (14, 3), (15, 3), (16, 5), 
        (17, 5), (18, 10), (19, 10), (20, 19), (21, 25), (22, 27), (23, 36), (24, 46), 
        (25, 75), (26, 69), (27, 91), (28, 91), (29, 115), (30, 128), (31, 133), (32, 158), 
        (33, 172), (34, 238), (35, 193), (36, 224), (37, 269), (38, 225), (39, 267), (40, 299), 
        (41, 321), (42, 275), (43, 323), (44, 283), (45, 338), (46, 270), (47, 262), (48, 266), 
        (49, 240), (50, 191), (51, 98), (52, 22), (53, 170), (54, 266), (55, 230)]

    df = pd.read_excel("https://epistat.sciensano.be/Data/COVID19BE.xlsx", sheet_name="MORT")
    sciensano_deaths = df.groupby("DATE")["DEATHS"].sum()   # start on March 10
    sciensano_deaths = [(i+12, v) for i, v in enumerate(sciensano_deaths)]
    deaths = consolidate(sciensano_deaths, nico_deaths)
    
    # Convert to pandas 
    data = pd.DataFrame({
        "n_hospitalized": [i for _ , i in hosps],
        "n_hospitalized_in": [i for _, i in new_in],
        "n_hospitalized_out": [i for _, i in new_out],
        "n_icu": [i for _, i in icus],
        "n_daily_deaths": [i for _, i in deaths],
        "date": pd.date_range(start="2020-02-28", end=last_date)
    }, index=range(1, len(hosps)+1))
    
    data["n_deaths"] = data["n_daily_deaths"].cumsum()
    
    return data
