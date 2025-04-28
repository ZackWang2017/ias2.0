#coding :utf8
from typing import Dict, Any
from loguru import logger

from tools.funcs import *
from utils.finance_item_cn import *
from utils.constants import ConstantsCN

import utils.db as db


ias_db = db.get_mongo_db()
balancesheet_collection = ias_db.get_collection("balancesheet")
profitstatement_collection = ias_db.get_collection("profitstatement")
cashflow_collection = ias_db.get_collection("cashflow")
tang_metrix_collection = ias_db.get_collection("tang_metrix")

def get_metrix_model(stockcode: str,for_update:int) -> Dict[str, Any]:
    '''
        Check weather it have generated the metrix before,
        if not , genearted the metrix first. Or return the generated metrix.
        :param stockcode: stock code
        :return: metrix value

        datastructure:
        
        {
            'stock_code': stockcode,
            'roe': [
                {
                    'year':value
                },
                {
                    'year':value
                }
            ],
            'roa': {
            }
        }
    '''
    find_one_condition = {"stock_code":stockcode}
    tang_metrix_one = tang_metrix_collection.find_one(find_one_condition)

    if tang_metrix_one is None or for_update == 1:

        # delete the old metrix
        logger.info(f"Delete old metrix model for {stockcode}")
        tang_metrix_collection.delete_many(find_one_condition)

        # generate the metrix
        logger.info(f"Generate metrix model for {stockcode}")
        __generate_metrix_model(stockcode)

        tang_metrix_one = tang_metrix_collection.find_one(find_one_condition)
        if tang_metrix_one is None:
            logger.info(f"Generate metrix model for {stockcode} failed")
        
    return tang_metrix_one

def __generate_metrix_model(stockcode:str)->None:
    '''
        Generate the metrix model
        :param stockcode: stock code
        :return: None
        datastructure:
        
        {
            'stock_code': stockcode,
            'roe': [
                {
                    'year':value
                },
                {
                    'year':value
                }
            ],
            'roa': {
            }
        }
    '''
    ''' change the below functions return to Dict[str, Any] and invoke the function to calculate the metrix,
        every function return json format data like below ( for example row):
        'roe': [
            {
                'year':value
            },
            {
                'year':value
            }
        ],
        'intrest_liability_rate': [
            {
                'year':value
            },
            {
                'year':value
            }
        ]
        and then , compose the json data to a dict like below:
        {
            'stock_code': stockcode,
            'roe': [
                {
                    'year':value
                },
                {
                    'year':value
                }
            ],
            'intrest_liability_rate': [
                {
                    'year':value
                },
                {
                    'year':value
                }
            ]
        }
        and insert the dict to the tang_metrix_collection
    '''
    # 请按照上述的注释给出框架代码，不必编写每个函数的具体实现
    # 1. Calculate the ROE
    roe_result = __roe_calculate(stockcode)
    # 2. Calculate the interest liability rate
    interest_liability_rate_result = __interest_liability_rate_calculate(stockcode)
    # 3. Calculate the is light asset
    is_light_asset_result = __is_light_asset_calculate(stockcode)
    # 4. Calculate the receivable to total asset
    receivable_to_total_asset_result = __reciable_to_total_asset_calculate(stockcode)
    # 5. Calculate the gross profit rate
    gross_profit_rate_result = __gross_profit_rate_calculate(stockcode)
    # 6. Calculate the expense rate
    expense_rate_result = __expense_rate_calculate(stockcode)
    # 7. Calculate the net operating cash to net profit
    net_operating_cash_to_net_profit_result = __net_operating_cash_to_net_profit_calculate(stockcode)
    # 8. Calculate the net operating cash
    net_operating_cash_result = __net_operating_cash(stockcode)
    # 9. Calculate the net investment cash
    net_investment_cash_result = __net_investment_cash(stockcode)
    # 10. Calculate the net financing cash
    net_financing_cash_result = __net_financing_cash(stockcode)
    # 11. Calculate the current ratio
    current_ratio_result = __current_ratio_calculate(stockcode)
    # 12. Calculate the quick ratio
    quick_ratio_result = __quick_ratio_calculate(stockcode)
    # 13. Calculate the cash and equivalents
    cash_and_equivalents_result = __cash_and_equivalents(stockcode)
    # 14. Calculate the final cash and equivalents to interest liability
    final_cash_and_equivalents_to_interest_liability_result = __final_cash_and_equivalents_to_intrest_liability_calculate(stockcode)

    # Compose the json data to a dict
    metrix_data = {
        'stock_code': stockcode,
        'roe': roe_result,
        'intrest_liability_rate': interest_liability_rate_result,
        'is_light_asset': is_light_asset_result,
        'receivable_to_total_asset': receivable_to_total_asset_result,
        'gross_profit_rate': gross_profit_rate_result,
        'expense_rate': expense_rate_result,
        'net_operating_cash_to_net_profit': net_operating_cash_to_net_profit_result,
        'net_operating_cash': net_operating_cash_result,
        'net_investment_cash': net_investment_cash_result,
        'net_financing_cash': net_financing_cash_result,
        'current_ratio': current_ratio_result,
        'quick_ratio': quick_ratio_result,
        'cash_and_equivalents': cash_and_equivalents_result,
        'final_cash_and_equivalents_to_intrest_liability': final_cash_and_equivalents_to_interest_liability_result
    }
    # Insert the dict to the tang_metrix_collection
    try:
        tang_metrix_collection.insert_one(metrix_data)
        logger.info(f"Insert metrix model for {stockcode} success")
    except Exception as e:
        logger.error(f"Insert metrix model for {stockcode} failed: {str(e)}")
        return
    logger.info(f"Insert metrix model for {stockcode} success")    

