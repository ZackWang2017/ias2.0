document.addEventListener('DOMContentLoaded', function() {
    // 初始化变量
    const stockSearch = document.getElementById('stockSearch');
    const generateBtn = document.getElementById('generateReport');
    const historyList = document.getElementById('analysisHistory');
    const historyChips = document.getElementById('historyChips');
    const prevBtn = document.getElementById('prevHistory');
    const nextBtn = document.getElementById('nextHistory');
    const contentArea = document.getElementById('analysisContent');

    // 模拟历史记录数据
    const mockHistory = [
        {
            stockCode: '600000',
            stockName: '浦发银行',
            date: '2025-04-02',
            analysisTypes: ['TangMetrix分析', '财务分析']
        },
        // 可以添加更多模拟数据
    ];

    // Mock data for demonstration - replace with actual data storage
    const analysisHistory = {
        '600000': {
            name: '浦发银行',
            date: '2025-04-02',
            content: `
                <div class="analysis-report">
                    <h4>浦发银行(600000) - 分析报告</h4>
                    <div class="report-section">
                        <h5>TangMetrix 分析结果</h5>
                        <p>核心财务指标评分：8.5/10</p>
                        <p>盈利能力：良好</p>
                        <p>营运能力：优秀</p>
                    </div>
                </div>
            `
        },
        // Add more historical data...
    };

    // 渲染历史记录
    function renderHistory(historyData) {
        historyList.innerHTML = '';
        historyData.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <div>${item.stockCode} - ${item.stockName}</div>
                <div>分析日期：${item.date}</div>
                <div>分析类型：${item.analysisTypes.join(', ')}</div>
            `;
            historyList.appendChild(historyItem);
        });
    }

    // 生成报告按钮点击事件
    generateBtn.addEventListener('click', function() {
        const stockCode = stockSearch.value.trim();
        if (!stockCode) {
            alert('请输入股票代码或名称');
            return;
        }

        const selectedOptions = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.nextElementSibling.textContent);

        if (selectedOptions.length === 0) {
            alert('请至少选择一项分析类型');
            return;
        }

        // 这里添加生成报告的逻辑
        console.log('生成报告:', {
            stockCode,
            analysisTypes: selectedOptions
        });
    });

    // 初始化显示历史记录
    renderHistory(mockHistory);

    document.getElementById('searchBtn').addEventListener('click', function() {
        const searchValue = document.getElementById('stockSearch').value.trim();
        if (searchValue) {
            // Update active chip or add new one
            updateActiveChip(searchValue);
        }
    });

    function updateActiveChip(stockInfo) {
        const chips = document.querySelectorAll('.history-chip');
        let found = false;
        
        // First try to find and activate existing chip
        chips.forEach(chip => {
            if (chip.textContent.includes(stockInfo)) {
                chips.forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                found = true;
            }
        });
        
        // If not found, add new chip
        if (!found) {
            const historyChips = document.getElementById('historyChips');
            const newChip = document.createElement('span');
            newChip.className = 'history-chip active';
            newChip.textContent = stockInfo;
            
            // Remove active class from other chips
            chips.forEach(c => c.classList.remove('active'));
            
            // Add new chip at the beginning
            if (historyChips.firstChild) {
                historyChips.insertBefore(newChip, historyChips.firstChild);
            } else {
                historyChips.appendChild(newChip);
            }
            
            // Update navigation visibility
            updateNavigationVisibility();
        }
    }

    // Update click handler for history chips
    document.getElementById('historyChips').addEventListener('click', function(e) {
        if (e.target.classList.contains('history-chip')) {
            const chips = document.querySelectorAll('.history-chip');
            chips.forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');
            
            // Load corresponding content
            const stockCode = e.target.textContent.match(/\((\d+)\)/)[1];
            loadAnalysisContent(stockCode);
        }
    });

    document.getElementById('stockSearch').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const searchValue = this.value.trim();
            if (searchValue) {
                searchStock(searchValue);
            }
        }
    });

    async function searchStock(query) {
        try {
            // Here you would typically make an API call to your backend
            // For now, we'll just show a mock result
            const searchResult = document.getElementById('searchResult');
            searchResult.style.display = 'block';
            
            // You can replace this with actual API call and data
            // const response = await fetch(`/api/stock/search?q=${query}`);
            // const data = await response.json();
            
            // For demo purposes, we'll keep the static content
        } catch (error) {
            console.error('Error searching stock:', error);
            // Add error handling UI feedback here
        }
    }

    function updateAnalysisProgress(step, status) {
        const timelineItem = document.querySelector(`.timeline-item[data-step="${step}"]`);
        
        if (status === 'in-progress') {
            timelineItem.classList.remove('pending', 'completed');
            timelineItem.classList.add('in-progress');
        } else if (status === 'completed') {
            timelineItem.classList.remove('pending', 'in-progress');
            timelineItem.classList.add('completed');
        } else {
            timelineItem.classList.remove('in-progress', 'completed');
            timelineItem.classList.add('pending');
        }
    }

    // Example usage:
    document.getElementById('generateReport').addEventListener('click', async function() {
        // Step 1: TangMetrix Analysis
        updateAnalysisProgress(1, 'in-progress');
        await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate analysis
        updateAnalysisProgress(1, 'completed');
        
        // Step 2: Financial Analysis
        updateAnalysisProgress(2, 'in-progress');
        await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate analysis
        updateAnalysisProgress(2, 'completed');
        
        // Step 3: Technical Analysis
        updateAnalysisProgress(3, 'in-progress');
        await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate analysis
        updateAnalysisProgress(3, 'completed');
    });

    document.getElementById('start-analyze').addEventListener('click', async function() {
        const stockInfo = document.querySelector('.stock-basic-info h4').textContent;
        await runAnalysis();
        loadAnalysisContent(stockInfo);
    });

    async function runAnalysis() {
        // Your existing analysis code
    }

    document.getElementById('start-analyze').addEventListener('click', async function() {
        // Disable the button
        this.disabled = true;
        this.classList.add('disabled');

        // Get all timeline items
        const timelineItems = document.querySelectorAll('.timeline-item');
        
        for (const item of timelineItems) {
            // Disable the item
            item.classList.add('disabled');
            
            // Start processing animation
            item.classList.add('processing');
            
            // Process all sub-items
            const subItems = item.querySelectorAll('.sub-timeline-item');
            for (const subItem of subItems) {
                subItem.classList.add('disabled');
                subItem.classList.add('processing');
                
                // Simulate processing time
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Complete sub-item
                subItem.classList.remove('processing');
                subItem.classList.add('completed');
            }
            
            // Complete main item
            await new Promise(resolve => setTimeout(resolve, 1000));
            item.classList.remove('processing');
            item.classList.add('completed');
        }
        
        // Re-enable the button
        this.disabled = false;
        this.classList.remove('disabled');
    });

    // Handle history navigation
    let scrollPosition = 0;
    const scrollAmount = 200;

    prevBtn.addEventListener('click', () => {
        scrollPosition = Math.max(0, scrollPosition - scrollAmount);
        historyChips.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
        updateNavigationVisibility();
    });

    nextBtn.addEventListener('click', () => {
        scrollPosition = Math.min(
            historyChips.scrollWidth - historyChips.clientWidth,
            scrollPosition + scrollAmount
        );
        historyChips.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
        updateNavigationVisibility();
    });

    function updateNavigationVisibility() {
        const isScrollable = historyChips.scrollWidth > historyChips.clientWidth;
        prevBtn.style.display = isScrollable ? 'flex' : 'none';
        nextBtn.style.display = isScrollable ? 'flex' : 'none';
        
        if (isScrollable) {
            prevBtn.disabled = scrollPosition <= 0;
            nextBtn.disabled = scrollPosition >= historyChips.scrollWidth - historyChips.clientWidth;
        }
    }

    // Handle window resize
    window.addEventListener('resize', updateNavigationVisibility);

    // Initial visibility check
    updateNavigationVisibility();

    // Handle chip selection and content display
    const chips = document.querySelectorAll('.history-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            // Update active state
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            
            // Extract stock code from chip text
            const stockCode = chip.textContent.match(/\((\d+)\)/)[1];
            
            // Display historical content
            if (analysisHistory[stockCode]) {
                contentArea.innerHTML = analysisHistory[stockCode].content;
                contentArea.classList.add('loaded');
            } else {
                contentArea.innerHTML = '<div class="no-content">暂无分析记录</div>';
            }
        });
    });

    // Initial button state
    updateNavigationVisibility();
});

function loadAnalysisContent(stockInfo) {
    const contentArea = document.getElementById('analysisContent');
    contentArea.className = 'content-area markdown-body';
    
    // Example markdown content - replace with actual analysis data
    const markdownContent = `
# ${stockInfo} 分析报告

## TangMetrix 分析结果

### 核心指标得分
- ROE: **15.2%** ⭐⭐⭐⭐
- 毛利率: **42.8%** ⭐⭐⭐
- 营收增速: **23.5%** ⭐⭐⭐⭐⭐

### 财务质量评估
| 指标 | 数值 | 行业均值 | 评级 |
|------|------|----------|------|
| 现金流质量 | 0.95 | 0.82 | 优秀 |
| 资产周转率 | 1.2 | 0.9 | 良好 |
| 负债率 | 65% | 70% | 适中 |

## 技术分析
\`\`\`
MA(20) = 34.56
MA(60) = 32.12
MACD = 正金叉
RSI = 58.3
\`\`\`

> 综合建议：基本面良好，技术面呈现上升趋势，可以考虑逢低买入。
`;

    // Convert markdown to HTML
    contentArea.innerHTML = marked(markdownContent);
}