import pandas as pd
from datetime import datetime


def load_dataframe(path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(path)
    return df


def clean_currency(x: "str | float") -> float:
    if isinstance(x, str):
        return float(x.replace('$', '').replace(',', '').replace('(', '').replace(')', ''))
    return x


def num_2_currency(curr: str, num: float) -> str:
    return f"{curr}{round(num, 2)}"


def str_2_date(dt_str: str) -> datetime:
    dt_obj: datetime = datetime.strptime(dt_str, "%m/%d/%Y")
    return dt_obj


def date_obj_2_str(dt_obj: str) -> str:
    dt_str: datetime = datetime.strftime(dt_obj, "%m/%d/%Y")
    return dt_str


def diff_dates(date1: datetime, date2: datetime) -> int:
    if date2 > date1:
        return (date2 - date1).days
    else:
        return (date1 - date2).days


def preferred_return_formula(C: float, R: float, d: int) -> float:
    return C * ( (1 + R) ** (d / 365) )


def catch_up_formula(ci: float, PR: float, cu: float) -> float:    
    return ci * PR / (cu - ci)

