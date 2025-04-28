#coding:utf8
def safe_float(value):
    if value in ['--', '', None]:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0