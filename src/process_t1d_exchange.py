import pandas as pd
import numpy as np
import utils
import math
from utils import DemographicSelection


def filter_df_by_demographic(df, demographic):
    if demographic == DemographicSelection.PEDIATRIC:
        return df[df[age_key] < 18]
    elif demographic == DemographicSelection.ADULT:
        return df[df[age_key] >= 18]
    elif demographic == DemographicSelection.ASPIRATIONAL:
        raise Exception("Not implemented yet")
    elif demographic == DemographicSelection.NON_ASPIRATIONAL:
        raise Exception("Not implemented yet")

    # Don't do anything if it's 'overall'
    return df


isf_icr_path = utils.find_full_path("HDeviceWizard", ".csv")
age_path = utils.find_full_path("HPtRoster", ".csv")
demographics_path = utils.find_full_path("HScreening", ".csv")

icr_isf_df = pd.read_csv(isf_icr_path)
age_df = pd.read_csv(age_path)
demographics_df = pd.read_csv(demographics_path)

# Keys for working with exports
""" T1D Exchange """
# tdd_key = "total_daily_dose_avg" TODO once Jaeb publishes basal data
# basal_key = "total_daily_basal_insulin_avg"  # Total daily basal, TODO once Jaeb publishes basal data
carb_key = "total_daily_carb_avg"  # Total daily carbs
bmi_key = "bmi"
weight_key = "Weight"  # in cm
height_key = "Height"  # in lbs
isf_key = "InsulinSensitivity"
icr_key = "InsulinCarbRatio"
age_key = "AgeAsOfEnrollDt"
# tir_key = "percent_70_180_2week"
demographics_to_get = DemographicSelection.PEDIATRIC

relevant_data = icr_isf_df[[isf_key, icr_key]]
relevant_data[isf_key] *= 18.0182  # Convert from mmol to mg/dL
# Get total daily carb intake
relevant_data[carb_key] = (
    icr_isf_df.groupby(["PtId", "DeviceDtTmDaysFromEnroll"])["CarbInput"]
    .sum()
    .reset_index()["CarbInput"]
)
relevant_data[age_key] = age_df[age_key]
relevant_data[bmi_key] = demographics_df[[height_key, weight_key]].apply(
    utils.find_bmi, axis=1
)

relevant_data = filter_df_by_demographic(relevant_data, demographics_to_get)

relevant_data.to_csv(
    utils.get_demographic_export_path(demographics_to_get, "t1d_exchange")
)