def __roe_calculate(stockcode:str)-> Dict[str, Any]:
    '''
        Calculate the ROE
        :param stockcode: stock code
        :return: 输出的 roe datastructure:
           [
                {
                    'year':value
                },
                {
                    'year':value
                    }
            ]
        

        roe = net profit / equity
        输入的 net profit 和 equity 是从 profitstatement 和 balancesheet 中获取的
        profitstatement的数据格式：
        {
            'stockcode':stockcode,
            data:[
                {
                    year:value,
                    item1:value,
                    item2:value
                    ...
                },{
                    year:value,
                    item1:value,
                    item2:value
                    ...
                }
            ]
        }
        balancesheet的数据格式与profitstatement相同
    '''
    result = []
    # Get balance sheet data
    balance_data = balancesheet_collection.find_one({"stockcode": stockcode})
    # Get profit statement data
    profit_data = profitstatement_collection.find_one({"stockcode": stockcode})
    
    if not balance_data or not profit_data:
        logger.error(f"No data found for stock {stockcode}")
        return {"roe": []}

    # Create a dictionary to store equity values by year
    equity_by_year = {
        year_data.get("year"): safe_float(year_data.get(EquityIdx.归属于母公司股东权益合计.name, 0))
        for year_data in balance_data.get("data", [])
    }

    # Calculate ROE for each year
    for year_data in profit_data.get("data", []):
        year = year_data.get("year")
        try:
            net_profit = safe_float(year_data.get(ProfitStatementIdx.归属于母公司所有者的净利润.name, 0))
            equity = equity_by_year.get(year, 0)
            
            if equity > 0:
                roe = round(net_profit / equity, 4)
                result.append({
                    "year": year,
                    "value": roe
                })
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating ROE for {stockcode} in year {year}: {str(e)}")
            continue

    return result


