# coding:utf8
from loguru import logger

import datetime
import numpy as np
import pandas as pd
import utils.db as db
import json

from datacenter.remote_data_model_cn import get_all_stockcode, get_remote_balancesheet_data, get_remote_cashflow_data, get_remote_porfitstatement_data

__dataformat__ = "google"


def init_balancesheet(stockcode,year_list=[]):
    """
        1. 从新浪财经爬取财务数据
        2. 4月30日前获取上两年止，最近五年的数据，4月30日后获取上1年止，最近5年的数据
        3. 获取前检查是否已经为最近5年数据
        4. 数据格式：
        collection : balancesheet/profitstatement/cashflow
        document :
            balancesheet:{
                _id:
                stockcode:
                latestyear:
                data:[
                    {
                        year:
                        hbzj:
                    }
                ]
            }
            profitstatement ..
            cashflow ..
            accountcode:{
                type:
                code:
            }
    """
    # 获取当前时间
    today = datetime.datetime.today()
    current_date = datetime.date(today.year,today.month,today.day)
    report_date = datetime.date(today.year, 4, 30)
    if current_date < report_date:
        report_year = today.year - 2
    else:
        report_year = today.year - 1

    if len(year_list) == 0:
        year_list.extend([report_year-10,report_year-9,report_year-8,report_year-7,report_year-6,report_year-5,report_year-4,report_year-3,report_year-2,report_year-1,report_year])
    year_list.sort()

    ias_db = db.get_mongo_db()
    balancesheet_collection = ias_db.get_collection("balancesheet")

    all_json_str = "{\"stockcode\":\"" + stockcode + "\","
    all_json_str += "\"latestyear\":\"" + str(report_year) + "\",\"updateday\":\""+today.strftime("%Y-%m-%d")+"\",\"data\":["

    return_json_str = ""
    for year in year_list:
        return_json_str += get_remote_balancesheet_data(stockcode, year)

    if len(return_json_str) <=0 :
        logger.info("获取bs数据失败 : %s" % stockcode)
        return

    # 删除数据
    balancesheet_collection.delete_one({"stockcode": stockcode})
    logger.info("deleted balancesheet of : %s" % stockcode)

    all_json_str += return_json_str.strip(",")+"]}"
    blancesheet_json_obj = json.loads(all_json_str)
    balancesheet_collection.insert_one(blancesheet_json_obj)
    logger.info("insert balancesheet data %s %s end."%(stockcode,report_year))

def init_profitstatement(stockcode,year_list=[]):
    # year_list = []
    # 获取当前时间
    today = datetime.datetime.today()
    current_date = datetime.date(today.year,today.month,today.day)
    report_date = datetime.date(today.year, 4, 30)
    if current_date < report_date:
        report_year = today.year - 2
    else:
        report_year = today.year - 1

    if len(year_list) == 0:
        year_list.extend([report_year-10,report_year-9,report_year-8,report_year-7,report_year-6,report_year-5,report_year-4,report_year-3,report_year-2,report_year-1,report_year])
    year_list.sort()

    ias_db = db.get_mongo_db()

    profitstatement_collection = ias_db.get_collection("profitstatement")

    all_json_str = "{\"stockcode\":\"" + stockcode + "\","
    all_json_str += "\"latestyear\":\"" + str(report_year) + "\",\"updateday\":\""+today.strftime("%Y-%m-%d")+"\",\"data\":["

    return_json_str = ""
    for year in year_list:
        return_json_str += get_remote_porfitstatement_data(stockcode, year)

    if len(return_json_str) <=0 :
        logger.info("获取ps数据失败 : %s" % stockcode)
        return

        # 删除数据
    profitstatement_collection.delete_one({"stockcode": stockcode})
    logger.info("deleted profitstatement of : %s" % stockcode)

    all_json_str += return_json_str.strip(",")+"]}"
    profitstatement_json_obj = json.loads(all_json_str)
    profitstatement_collection.insert_one(profitstatement_json_obj)
    logger.info("insert profitstatement data %s %s end."%(stockcode,report_year))

