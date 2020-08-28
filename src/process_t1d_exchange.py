import pandas as pd
import numpy as np
import utils
from pathlib import Path
import math

base_path = Path(__file__).parent
isf_icr_path = (
    base_path
    / "../data/HDeviceWizard.csv"
).resolve()
age_path = (
    base_path
    / "../data/HPtRoster.csv"
)
demographics_path = (
    base_path
    / "../data/HScreening.csv"
)

icr_isf_df = pd.read_csv(isf_icr_path)
age_df = pd.read_csv(age_path)
demographics_df = pd.read_csv(demographics_path)

# Keys for working with exports
""" T1D Exchange """
# tdd_key = "total_daily_dose_avg"
# basal_key = "total_daily_basal_insulin_avg"  # Total daily basal
# carb_key = "total_daily_carb_avg"  # Total daily CHO
bmi_key = "bmi"
weight_key = "Weight" # in cm
height_key = "Height" # in lbs
isf_key = "InsulinSensitivity"
icr_key = "InsulinCarbRatio"
age_key = "AgeAsOfEnrollDt"
# tir_key = "percent_70_180_2week"

relevent_data = icr_isf_df[[isf_key, icr_key]]
relevent_data[age_key] = age_df[age_key]
relevent_data[bmi_key] = demographics_df[[height_key, weight_key]].apply(utils.find_bmi, axis=1)