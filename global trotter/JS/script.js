// 全局功能函数

// 模拟后端API调用
const mockAPI = {
    // 获取用户数据
    getUserProfile: function(userId) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    id: userId,
                    name: "Velvety Finch",
                    email: "user@example.com",
                    phone: "+1234567890",
                    city: "New York",
                    country: "USA",
                    avatar: "default-avatar.jpg"
                });
            }, 500);
        });
    },
    
    // 获取用户行程
    getUserTrips: function(userId, type = 'all') {
        return new Promise((resolve) => {
            const trips = {
                ongoing: [
                    { id: 1, name: "Paris Trip", dates: "Jan 5-12, 2024", status: "active" },
                    { id: 2, name: "Japan Adventure", dates: "Jan 15-22, 2024", status: "active" }
                ],
                upcoming: [
                    { id: 3, name: "NYC Getaway", dates: "Jan 28-Feb 5, 2024", status: "upcoming" }
                ],
                completed: [
                    { id: 4, name: "European Tour", dates: "Dec 2023", status: "completed" },
                    { id: 5, name: "Tropical Vacation", dates: "Nov 2023", status: "completed" }
                ]
            };
            
            setTimeout(() => {
                if (type === 'all') {
                    resolve([...trips.ongoing, ...trips.upcoming, ...trips.completed]);
                } else {
                    resolve(trips[type] || []);
                }
            }, 500);
        });
    },
    
    // 获取日历事件
    getCalendarEvents: function(year, month) {
        return new Promise((resolve) => {
            const events = [
                { date: '2024-01-05', title: 'Paris Trip', duration: '5-12 Jan' },
                { date: '2024-01-15', title: 'Japan Adventure', duration: '15-22 Jan' },
                { date: '2024-01-28', title: 'NYC Getaway', duration: '28 Jan - 5 Feb' }
            ];
            
            setTimeout(() => resolve(events), 500);
        });
    },
    
    // 搜索活动
    searchActivities: function(query, filters) {
        return new Promise((resolve) => {
            const results = [
                { 
                    id: 1, 
                    name: "Euphoric Wolf Paragliding", 
                    location: "Swiss Alps", 
                    price: "$150",
                    rating: 4.8,
                    description: "Experience the thrill of paragliding over beautiful mountain ranges."
                },
                // 更多结果...
            ];
            
            setTimeout(() => resolve(results), 600);
        });
    },
    
    // 管理员数据
    getAdminStats: function() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    averageUsers: 1250,
                    popularCities: [
                        { name: "Paris", count: 345 },
                        { name: "Tokyo", count: 298 },
                        { name: "New York", count: 267 }
                    ],
                    popularActivities: [
                        { name: "Paragliding", count: 156 },
                        { name: "Scuba Diving", count: 142 },
                        { name: "City Tours", count: 189 }
                    ],
                    userTrends: {
                        monthlyGrowth: "12%",
                        activeUsers: 3245,
                        newRegistrations: 234
                    }
                });
            }, 500);
        });
    }
};

// 工具函数
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showLoading(element) {
    element.innerHTML = '<div class="loading">Loading...</div>';
}

function hideLoading(element) {
    // 移除加载状态
}

// 初始化日历
function initCalendar(year, month) {
    // 日历初始化逻辑
    const calendarGrid = document.querySelector('.calendar-grid');
    if (!calendarGrid) return;
    
    // 这里将生成日历网格和事件
    // 实际实现需要完整的日历逻辑
}

// 事件监听器设置
document.addEventListener('DOMContentLoaded', function() {
    // 全局事件监听
    const searchInputs = document.querySelectorAll('.search-bar input');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                // 执行搜索
                performSearch(this.value);
            }
        });
    });
    
    // 如果有日历页面，初始化日历
    if (window.location.pathname.includes('calendar.html')) {
        const now = new Date();
        initCalendar(now.getFullYear(), now.getMonth());
    }
    
    // 管理员面板数据加载
    if (window.location.pathname.includes('admin.html')) {
        loadAdminData();
    }
});

// 加载管理员数据
async function loadAdminData() {
    try {
        const stats = await mockAPI.getAdminStats();
        
        // 更新DOM元素
        document.getElementById('average-users').textContent = stats.averageUsers.toLocaleString();
        
        // 填充热门城市
        const citiesContainer = document.getElementById('popular-cities');
        if (citiesContainer) {
            citiesContainer.innerHTML = stats.popularCities
                .map(city => `<div>${city.name}: ${city.count} visits</div>`)
                .join('');
        }
        
        // 填充热门活动
        const activitiesContainer = document.getElementById('popular-activities');
        if (activitiesContainer) {
            activitiesContainer.innerHTML = stats.popularActivities
                .map(activity => `<div>${activity.name}: ${activity.count}</div>`)
                .join('');
        }
        
        // 填充用户趋势
        const trendsContainer = document.getElementById('user-trends');
        if (trendsContainer) {
            trendsContainer.innerHTML = `
                <div>Monthly Growth: ${stats.userTrends.monthlyGrowth}</div>
                <div>Active Users: ${stats.userTrends.activeUsers.toLocaleString()}</div>
                <div>New Registrations: ${stats.userTrends.newRegistrations}</div>
            `;
        }
    } catch (error) {
        console.error('Error loading admin data:', error);
    }
}

// 搜索功能
async function performSearch(query) {
    if (!query.trim()) return;
    
    try {
        const results = await mockAPI.searchActivities(query, {});
        
        // 在搜索页面显示结果
        if (window.location.pathname.includes('search.html')) {
            displaySearchResults(results);
        } else {
            // 重定向到搜索页面
            window.location.href = `search.html?q=${encodeURIComponent(query)}`;
        }
    } catch (error) {
        console.error('Search error:', error);
    }
}

// 显示搜索结果
function displaySearchResults(results) {
    const container = document.getElementById('search-results');
    if (!container) return;
    
    container.innerHTML = results.map(result => `
        <div class="search-result card">
            <h3>${result.name}</h3>
            <p>${result.description}</p>
            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                <span>Location: ${result.location}</span>
                <span>Price: ${result.price}</span>
                <span>Rating: ${result.rating}/5</span>
            </div>
            <button class="btn btn-primary" style="margin-top: 10px;">View Details</button>
        </div>
    `).join('');
}