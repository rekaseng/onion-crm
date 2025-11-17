from datetime import date, datetime, timedelta
from typing import Optional


def fomat_local_datetime(ref_date: Optional[date]):
    result = None
    if ref_date:
        result = datetime.combine(ref_date, datetime.min.time()) - timedelta(hours=8)

    return result
