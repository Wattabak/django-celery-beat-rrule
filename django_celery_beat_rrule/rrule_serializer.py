"""
Credit for original implementation https://gist.github.com/maxfire2008/096fd5f55c9d79a11d41769d58e8bca1

Under CC0 License
"""

import datetime
import json

import dateutil.rrule


def rruleset_to_dict(rruleset: dateutil.rrule.rruleset) -> dict:
    """
    Convert a rruleset to a JSON string.
    """ 
    return {
        "rrule": [str(rrule) for rrule in rruleset._rrule],
        "rdate": [rdate.isoformat() for rdate in rruleset._rdate],
        "exrule": [str(exrule) for exrule in rruleset._exrule],
        "exdate": [exdate.isoformat() for exdate in rruleset._exdate],
    }


def json_to_rruleset(json_string: str| any) -> dateutil.rrule.rruleset:
    """
    Convert a JSON string to a rruleset.
    """
    if isinstance(json_string, str):
        data = json.loads(json_string)
    else:
        raise TypeError("Expected string or")
    rruleset = dateutil.rrule.rruleset()
    rruleset._rrule = [dateutil.rrule.rrulestr(rrule) for rrule in data["rrule"]]
    rruleset._rdate = [
        datetime.datetime.fromisoformat(rdate) for rdate in data["rdate"]
    ]
    rruleset._exrule = [dateutil.rrule.rrulestr(exrule) for exrule in data["exrule"]]
    rruleset._exdate = [
        datetime.datetime.fromisoformat(exdate) for exdate in data["exdate"]
    ]
    return rruleset


def rruleset_to_str(myset: dateutil.rrule.rruleset) -> str:
    """Convert a rruleset to a json string"""
    return json.dumps(rruleset_to_dict(myset))

