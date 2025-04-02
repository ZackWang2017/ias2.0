# Investment Analysis System 2.0 | 投资分析系统 2.0

A comprehensive system for investment analysis and portfolio management.
一个完整的投资分析和投资组合管理系统。

![License](https://img.shields.io/github/license/yourusername/ias2.0)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## Overview | 概述

IAS 2.0 is a modern web-based platform that helps investors analyze stocks and manage their portfolios. It provides comprehensive financial analysis tools, technical indicators, and portfolio tracking capabilities.

IAS 2.0 是一个现代化的网络平台，帮助投资者分析股票和管理投资组合。它提供全面的财务分析工具、技术指标和投资组合跟踪功能。

### Key Features | 主要特点

- 🔍 Advanced stock screening and analysis | 高级股票筛选和分析
- 📊 Financial ratio analysis (TangMetrix) | 财务比率分析（唐系数）
- 📈 Technical analysis indicators | 技术分析指标
- 💼 Portfolio management and tracking | 投资组合管理和跟踪
- 📱 Responsive web interface | 响应式网页界面

## Installation | 安装

### Prerequisites | 前置要求

- Python 3.8 or higher | Python 3.8 或更高版本
- pip (Python package installer) | pip（Python包安装器）
- Git | Git版本控制系统

### Quick Start | 快速开始

```bash
# Clone the repository | 克隆仓库
git clone https://github.com/yourusername/ias2.0.git
cd ias2.0

# Create a virtual environment | 创建虚拟环境
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies | 安装依赖
pip install -e ".[dev]"
```

## Development | 开发

### Project Structure | 项目结构

```
ias2.0/
├── src/
│   ├── reportcenter/      # Report generation and analysis | 报告生成和分析
│   ├── datacenter/        # Data collection and processing | 数据收集和处理
│   └── website/           # Web interface | 网页界面
├── tests/                 # Test files | 测试文件
└── docs/                  # Documentation | 文档
```

### Running Tests | 运行测试

```bash
# Run all tests | 运行所有测试
pytest

# Run tests with coverage | 运行测试并生成覆盖率报告
pytest --cov=src tests/
```

### Contributing | 贡献指南

1. Fork the repository | 复刻仓库
2. Create a feature branch | 创建特性分支
3. Commit your changes | 提交更改
4. Push to the branch | 推送到分支
5. Submit a pull request | 提交拉取请求

## Documentation | 文档

Detailed documentation is available at [docs/index.md](docs/index.md)
详细文档请参见 [docs/index.md](docs/index.md)

## License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

## Acknowledgments | 致谢

- Thanks to all contributors | 感谢所有贡献者
- Special thanks to the open source community | 特别感谢开源社区

## Contact | 联系方式

- Author: Your Name | 作者：您的名字
- Email: your.email@example.com | 邮箱：your.email@example.com
- Project Link: https://github.com/yourusername/ias2.0 | 项目链接：https://github.com/yourusername/ias2.0