def init_cashflow(stockcode,year_list=[]):
    # year_list = []
    # 获取当前时间
    today = datetime.datetime.today()
    current_date = datetime.date(today.year, today.month, today.day)
    report_date = datetime.date(today.year, 4, 30)
    if current_date < report_date:
        report_year = today.year - 2
    else:
        report_year = today.year - 1

    if len(year_list) == 0:
        year_list.extend([report_year-10,report_year-9,report_year-8,report_year-7,report_year-6,report_year-5,report_year-4,report_year-3,report_year-2,report_year-1,report_year])
    year_list.sort()

    ias_db = db.get_mongo_db()

    cashflow_collection = ias_db.get_collection("cashflow")

    # 删除数据
    cashflow_collection.delete_one({"stockcode": stockcode})

    print("deleted cashflow of : %s" % stockcode)

    all_json_str = "{\"stockcode\":\"" + stockcode + "\","
    all_json_str += "\"latestyear\":\"" + str(report_year) + "\",\"updateday\":\"" + today.strftime(
        "%Y-%m-%d") + "\",\"data\":["

    return_json_str = ""
    for year in year_list:
        return_json_str += get_remote_cashflow_data(stockcode, year)

    if len(return_json_str) <=0 :
        logger.info("获取cs数据失败 : %s" % stockcode)
        return

        # 删除数据
    cashflow_collection.delete_one({"stockcode": stockcode})
    logger.info("deleted profitstatement of : %s" % stockcode)

    all_json_str += return_json_str.strip(",") + "]}"
    cashflow_json_obj = json.loads(all_json_str)
    cashflow_collection.insert_one(cashflow_json_obj)
    logger.info("insert cashflow data %s %s end." % (stockcode, report_year))

def init_all_stock():
    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")
    stock_code_collection.drop()
    for i in range(1, 11):
        get_all_stockcode(i)
        logger.info(i)

def init_all_stock_fi_data(start=0,end=0,year_list=[],exclude=[]):

    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")
    with stock_code_collection.find(no_cursor_timeout=True) as stock_dic:
        cnt = start
        error_cnt = 0
        l_temp = []
        if end > 0 :
            l_temp = stock_dic[start:end]
        else:
            l_temp = stock_dic[start:]

        sleep_cnt = 0
        for stock in l_temp:

            # if sleep_cnt >= 10 :
            #     print("暂停3分钟。。")
            #     time.sleep(60*3)
            #     sleep_cnt = 0
            #     print("恢复运行。。")
            try:
                if stock["SECURITY_CODE"] in exclude:
                    continue
                init_balancesheet(stock["SECURITY_CODE"],year_list)
                init_profitstatement(stock["SECURITY_CODE"],year_list)
                init_cashflow(stock["SECURITY_CODE"],year_list)
                logger.info(stock["SECURITY_CODE"])
            except Exception as e:
                logger.info(stock["SECURITY_CODE"]+"出错了。%s"%(str(e)))
                error_cnt = error_cnt+1
            cnt = cnt + 1
            sleep_cnt = sleep_cnt + 1
            # if cnt%10 == 0:
            #     time.sleep(5)
            #     print("中断5s")
            logger.info(cnt)
        logger.info("总计：%d , 失败：%d" % (cnt,error_cnt))

def init_one_stock_fi_data(stock_code,year_list=[]):

    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")
    stock_dic = stock_code_collection.find()

    try:
        init_balancesheet(stock_code,year_list)
        init_profitstatement(stock_code,year_list)
        init_cashflow(stock_code,year_list)
        logger.info(stock_code)
    except Exception as e:
        logger.info(stock_code+"出错了。%s"%(str(e)))

