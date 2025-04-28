# coding:utf8
import json
import utils.db as db

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from loguru import logger

from utils.finance_item_cn import FinanceNotesIdx, ProfitStatementIdx

__dataformat__ = "google"


def get_remote_balancesheet_data(stockcode,year):

    year_str = str(year)
    url_list = ["https://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/",stockcode,"/ctrl/",year_str,"/displaytype/4.phtml"]
    url = "".join(url_list)

    session = HTMLSession()
    response = session.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.find("table",id="BalanceSheetNewTable0")

    if table is None:
        return ""

    trs = table.find_all("tr")[4:]

    json_str = "{\"year\":\""+year_str+"\""
    for tr in trs :
        tds = tr.find_all("td")[:2]
        if len(tds) < 2:
            continue

        account_name = tds[0].find("a").text.strip()
        # print(tds[0])
        # print(tds[1])
        amount_str = tds[1].text.strip()
        if amount_str.find(",") != -1:
            amount_num = str(float(tds[1].text.strip().replace(",","")))
        else:
            amount_num = amount_str

        json_str += ",\""+account_name+"\":\""+amount_num+"\""

    json_str += "},"

    return json_str

def get_remote_porfitstatement_data(stockcode,year):

    year_str = str(year)
    url_list = ["https://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/", stockcode, "/ctrl/",
                year_str, "/displaytype/4.phtml"]
    url = "".join(url_list)

    session = HTMLSession()
    response = session.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.find("table", id="ProfitStatementNewTable0")

    if table is None:
        return ""

    trs = table.find_all("tr")[3:]

    json_str = "{\"year\":\"" + year_str + "\""
    for tr in trs:
        tds = tr.find_all("td")[:2]
        if len(tds) < 2:
            continue

        account_name = tds[0].find("a").text.strip()
        # print(tds[0])
        # print(tds[1])
        amount_str = tds[1].text.strip()
        if amount_str.find(",") != -1:
            amount_num = str(float(tds[1].text.strip().replace(",", "")))
        else:
            amount_num = amount_str

        json_str += ",\"" + account_name + "\":\"" + amount_num + "\""

    json_str += "},"

    return json_str

def get_remote_cashflow_data(stockcode,year):
    year_str = str(year)
    url_list = ["https://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/", stockcode, "/ctrl/",
                year_str, "/displaytype/4.phtml"]
    url = "".join(url_list)

    session = HTMLSession()
    response = session.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.find("table", id="ProfitStatementNewTable0")

    if table is None:
        return ""

    trs = table.find_all("tr")[3:]

    json_str = "{\"year\":\"" + year_str + "\""
    for tr in trs:
        tds = tr.find_all("td")[:2]
        if len(tds) < 2:
            continue

        account_name = tds[0].find("a").text.strip()
        # print(tds[0])
        # print(tds[1])
        amount_str = tds[1].text.strip()
        if amount_str.find(",") != -1:
            amount_num = str(float(tds[1].text.strip().replace(",", "")))
        else:
            amount_num = amount_str

        json_str += ",\"" + account_name + "\":\"" + amount_num + "\""

    json_str += "},"

    json_str = json_str.replace(ProfitStatementIdx.财务费用.name,FinanceNotesIdx.财务费用_FN.name)

    return json_str

def get_all_stockcode(page_num):
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112309273027854195741_1678799885331&sortColumns=SECURITY_CODE&sortTypes=1&pageSize=500&pageNumber=%s&reportName=RPT_DMSK_TS_STOCKNEW&quoteColumns=&quoteType=0&columns=SECURITY_CODE,SECURITY_NAME_ABBR&filter=&token=894050c76af8597a853f5b408b759f5d"%str(page_num)
    session = HTMLSession()
    response = session.get(url)
    text_str = response.text
    start_pos = text_str.index("(")
    end_pos = text_str.index(")")
    json_str = text_str[start_pos+1:end_pos]
    json_dic = json.loads(json_str)
    json_data = json_dic["result"]["data"]

    ias_db = db.get_mongo_db()
    stock_code_collection = ias_db.get_collection("stock_code")

    stock_code_collection.insert_many(json_data)
    logger.info("insert many complate.")
