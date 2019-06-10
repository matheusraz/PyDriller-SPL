from pyexcel_ods import get_data
from bson import json_util
import datetime
import json

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def getManualResults():
    data = get_data("results-manual.ods")
    allHashs = []
    for i in range(1,len(data['FM'])-1):
        if(len(data['FM'][i]) > 0):
            allHashs.append(data['FM'][i][0])
    return allHashs