def update_balancesheet(symbol:str):
    '''
    WALL-E data
    :param symbol: stockcode(the same as symbol in ias2.0)
    1. Check the data first and find out the lack year of data
    2. Get the data from sina finance
    3. Insert the data into MongoDB
    '''
    today = datetime.datetime.today()
    current_date = datetime.date(today.year,today.month,today.day)
    report_date = datetime.date(today.year, 4, 30)
    if current_date < report_date:
        report_year = today.year - 2
    else:
        report_year = today.year - 1

    ias_db = db.get_mongo_db()
    balancesheet_collection = ias_db.get_collection("balancesheet")
    
    # 使用聚合管道查询最大年份
    pipeline = [
        {"$match": {"stockcode": symbol}},  # 匹配指定的股票代码
        {"$unwind": "$data"},  # 展开data数组
        {"$group": {
            "_id": "$stockcode",
            "maxYear": {"$max": "$data.year"}  # 获取year字段的最大值
        }}
    ]
    
    result = list(balancesheet_collection.aggregate(pipeline))
    
    if not result:
        logger.info(f"No balancesheet data found for stock {symbol}")
        return None
    
    max_year = result[0]["maxYear"]
    logger.info(f"Latest year for stock {symbol} is {max_year}")

    # Check if the latest year is less than the report year
    if max_year < report_year:
        logger.info(f"Updating balancesheet data for stock {symbol} from year {max_year + 1} to {report_year}")
        # Get the data from sina finance
        for year in range(max_year + 1, report_year + 1):
            get_remote_balancesheet_data(symbol, year)
        
        # Insert the new data into MongoDB
        all_json_str = "{\"stockcode\":\"" + symbol + "\","
        all_json_str += "\"latestyear\":\"" + str(report_year) + "\",\"updateday\":\""+today.strftime("%Y-%m-%d")+"\",\"data\":["

        return_json_str = ""
        for year in range(max_year + 1, report_year + 1):
            return_json_str += get_remote_balancesheet_data(symbol, year)

        all_json_str += return_json_str.strip(",") + "]}"
        blancesheet_json_obj = json.loads(all_json_str)
        
        # Update the existing document or insert a new one
        balancesheet_collection.update_one({"stockcode": symbol}, {"$set": blancesheet_json_obj}, upsert=True)
        logger.info(f"Inserted/Updated balancesheet data for stock {symbol} from year {max_year + 1} to {report_year}")
    else:
        logger.info(f"No need to update balancesheet data for stock {symbol}, latest year is already {max_year}")
    
def update_profitstatement(symbol:str):
    '''
    WALL-E data
    :param symbol: stockcode(the same as symbol in ias2.0)
    1. Check the data first and find out the lack year of data
    2. Get the data from sina finance
    3. Insert the data into MongoDB
    '''
    today = datetime.datetime.today()
    current_date = datetime.date(today.year,today.month,today.day)
    report_date = datetime.date(today.year, 4, 30)
    if current_date < report_date:
        report_year = today.year - 2
    else:
        report_year = today.year - 1
    ias_db = db.get_mongo_db()
    profitstatement_collection = ias_db.get_collection("profitstatement")
    # 使用聚合管道查询最大年份
    pipeline = [
        {"$match": {"stockcode": symbol}},  # 匹配指定的股票代码
        {"$unwind": "$data"},  # 展开data数组
        {"$group": {
            "_id": "$stockcode",
            "maxYear": {"$max": "$data.year"}  # 获取year字段的最大值
        }}
    ]
    result = list(profitstatement_collection.aggregate(pipeline))
    if not result:
        logger.info(f"No profitstatement data found for stock {symbol}")
        return None
    max_year = result[0]["maxYear"]                 
    logger.info(f"Latest year for stock {symbol} is {max_year}")
    # Check if the latest year is less than the report year
    if max_year < report_year:
        logger.info(f"Updating profitstatement data for stock {symbol} from year {max_year + 1} to {report_year}")
        # Get the data from sina finance
        for year in range(max_year + 1, report_year + 1):
            get_remote_porfitstatement_data(symbol, year)
        
        # Insert the new data into MongoDB
        all_json_str = "{\"stockcode\":\"" + symbol + "\","
        all_json_str += "\"latestyear\":\"" + str(report_year) + "\",\"updateday\":\""+today.strftime("%Y-%m-%d")+"\",\"data\":["

        return_json_str = ""
        for year in range(max_year + 1, report_year + 1):
            return_json_str += get_remote_porfitstatement_data(symbol, year)

        all_json_str += return_json_str.strip(",") + "]}"
        profitstatement_json_obj = json.loads(all_json_str)
        
        # Update the existing document or insert a new one
        profitstatement_collection.update_one({"stockcode": symbol}, {"$set": profitstatement_json_obj}, upsert=True)
        logger.info(f"Inserted/Updated profitstatement data for stock {symbol} from year {max_year + 1} to {report_year}")
    else:
        logger.info(f"No need to update profitstatement data for stock {symbol}, latest year is already {max_year}")
