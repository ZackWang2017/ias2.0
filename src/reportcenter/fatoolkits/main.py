import argparse
from enum import Enum
import sys
import questionary

from colorama import Fore, Style

from utils.market import StockMarket

class Toolkits(Enum):
    FINANCE_TANG_METRIX = "FananceTangMetrix"

MARKET_CONFIG = {
    "cn": {
        "display_name": "A 股",
        "order": 0,
    },
    "usa": {
        "display_name": "美股",
        "order": 1,
    }
}
MARKET_ORDER = [(config["display_name"], key) for key, config in sorted(MARKET_CONFIG.items(), key=lambda x: x[1]["order"])]
TOOLKIT_CONFIG = {
    "fin_tang_metrix": {
        "display_name": "导出初步筛选指标和财务报表到Excel",
        "order": 0,
    }
}
TOOLKIT_ORDER = [(config["display_name"], key) for key, config in sorted(TOOLKIT_CONFIG.items(), key=lambda x: x[1]["order"])]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="投资分析助手")
    
    # Select market
    market = questionary.select(
        "请选择市场:",
        choices=[questionary.Choice(display, value=value) for display, value in MARKET_ORDER]
    ).ask()

    stock_code = questionary.text("请输入股票代码:").ask()
    if not stock_code:
        print(Fore.RED + "股票代码不能为空" + Style.RESET_ALL)
        sys.exit(1)


    # Select toolkit
    toolkit = questionary.select(
        "请选择分析工具:",
        choices=[questionary.Choice(display, value=value) for display, value in TOOLKIT_ORDER]
    ).ask()  