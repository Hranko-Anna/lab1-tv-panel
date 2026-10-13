import pandas as pd
import numpy as np

def split_sessions_by_hour(start, end, weight):
    cur = start
    while cur < end:
        nxt = min(end, (cur + pd.Timedelta(hours=1)).floor('h'))
        yield cur.hour, (nxt - cur).total_seconds()/60, weight
        cur = nxt

def person_mask(resp_type_series):
    return resp_type_series.isin(['R','L'])

def build_person_attrs(viewer_attributes, attributes):
    va = viewer_attributes.merge(
        attributes.set_index('attr_id')[['attr_group','attr_name']],
        on='attr_id', how='left')
    sex = va[va.attr_id.isin([201,202])].copy()
    sex['sex'] = sex.attr_id.map({201:'M', 202:'F'})
    age = va[va.attr_id == 300][['respondent_id','value']].rename(columns={'value':'age'})
    return sex[['respondent_id','sex']].merge(age, on='respondent_id', how='left')