def __interest_liability_rate_calculate(stockcode:str) -> Dict[str, Any]:
    '''
    Calculate the interest liability rate
    Interest liability rate = Interest bearing liabilities / Total assets
    :param stockcode: stock code
    :return: Dictionary containing yearly interest liability rates
    '''
    result = []
    balancesheet_data = balancesheet_collection.find_one({"stockcode": stockcode})
    
    if not balancesheet_data:
        logger.error(f"No balance sheet data found for stock {stockcode}")
        return {"interest_liability_rate": []}
    
    for year_data in balancesheet_data.get("data", []):
        year = year_data.get("year")
        try:
            total_assets = safe_float(year_data.get(NonCurrentAssetsIdx.资产总计.name, 0))
            if total_assets == 0:
                continue
            
            # Calculate interest bearing liabilities
            short_term_loan = safe_float(year_data.get(CurrentLiabilitiesIdx.短期借款.name, 0))
            financial_liabilities_held_for_trading = safe_float(year_data.get(CurrentLiabilitiesIdx.交易性金融负债.name, 0))
            bills_payables = safe_float(year_data.get(CurrentLiabilitiesIdx.应付短期债券.name, 0))
            non_current_liabilities_due_within_one_year = safe_float(year_data.get(CurrentLiabilitiesIdx.一年内到期的非流动负债.name, 0))
            other_payables = safe_float(year_data.get(CurrentLiabilitiesIdx.其他应付款.name, 0))
            other_current_liabilities = safe_float(year_data.get(CurrentLiabilitiesIdx.其他流动负债.name, 0))
            
            interest_bearing_liabilities = short_term_loan + financial_liabilities_held_for_trading + bills_payables+non_current_liabilities_due_within_one_year+other_payables+other_current_liabilities
            
            # Calculate the rate
            rate = round(interest_bearing_liabilities / total_assets, 4) if total_assets else 0
            
            result.append({
                "year": year,
                "value": rate
            })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating interest liability rate for {stockcode} in year {year}: {str(e)}")
            continue
    
    return result

def __is_light_asset_calculate(stockcode:str)->None:
    '''
        Calculate the is light asset
        :param stockcode: stock code
        :return: None

        生产资产=有形资产+土地
        有形资产=固定资产+在建工程+工程物资+固定资产清理+生产性生物资产+油气资产+长期待摊费用
        这里用有形资产进行分析,没有包含无形资产里的土地
        轻资产公司，当年税前利润总额/生产资产（此处无法取得无形资产里的土地数据，所以只用有形资产代替）-> 社会平均资本回报（银行标准贷款利率的2倍）
    '''
    # 轻资产判断：利润总额/有形资产 > 2 * 银行贷款标准利率
    result = []
    balancesheet_data = balancesheet_collection.find_one({"stockcode": stockcode})
    profit_data = profitstatement_collection.find_one({"stockcode": stockcode})
    
    if not balancesheet_data or not profit_data:
        logger.error(f"No data found for stock {stockcode}")
        return {"is_light_asset": []}

    
    for year_data in balancesheet_data.get("data", []):
        year = year_data.get("year")
        try:
            # 计算有形资产总额
            fixed_assets = safe_float(year_data.get(NonCurrentAssetsIdx.固定资产净额.name, 0))
            construction_in_progress = safe_float(year_data.get(NonCurrentAssetsIdx.在建工程.name, 0))
            project_materials = safe_float(year_data.get(NonCurrentAssetsIdx.工程物资.name, 0))
            fixed_assets_disposal = safe_float(year_data.get(NonCurrentAssetsIdx.固定资产清理.name, 0))
            biological_assets = safe_float(year_data.get(NonCurrentAssetsIdx.生产性生物资产.name, 0))
            oil_gas_assets = safe_float(year_data.get(NonCurrentAssetsIdx.油气资产.name, 0))
            long_term_deferred_expenses = safe_float(year_data.get(NonCurrentAssetsIdx.长期待摊费用.name, 0))
            
            tangible_assets = (fixed_assets + construction_in_progress + project_materials + 
                             fixed_assets_disposal + biological_assets + oil_gas_assets + 
                             long_term_deferred_expenses)
            
            # 获取对应年份的利润总额
            profit_year_data = next((item for item in profit_data.get("data", []) if item.get("year") == year), None)
            if profit_year_data:
                total_profit = safe_float(profit_year_data.get(ProfitStatementIdx.四_利润总额.name, 0))
                
                if tangible_assets > 0:
                    # 计算资产回报率
                    return_rate = total_profit / tangible_assets
                    # 判断是否为轻资产（回报率是否大于银行贷款利率的2倍）
                    is_light = return_rate > (2 * ConstantsCN.BANK_LOAN_RATE)
                    
                    result.append({
                        "year": year,
                        "value": is_light,
                        "return_rate": round(return_rate, 4)
                    })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating light asset status for {stockcode} in year {year}: {str(e)}")
            continue
    
    return result
    

