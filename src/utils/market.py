#coding=utf-8
# @Time    : 2023/10/12 17:00
# @Author  : zack wang

from enum import Enum
import re

class StockMarket(Enum):
    CHINA_SH = "SH"
    CHINA_SZ = "SZ"
    HONG_KONG = "HK"
    USA = "美国证券交易所"
    JAPAN = "日本证券交易所"
    UNKNOWN = "未知市场"

def determine_stock_market(stock_code: str) -> StockMarket:
    """
    Determine the stock market based on stock code pattern
    
    Patterns:
    - China SH: 6xxxxx
    - China SZ: 0xxxxx or 3xxxxx
    - Hong Kong: xxxx.HK
    - USA: Alphabetic symbols or symbols with '.'
    - Japan: xxxx.T
    """
    # Remove any whitespace and convert to uppercase
    stock_code = stock_code.strip().upper()
    
    # Chinese A-share patterns
    if re.match(r'^60\d{4}$|^68\d{4}$', stock_code):
        return StockMarket.CHINA_SH
    elif re.match(r'^(00|30|002|300)\d{3,4}$', stock_code):
        return StockMarket.CHINA_SZ
    
    # Hong Kong stocks
    elif re.match(r'^\d{4}\.?HK$', stock_code):
        return StockMarket.HONG_KONG
    
    # Japanese stocks
    elif re.match(r'^\d{4}\.?T$', stock_code):
        return StockMarket.JAPAN
    
    # US stocks (typically alphabetic symbols)
    elif re.match(r'^[A-Z]{1,5}$|^[A-Z]{1,4}\.[A-Z]{1,2}$', stock_code):
        return StockMarket.USA
    
    return StockMarket.UNKNOWN