from datetime import datetime

def get_date():
    format = '%Y%m%d%M%s'
    return datetime.now().strftime(format)