def __reciable_to_total_asset_calculate(stockcode:str)->None:
    '''
        Calculate the receivable to total asset
        :param stockcode: stock code
        :return: None
        应收资产=应收账款+应收利息+应收股利+其他应收款
        应收资产占比 = 应收资产/总资产
    '''
    result = []
    balancesheet_data = balancesheet_collection.find_one({"stockcode": stockcode})
    
    if not balancesheet_data:
        logger.error(f"No balance sheet data found for stock {stockcode}")
        return {"receivable_to_total_asset": []}

    for year_data in balancesheet_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get total assets
            total_assets = safe_float(year_data.get(NonCurrentAssetsIdx.资产总计.name, 0))
            if total_assets == 0:
                continue

            # Calculate total receivables
            accounts_receivable = safe_float(year_data.get(CurrentAssetsIdx.应收账款.name, 0))
            interest_receivable = safe_float(year_data.get(CurrentAssetsIdx.应收利息.name, 0))
            dividends_receivable = safe_float(year_data.get(CurrentAssetsIdx.应收股利.name, 0))
            other_receivables = safe_float(year_data.get(CurrentAssetsIdx.其他应收款.name, 0))

            total_receivables = (accounts_receivable + interest_receivable + 
                               dividends_receivable + other_receivables)

            # Calculate the ratio
            ratio = round(total_receivables / total_assets, 4) if total_assets else 0

            result.append({
                "year": year,
                "value": ratio
            })

        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating receivable to total asset ratio for {stockcode} in year {year}: {str(e)}")
            continue

    return result
    
def __gross_profit_rate_calculate(stockcode:str)->None:
    '''
        Calculate the gross profit rate
        :param stockcode: stock code
        :return: None
    '''
    result = []
    profit_data = profitstatement_collection.find_one({"stockcode": stockcode})
    
    if not profit_data:
        logger.error(f"No profit statement data found for stock {stockcode}")
        return {"gross_profit_rate": []}

    for year_data in profit_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get revenue and cost of sales
            revenue = safe_float(year_data.get(ProfitStatementIdx.营业收入.name, 0))
            cost_of_sales = safe_float(year_data.get(ProfitStatementIdx.营业成本.name, 0))
            
            if revenue > 0:
                # Calculate gross profit rate
                gross_profit = revenue - cost_of_sales
                gross_profit_rate = round(gross_profit / revenue, 4)
                
                result.append({
                    "year": year,
                    "value": gross_profit_rate
                })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating gross profit rate for {stockcode} in year {year}: {str(e)}")
            continue

    return result

def __expense_rate_calculate(stockcode:str)->None:
    '''
        Calculate the expense rate
        :param stockcode: stock code
        :return: None

        三费=销售费用+管理费用+财务费用
        三费占比 = 三费/营业收入
    '''
    result = []
    profit_data = profitstatement_collection.find_one({"stockcode": stockcode})
    if not profit_data:
        logger.error(f"No profit statement data found for stock {stockcode}")
        return {"expense_rate": []}
    for year_data in profit_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get operating income and expenses
            operating_income = safe_float(year_data.get(ProfitStatementIdx.营业收入.name, 0))
            selling_expenses = safe_float(year_data.get(ProfitStatementIdx.销售费用.name, 0))
            management_expenses = safe_float(year_data.get(ProfitStatementIdx.管理费用.name, 0))
            financial_expenses = safe_float(year_data.get(ProfitStatementIdx.财务费用.name, 0))

            total_expenses = selling_expenses + management_expenses + financial_expenses

            if operating_income > 0:
                # Calculate expense rate
                expense_rate = round(total_expenses / operating_income, 4)
                
                result.append({
                    "year": year,
                    "value": expense_rate
                })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating expense rate for {stockcode} in year {year}: {str(e)}")
            continue
    return result

