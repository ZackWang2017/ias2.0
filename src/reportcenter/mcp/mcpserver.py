#coding:utf8

from mcp.server.fastmcp import FastMCP

# 初始化FastMCP服务端
mcp = FastMCP("reportcenter")

@mcp.tool()
def get_tang_metrix(symbol:str):
    
    "todo: 这里需要实现获取tang_metrix的逻辑"
    return f"{'test': 1234567890}"

if __name__ == "__main__":
    # 初始化并运行服务端
    mcp.run(transport='stdio')