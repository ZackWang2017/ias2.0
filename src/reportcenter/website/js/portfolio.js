document.addEventListener('DOMContentLoaded', function() {
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const userMenuBtn = document.getElementById('userMenuBtn');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    const addPositionBtn = document.getElementById('addPosition');
    const stockDetail = document.querySelector('.stock-detail');

    // User menu dropdown
    userMenuBtn.addEventListener('click', () => {
        dropdownMenu.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!userMenuBtn.contains(e.target)) {
            dropdownMenu.classList.remove('show');
        }
    });

    // Load stock details when clicking portfolio item
    portfolioItems.forEach(item => {
        item.addEventListener('click', () => {
            portfolioItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            // Get stock code from the clicked item
            const stockCode = item.querySelector('.stock-name').textContent.match(/\((\d+)\)/)[1];
            loadStockDetails(stockCode);
        });
    });

    // Add new position
    addPositionBtn.addEventListener('click', () => {
        showAddPositionModal();
    });

    // Load stock details function
    async function loadStockDetails(stockCode) {
        try {
            // Show loading state
            stockDetail.innerHTML = '<div class="loading">Loading...</div>';
            
            // Fetch stock details from API
            const response = await fetch(`/api/stock/${stockCode}`);
            const data = await response.json();
            
            // Update UI with stock details
            updateStockDetails(data);
        } catch (error) {
            console.error('Error loading stock details:', error);
            stockDetail.innerHTML = '<div class="error">Failed to load stock details</div>';
        }
    }

    // Update stock details UI
    function updateStockDetails(data) {
        const detailHTML = `
            <div class="detail-header">
                <h2>股票详情</h2>
            </div>
            <div class="detail-content">
                <div class="detail-section">
                    <h3>基本信息</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">股票代码</span>
                            <span class="value">${data.code}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">股票名称</span>
                            <span class="value">${data.name}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">当前价格</span>
                            <span class="value">${data.currentPrice}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">成本价格</span>
                            <span class="value">${data.costPrice}</span>
                        </div>
                    </div>
                </div>
                <div class="detail-section">
                    <h3>持仓信息</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">持仓数量</span>
                            <span class="value">${data.shares}股</span>
                        </div>
                        <div class="info-item">
                            <span class="label">持仓市值</span>
                            <span class="value">${data.marketValue}元</span>
                        </div>
                        <div class="info-item">
                            <span class="label">浮动盈亏</span>
                            <span class="value ${data.profit >= 0 ? 'profit' : 'loss'}">${data.profit}元</span>
                        </div>
                        <div class="info-item">
                            <span class="label">盈亏比例</span>
                            <span class="value ${data.profitRatio >= 0 ? 'profit' : 'loss'}">${data.profitRatio}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        stockDetail.innerHTML = detailHTML;
    }

    // Auto-refresh prices every minute
    setInterval(() => {
        portfolioItems.forEach(item => {
            if (item.classList.contains('active')) {
                const stockCode = item.querySelector('.stock-name').textContent.match(/\((\d+)\)/)[1];
                loadStockDetails(stockCode);
            }
        });
    }, 60000);
});