def __net_operating_cash_to_net_profit_calculate(stockcode:str)->None:
    result = []
    profit_data = profitstatement_collection.find_one({"stockcode": stockcode})
    cashflow_data = cashflow_collection.find_one({"stockcode": stockcode})
    
    if not profit_data or not cashflow_data:
        logger.error(f"No data found for stock {stockcode}")
        return {"net_operating_cash_to_net_profit": []}
    
    for year_data in profit_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get net profit
            net_profit = safe_float(year_data.get(ProfitStatementIdx.归属于母公司所有者的净利润.name, 0))
            
            # Find matching cashflow data for the year
            cashflow_year_data = next(
                (item for item in cashflow_data.get("data", []) if item.get("year") == year), 
                None
            )
            
            if cashflow_year_data and net_profit > 0:
                # Get operating cash flow from matching year
                operating_cash_flow = safe_float(cashflow_year_data.get(CashFlowIdx.经营活动产生的现金流量净额.name, 0))
                # Calculate the ratio
                ratio = round(operating_cash_flow / net_profit, 4)
                
                result.append({
                    "year": year,
                    "value": ratio
                })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating ratio for {stockcode} in year {year}: {str(e)}")
            continue
    
    return result

def __net_operating_cash(stockcode:str)->None:
    '''
        Calculate the net operating cash
        :param stockcode: stock code
        :return: None

        经营活动现金流净额来自cashflow表
    '''
    result = []
    cashflow_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not cashflow_data:
        logger.error(f"No cash flow data found for stock {stockcode}")
        return {"net_operating_cash": []}
    for year_data in cashflow_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get operating cash flow
            operating_cash_flow = safe_float(year_data.get(CashFlowIdx.经营活动产生的现金流量净额.name, 0))
            
            result.append({
                "year": year,
                "value": operating_cash_flow
            })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating net operating cash for {stockcode} in year {year}: {str(e)}")
            continue
    return result
    
def __net_investment_cash(stockcode:str)->None:
    '''
        Calculate the net investment cash
        :param stockcode: stock code
        :return: None

        投资活动现金流净额来自cashflow表
    '''
    result = []
    cashflow_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not cashflow_data:
        logger.error(f"No cash flow data found for stock {stockcode}")
        return {"net_investment_cash": []}
    for year_data in cashflow_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get investment cash flow
            investment_cash_flow = safe_float(year_data.get(CashFlowIdx.投资活动产生的现金流量净额.name, 0))
            
            result.append({
                "year": year,
                "value": investment_cash_flow
            })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating net investment cash for {stockcode} in year {year}: {str(e)}")
            continue
    return result

def __net_financing_cash(stockcode:str)->None:
    '''
        Calculate the net financing cash
        :param stockcode: stock code
        :return: None
        筹资活动现金流净额来自cashflow表
    '''
    result = []
    cashflow_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not cashflow_data:
        logger.error(f"No cash flow data found for stock {stockcode}")
        return {"net_financing_cash": []}
    for year_data in cashflow_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get financing cash flow
            financing_cash_flow = safe_float(year_data.get(CashFlowIdx.筹资活动产生的现金流量净额.name, 0))
            
            result.append({
                "year": year,
                "value": financing_cash_flow
            })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating net financing cash for {stockcode} in year {year}: {str(e)}")
            continue
    return result

def __current_ratio_calculate(stockcode:str)->None:
    '''
        Calculate the current ratio
        :param stockcode: stock code
        :return: None
    '''
    result = []
    balancesheet_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not balancesheet_data:
        logger.error(f"No balance sheet data found for stock {stockcode}")
        return {"current_ratio": []}
    for year_data in balancesheet_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get current assets and current liabilities
            current_assets = safe_float(year_data.get(CurrentAssetsIdx.流动资产合计.name, 0))
            current_liabilities = safe_float(year_data.get(CurrentLiabilitiesIdx.流动负债合计.name, 0))
            
            if current_liabilities > 0:
                # Calculate the ratio
                ratio = round(current_assets / current_liabilities, 4)
                
                result.append({
                    "year": year,
                    "value": ratio
                })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating current ratio for {stockcode} in year {year}: {str(e)}")
            continue
    return result

