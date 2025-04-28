#coding:utf8

import os
import pandas as pd
import utils.db as db

ias_db = db.get_mongo_db()

def export_balance_sheet_to_excel(stock_code:str,export_file_path:str):
    """
    导出资产负债表
    :return:
    """
    # 从MongoDB查询数据
    balance_sheet = ias_db.balancesheet.find_one({'stockcode': stock_code})
    
    if balance_sheet is None or 'data' not in balance_sheet:
        raise ValueError(f"No balance sheet data found for stock code {stock_code}")
        
    # 转换数据为DataFrame
    df = pd.DataFrame(balance_sheet['data'])
    
    # 设置年份为索引
    df.set_index('year', inplace=True)
    
    # 创建Excel writer对象
    # Create Excel file path with stock_code as filename
    file_name = f"{stock_code}.xlsx"
    with pd.ExcelWriter(f"{export_file_path}/{file_name}", engine='openpyxl') as writer:
        # 将DataFrame导出到Excel，sheet名称为"资产负债表"
        df.to_excel(writer, sheet_name='资产负债表')

def export_income_statement_to_excel(stock_code:str,export_file_path:str):
    """
    导出利润表 利润表的collection名称为：profitstatement
    :return:
    """
    # 从MongoDB查询数据
    income_statement = ias_db.profitstatement.find_one({'stockcode': stock_code})
    
    if income_statement is None or 'data' not in income_statement:
        raise ValueError(f"No income statement data found for stock code {stock_code}")
        
    # 转换数据为DataFrame
    df = pd.DataFrame(income_statement['data'])
    
    # 设置年份为索引
    df.set_index('year', inplace=True)
    
    # 创建Excel writer对象
    file_name = f"{stock_code}.xlsx"
    with pd.ExcelWriter(f"{export_file_path}/{file_name}", engine='openpyxl') as writer:
        # 将DataFrame导出到Excel，sheet名称为"利润表"
        df.to_excel(writer, sheet_name='利润表')
    

def export_cash_flow_statement_to_excel(stock_code:str,export_file_path:str):
    """
    导出现金流量表 现金流量表的collection名称为：cashflow
    :return:
    """
    # 从MongoDB查询数据
    cash_flow_statement = ias_db.cashflow.find_one({'stockcode': stock_code})
    
    if cash_flow_statement is None or 'data' not in cash_flow_statement:
        raise ValueError(f"No cash flow statement data found for stock code {stock_code}")
        
    # 转换数据为DataFrame
    df = pd.DataFrame(cash_flow_statement['data'])
    
    # 设置年份为索引
    df.set_index('year', inplace=True)
    
    # 创建Excel writer对象
    file_name = f"{stock_code}.xlsx"
    with pd.ExcelWriter(f"{export_file_path}/{file_name}", engine='openpyxl') as writer:
        # 将DataFrame导出到Excel，sheet名称为"现金流量表"
        df.to_excel(writer, sheet_name='现金流量表')

def export_statement_to_excel(stock_code:str,export_file_path:str):
    """
    导出财务报表
    :return:
    """
    # 获取所有报表数据
    balance_sheet = ias_db.balancesheet.find_one({'stockcode': stock_code})
    income_statement = ias_db.profitstatement.find_one({'stockcode': stock_code})
    cash_flow_statement = ias_db.cashflow.find_one({'stockcode': stock_code})

    # 检查数据是否存在
    if any(x is None or 'data' not in x for x in [balance_sheet, income_statement, cash_flow_statement]):
        raise ValueError(f"Missing data for stock code {stock_code}")

    # 转换数据为DataFrame
    balance_df = pd.DataFrame(balance_sheet['data']).set_index('year')
    income_df = pd.DataFrame(income_statement['data']).set_index('year')
    cash_flow_df = pd.DataFrame(cash_flow_statement['data']).set_index('year')

    # 创建Excel文件，mode='w'表示覆盖已存在的文件
    # 检查export_file_path是否存在
    if not os.path.exists(export_file_path):
        os.makedirs(export_file_path)
    file_name = f"{stock_code}.xlsx"
    with pd.ExcelWriter(f"{export_file_path}/{file_name}", engine='openpyxl', mode='w') as writer:
        balance_df.to_excel(writer, sheet_name='资产负债表')
        income_df.to_excel(writer, sheet_name='利润表')
        cash_flow_df.to_excel(writer, sheet_name='现金流量表')

if __name__ == "__main__":
    # 测试导出函数
    stock_code = "000596"  # 示例股票代码
    export_file_path = "./exported_reports"  # 示例导出路径

    try:
        export_statement_to_excel(stock_code, export_file_path)
        print(f"财务报表已成功导出到 {export_file_path}/{stock_code}.xlsx")
    except Exception as e:
        print(f"导出失败: {e}")