def update_cashflow(symbol:str):
    '''
    WALL-E data
    :param symbol: stockcode(the same as symbol in ias2.0)
    1. Check the data first and find out the lack year of data
    2. Get the data from sina finance
    3. Insert the data into MongoDB
    '''
    today = datetime.datetime.today()
    current_date = datetime.date(today.year,today.month,today.day)
    report_date = datetime.date(today.year, 4, 30)
    if current_date < report_date:
        report_year = today.year - 2
    else:
        report_year = today.year - 1
    ias_db = db.get_mongo_db()
    cashflow_collection = ias_db.get_collection("cashflow")
    # 使用聚合管道查询最大年份
    pipeline = [
        {"$match": {"stockcode": symbol}},  # 匹配指定的股票代码
        {"$unwind": "$data"},  # 展开data数组
        {"$group": {
            "_id": "$stockcode",
            "maxYear": {"$max": "$data.year"}  # 获取year字段的最大值
        }}
    ]
    result = list(cashflow_collection.aggregate(pipeline))
    if not result:
        logger.info(f"No cashflow data found for stock {symbol}")
        return None
    max_year = result[0]["maxYear"]
    logger.info(f"Latest year for stock {symbol} is {max_year}")
    # Check if the latest year is less than the report year
    if max_year < report_year:
        logger.info(f"Updating cashflow data for stock {symbol} from year {max_year + 1} to {report_year}")
        # Get the data from sina finance
        for year in range(max_year + 1, report_year + 1):
            get_remote_cashflow_data(symbol, year)
        
        # Insert the new data into MongoDB
        all_json_str = "{\"stockcode\":\"" + symbol + "\","
        all_json_str += "\"latestyear\":\"" + str(report_year) + "\",\"updateday\":\""+today.strftime("%Y-%m-%d")+"\",\"data\":["

        return_json_str = ""
        for year in range(max_year + 1, report_year + 1):
            return_json_str += get_remote_cashflow_data(symbol, year)

        all_json_str += return_json_str.strip(",") + "]}"
        cashflow_json_obj = json.loads(all_json_str)
        
        # Update the existing document or insert a new one
        cashflow_collection.update_one({"stockcode": symbol}, {"$set": cashflow_json_obj}, upsert=True)
        logger.info(f"Inserted/Updated cashflow data for stock {symbol} from year {max_year + 1} to {report_year}")
    else:
        logger.info(f"No need to update cashflow data for stock {symbol}, latest year is already {max_year}")
def update_all_stock_fi_data(start=0,end=0,year_list=[],exclude=[]):
    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")
    with stock_code_collection.find(no_cursor_timeout=True) as stock_dic:
        cnt = start
        error_cnt = 0
        l_temp = []
        if end > 0 :
            l_temp = stock_dic[start:end]
        else:
            l_temp = stock_dic[start:]

        sleep_cnt = 0
        for stock in l_temp:

            # if sleep_cnt >= 10 :
            #     print("暂停3分钟。。")
            #     time.sleep(60*3)
            #     sleep_cnt = 0
            #     print("恢复运行。。")
            try:
                if stock["SECURITY_CODE"] in exclude:
                    continue
                update_balancesheet(stock["SECURITY_CODE"])
                update_profitstatement(stock["SECURITY_CODE"])
                update_cashflow(stock["SECURITY_CODE"])
                logger.info(stock["SECURITY_CODE"])
            except Exception as e:
                logger.info(stock["SECURITY_CODE"]+"出错了。%s"%(str(e)))
                error_cnt = error_cnt+1
            cnt = cnt + 1
            sleep_cnt = sleep_cnt + 1
            # if cnt%10 == 0:
            #     time.sleep(5)
            #     print("中断5s")
            logger.info(cnt)
        logger.info("总计：%d , 失败：%d" % (cnt,error_cnt))
def update_one_stock_fi_data(stock_code):
    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")
    stock_dic = stock_code_collection.find()
    try:
        update_balancesheet(stock_code)
        update_profitstatement(stock_code)
        update_cashflow(stock_code)
        logger.info(stock_code)
    except Exception as e:
        logger.info(stock_code+"出错了。%s"%(str(e)))
    # update_balancesheet(stock_code)
    # update_profitstatement(stock_code)
    # update_cashflow(stock_code)
    # logger.info(stock_code)
def update_all_stock():
    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")
    stock_code_collection.drop()
    for i in range(1, 11):
        get_all_stockcode(i)
        logger.info(i)
    
if __name__ == '__main__' :

    year_list = [1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
    # init_balancesheet("000858",[1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022])
    # init_profitstatement("000858",[1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022])
    # init_cashflow("000858",[1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022])

    # init_profitstatement("000858")
    # init_cashflow("000858")
    # init_all_stock_fi_data(start=4886,end=0,year_list=year_list,exclude=["600519"])
    # init_all_stock()3563
    # init_one_stock_fi_data(stock_code="300272",year_list=year_list)

    update_all_stock()

