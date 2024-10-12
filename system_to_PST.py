#!/bin/python
# convert from system time (GMT) to human PST

def mytime(gmt_time):

    # Convert to datetime in GMT with timezone awareness
    gmt_datetime = datetime.datetime.fromtimestamp(gmt_time, datetime.timezone.utc)

    # Convert to PST (Pacific Standard Time)
    pst_offset = datetime.timedelta(hours=-8)
    pst_datetime = gmt_datetime.astimezone(datetime.timezone(pst_offset))
    print("PST Time:", pst_datetime)