def __quick_ratio_calculate(stockcode:str)->None:
    '''
        Calculate the quick ratio
        :param stockcode: stock code
        :return: None
        速冻比 = 速冻资产 / 流动负债
        速冻资产 = 流动资产 - 存货 - 预付账款
    '''
    result = []
    balancesheet_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not balancesheet_data:
        logger.error(f"No balance sheet data found for stock {stockcode}")
        return {"quick_ratio": []}
    for year_data in balancesheet_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get current assets and current liabilities
            current_assets = safe_float(year_data.get(CurrentAssetsIdx.流动资产合计.name, 0))
            inventory = safe_float(year_data.get(CurrentAssetsIdx.存货.name, 0))
            #prepayments = float(year_data.get(CurrentAssetsIdx.预付账款.name, 0))
            current_liabilities = safe_float(year_data.get(CurrentLiabilitiesIdx.流动负债合计.name, 0))

            # Calculate quick assets
            quick_assets = current_assets - inventory
            
            if current_liabilities > 0:
                # Calculate the ratio
                ratio = round(quick_assets / current_liabilities, 4)
                
                result.append({
                    "year": year,
                    "value": ratio
                })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating quick ratio for {stockcode} in year {year}: {str(e)}")
            continue
    return result

def __cash_and_equivalents(stockcode:str)->None:
    '''
        Calculate the cash and equivalents
        :param stockcode: stock code
        :return: None
        现金及现金等价物净增加额来自cashflow表
    '''
    result = []
    cashflow_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not cashflow_data:
        logger.error(f"No cash flow data found for stock {stockcode}")
        return {"cash_and_equivalents": []}
    for year_data in cashflow_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get cash and equivalents
            cash_and_equivalents = safe_float(year_data.get(CashFlowIdx.五_现金及现金等价物净增加额.name, 0))
            
            result.append({
                "year": year,
                "value": cash_and_equivalents
            })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating cash and equivalents for {stockcode} in year {year}: {str(e)}")
            continue
    return result

def __final_cash_and_equivalents_to_intrest_liability_calculate(stockcode:str)->None:
    '''
        Calculate the final cash and equivalents to intrest liability
        :param stockcode: stock code
        :return: None
        计算“现金及现金等价物余额/有息负债”
        现金及现金等价物的余额在cashflow表中
        有息负债参考__interest_liability_rate_calculate中计算有息负债的方法
    '''
    result = []
    balancesheet_data = balancesheet_collection.find_one({"stockcode": stockcode})
    if not balancesheet_data:
        logger.error(f"No balance sheet data found for stock {stockcode}")
        return {"final_cash_and_equivalents_to_interest_liability": []}
    for year_data in balancesheet_data.get("data", []):
        year = year_data.get("year")
        try:
            # Get cash and equivalents
            cash_and_equivalents = safe_float(year_data.get(CashFlowIdx.六_期末现金及现金等价物余额.name, 0))
            # Calculate interest bearing liabilities
            short_term_loan = safe_float(year_data.get(CurrentLiabilitiesIdx.短期借款.name, 0))
            financial_liabilities_held_for_trading = safe_float(year_data.get(CurrentLiabilitiesIdx.交易性金融负债.name, 0))
            bills_payables = safe_float(year_data.get(CurrentLiabilitiesIdx.应付短期债券.name, 0))
            non_current_liabilities_due_within_one_year = safe_float(year_data.get(CurrentLiabilitiesIdx.一年内到期的非流动负债.name, 0))
            other_payables = safe_float(year_data.get(CurrentLiabilitiesIdx.其他应付款.name, 0))
            other_current_liabilities = safe_float(year_data.get(CurrentLiabilitiesIdx.其他流动负债.name, 0))

            interest_bearing_liabilities = short_term_loan + financial_liabilities_held_for_trading + bills_payables+non_current_liabilities_due_within_one_year+other_payables+other_current_liabilities
            
            if interest_bearing_liabilities > 0:
                # Calculate the ratio
                ratio = round(cash_and_equivalents / interest_bearing_liabilities, 4)
                
                result.append({
                    "year": year,
                    "value": ratio
                })
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating final cash and equivalents to interest liability for {stockcode} in year {year}: {str(e)}")
            continue
    return result

if __name__ == '__main__' :
    #__roe_calculate("600519")
    get_metrix_model("600519",0)