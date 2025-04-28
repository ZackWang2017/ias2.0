#coding:utf8

class ConstantsCN:
    """
    Constants for Chinese stock markets.
    """
    # Stock market codes
    SHANGHAI_STOCK_EXCHANGE = "SH"
    SHENZHEN_STOCK_EXCHANGE = "SZ"
    
    # Stock types
    A_SHARE = "A股"
    B_SHARE = "B股"
    H_SHARE = "H股"
    
    # Stock market names
    STOCK_MARKET_CN = {
        SHANGHAI_STOCK_EXCHANGE: "上海证券交易所",
        SHENZHEN_STOCK_EXCHANGE: "深圳证券交易所",
        A_SHARE: "A股",
        B_SHARE: "B股",
        H_SHARE: "H股",
    }
    # 银行标准贷款利率
    BANK_LOAN_RATE = 0.035