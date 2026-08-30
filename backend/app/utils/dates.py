from datetime import datetime


def get_current_quarter():

    now = datetime.now()

    quarter = (now.month - 1) // 3 + 1

    start_month = 3 * (quarter - 1) + 1

    start_date = datetime(
        now.year,
        start_month,
        1
    )

    if quarter == 4:

        end_date = datetime(
            now.year,
            12,
            31,
            23,
            59,
            59
        )

    else:

        end_date = datetime(
            now.year,
            start_month + 3,
            1
        )

    return start_date, end_date


def filter_current_quarter(df, date_column):

    start_date, end_date = get_current_quarter()

    return df[
        (df[date_column] >= start_date)
        &
        (df[date_column] < end_date)
    ]