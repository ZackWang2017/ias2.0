#coding:utf8

from utils import db, market

ias_db = db.get_db("ias")
stock_code_collection = ias_db.get_collection("stock_code")
sw_class_stock_collection = ias_db.get_collection("sw_class_stock")

def search_stock(stock_code: str):

    '''
    :param stock_code: 股票代码
    :return: 股票信息
    
    1. recognize the market
    2. get the stock information, the datastructure is:
        {
            symbol: str, # 股票代码
            name: str, # 股票名称
            market: str, # 股票市场
            exchange: str, # 股票交易所
            industry_code: str, # 股票行业代码
            industry_name: str, # 股票行业名称
        }
    '''

    # 1. recognize the market
    market_type = market.get_market(stock_code)
    if market_type == market.StockMarket.UNKNOWN:
        return "{'error':'unknown market'}"
    elif market_type == market.StockMarket.CHINA_SH or market_type == market.StockMarket.CHINA_SZ:
        #2. get the stock information
        stock_info = stock_code_collection.find_one({"SECURITY_CODE": stock_code})
        if stock_info is None:
            return "stock not found"
        else:
            stock_info = {
                "symbol": stock_info["SECURITY_CODE"],
                "name": stock_info["SECURITY_NAME_ABBR"],
                "market": "中国",
                "exchange": market_type.value,
                "industry_code": "",
                "industry_name": ""
            }
            #3. get the industry information
            symbol = stock_code+"."+market_type.value
            sw_class_stock = sw_class_stock_collection.find_one({"stock_code": symbol})
            if sw_class_stock is None:
                return "industry not found"
            else:
                stock_info["industry_code"] = sw_class_stock["class_code"]
                stock_info["industry_name"] = sw_class_stock["c3_name"]
                return stock_info
    else:
        return "{'error':'other market'}"