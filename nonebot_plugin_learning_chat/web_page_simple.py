"""简化的 Web 管理界面 - 不依赖 amis-python"""

# 登录页面 HTML
LOGIN_PAGE_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 | Learning-Chat 后台管理</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #667eea;
            font-size: 24px;
            margin-top: 10px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #5568d3;
        }
        .error {
            color: #f56565;
            font-size: 14px;
            margin-top: 10px;
            display: none;
        }
        .info {
            color: #718096;
            font-size: 12px;
            margin-top: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>🤖 Learning-Chat</h1>
            <p style="color: #718096; margin-top: 5px;">后台管理系统</p>
        </div>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" id="username" name="username" placeholder="请输入用户名" required>
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" id="password" name="password" placeholder="请输入密码" required>
            </div>
            <button type="submit" class="btn">登录</button>
            <div class="error" id="error"></div>
            <div class="info">默认用户名: chat / 默认密码: admin</div>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('error');
            
            try {
                const response = await fetch('/learning_chat/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (data.status === 0) {
                    localStorage.setItem('token', data.data.token);
                    window.location.href = '/learning_chat/admin';
                } else {
                    errorDiv.textContent = data.msg || '登录失败';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = '网络错误，请稍后重试';
                errorDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

# 管理页面 HTML
ADMIN_PAGE_HTML = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learning-Chat 后台管理</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f7fafc;
        }}
        .header {{
            background: white;
            padding: 15px 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{
            color: #667eea;
            font-size: 20px;
        }}
        .logout-btn {{
            padding: 8px 16px;
            background: #f56565;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .container {{
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .card h2 {{
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 18px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-card h3 {{
            font-size: 32px;
            margin-bottom: 5px;
        }}
        .stat-card p {{
            opacity: 0.9;
        }}
        .table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .table th, .table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        .table th {{
            background: #f7fafc;
            font-weight: 600;
            color: #2d3748;
        }}
        .btn {{
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 5px;
        }}
        .btn-primary {{ background: #667eea; color: white; }}
        .btn-danger {{ background: #f56565; color: white; }}
        .btn-success {{ background: #48bb78; color: white; }}
        .loading {{
            text-align: center;
            padding: 40px;
            color: #718096;
        }}
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .tab {{
            padding: 10px 20px;
            cursor: pointer;
            border: none;
            background: none;
            color: #718096;
            font-size: 15px;
            position: relative;
        }}
        .tab.active {{
            color: #667eea;
            font-weight: 600;
        }}
        .tab.active::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: #667eea;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .form-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .form-field {{
            margin-bottom: 15px;
        }}
        .form-field label {{
            display: block;
            margin-bottom: 5px;
            color: #2d3748;
            font-weight: 500;
            font-size: 14px;
        }}
        .form-field input, .form-field select, .form-field textarea {{
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            font-size: 14px;
        }}
        .form-field input:focus, .form-field select:focus, .form-field textarea:focus {{
            outline: none;
            border-color: #667eea;
        }}
        .form-field small {{
            display: block;
            margin-top: 4px;
            color: #718096;
            font-size: 12px;
        }}
        .config-section {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .config-section h3 {{
            color: #2d3748;
            margin-bottom: 15px;
            font-size: 16px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }}
        .btn-group {{
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }}
        .success-msg {{
            background: #48bb78;
            color: white;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 15px;
            display: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Learning-Chat 管理控制台</h1>
        <button class="logout-btn" onclick="logout()">退出登录</button>
    </div>
    
    <div class="container">
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3 id="messageCount">-</h3>
                <p>消息总数</p>
            </div>
            <div class="stat-card">
                <h3 id="contextCount">-</h3>
                <p>学习内容</p>
            </div>
            <div class="stat-card">
                <h3 id="answerCount">-</h3>
                <p>学习回复</p>
            </div>
            <div class="stat-card">
                <h3 id="blacklistCount">-</h3>
                <p>禁用词</p>
            </div>
        </div>
        
        <div class="card">
            <h2>📊 管理中心</h2>
            <div class="tabs">
                <button class="tab active" onclick="switchTab('config')">⚙️ 配置</button>
                <button class="tab" onclick="switchTab('messages')">💬 消息记录</button>
                <button class="tab" onclick="switchTab('contexts')">📚 学习内容</button>
                <button class="tab" onclick="switchTab('answers')">💡 学习回复</button>
                <button class="tab" onclick="switchTab('blacklist')">🚫 禁用列表</button>
            </div>
            
            <div id="config" class="tab-content active">
                <p class="loading">加载中...</p>
            </div>
            
            <div id="messages" class="tab-content">
                <p class="loading">加载中...</p>
            </div>
            <div id="contexts" class="tab-content">
                <p class="loading">加载中...</p>
            </div>
            <div id="answers" class="tab-content">
                <p class="loading">加载中...</p>
            </div>
            <div id="blacklist" class="tab-content">
                <p class="loading">加载中...</p>
            </div>
        </div>
    </div>
    
    <script>
        const API_BASE = '/learning_chat/api';
        let token = localStorage.getItem('token');
        
        if (!token) {{
            window.location.href = '/learning_chat/login';
        }}
        
        async function apiCall(endpoint, options = {{}}) {{
            const response = await fetch(API_BASE + endpoint, {{
                ...options,
                headers: {{
                    ...options.headers,
                    'token': token,
                    'Content-Type': 'application/json'
                }}
            }});
            const data = await response.json();
            if (data.status === -100 || data.detail) {{
                logout();
                return null;
            }}
            return data;
        }}
        
        function logout() {{
            localStorage.removeItem('token');
            window.location.href = '/learning_chat/login';
        }}
        
        async function loadStats() {{
            const [messages, contexts, answers, blacklist] = await Promise.all([
                apiCall('/get_chat_messages?perPage=1'),
                apiCall('/get_chat_contexts?perPage=1'),
                apiCall('/get_chat_answers?perPage=1'),
                apiCall('/get_chat_blacklist?perPage=1')
            ]);
            
            document.getElementById('messageCount').textContent = messages?.data?.total || 0;
            document.getElementById('contextCount').textContent = contexts?.data?.total || 0;
            document.getElementById('answerCount').textContent = answers?.data?.total || 0;
            document.getElementById('blacklistCount').textContent = blacklist?.data?.total || 0;
        }}
        
        function switchTab(tabName) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
            
            if (tabName === 'config') loadConfig();
            else if (tabName === 'messages') loadMessages();
            else if (tabName === 'contexts') loadContexts();
            else if (tabName === 'answers') loadAnswers();
            else if (tabName === 'blacklist') loadBlacklist();
        }}
        
        async function loadMessages() {{
            const data = await apiCall('/get_chat_messages?perPage=20');
            if (!data) return;
            
            const html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>群ID</th>
                            <th>用户ID</th>
                            <th>消息</th>
                            <th>时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{data.data.items.map(item => `
                            <tr>
                                <td>${{item.group_id}}</td>
                                <td>${{item.user_id}}</td>
                                <td>${{(item.raw_message || '').substring(0, 50)}}...</td>
                                <td>${{new Date(item.time * 1000).toLocaleString()}}</td>
                                <td>
                                    <button class="btn btn-danger" onclick="deleteItem('message', ${{item.id}})">删除</button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            document.getElementById('messages').innerHTML = html;
        }}
        
        async function loadContexts() {{
            const data = await apiCall('/get_chat_contexts?perPage=20');
            if (!data) return;
            
            const html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>内容/关键词</th>
                            <th>已学次数</th>
                            <th>时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{data.data.items.map(item => `
                            <tr>
                                <td>${{(item.keywords || '').substring(0, 50)}}</td>
                                <td>${{item.count}}</td>
                                <td>${{new Date(item.time * 1000).toLocaleString()}}</td>
                                <td>
                                    <button class="btn btn-danger" onclick="banItem('context', ${{item.id}})">禁用</button>
                                    <button class="btn btn-danger" onclick="deleteItem('context', ${{item.id}})">删除</button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            document.getElementById('contexts').innerHTML = html;
        }}
        
        async function loadAnswers() {{
            const data = await apiCall('/get_chat_answers?perPage=20');
            if (!data) return;
            
            const html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>群ID</th>
                            <th>关键词</th>
                            <th>次数</th>
                            <th>时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{data.data.items.map(item => `
                            <tr>
                                <td>${{item.group_id}}</td>
                                <td>${{(item.keywords || '').substring(0, 50)}}</td>
                                <td>${{item.count}}</td>
                                <td>${{new Date(item.time * 1000).toLocaleString()}}</td>
                                <td>
                                    <button class="btn btn-danger" onclick="banItem('answer', ${{item.id}})">禁用</button>
                                    <button class="btn btn-danger" onclick="deleteItem('answer', ${{item.id}})">删除</button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            document.getElementById('answers').innerHTML = html;
        }}
        
        async function loadBlacklist() {{
            const data = await apiCall('/get_chat_blacklist?perPage=20');
            if (!data) return;
            
            const html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>内容/关键词</th>
                            <th>禁用范围</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{data.data.items.map(item => `
                            <tr>
                                <td>${{(item.keywords || '').substring(0, 50)}}</td>
                                <td>${{item.global_ban ? '全局禁用' : '部分群禁用'}}</td>
                                <td>
                                    <button class="btn btn-success" onclick="deleteItem('blacklist', ${{item.id}})">取消禁用</button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            document.getElementById('blacklist').innerHTML = html;
        }}
        
        async function deleteItem(type, id) {{
            if (!confirm('确定要删除吗？')) return;
            await apiCall(`/delete_chat?type=${{type}}&id=${{id}}`, {{ method: 'DELETE' }});
            loadStats();
            switchTab(type === 'message' ? 'messages' : type === 'context' ? 'contexts' : type === 'answer' ? 'answers' : 'blacklist');
        }}
        
        async function banItem(type, id) {{
            if (!confirm('确定要禁用吗？')) return;
            await apiCall(`/ban_chat?type=${{type}}&id=${{id}}`, {{ method: 'PUT' }});
            loadStats();
            switchTab(type === 'context' ? 'contexts' : 'answers');
        }}
        
        async function loadConfig() {{
            const data = await apiCall('/get_group_list');
            if (!data || data.status !== 0) {{
                document.getElementById('config').innerHTML = '<p class="loading">获取配置失败</p>';
                return;
            }}
            
            const groupList = data.data.group_list || [];
            
            const html = `
                <div id="successMsg" class="success-msg">保存成功！</div>
                
                <div class="config-section">
                    <h3>🌍 全局配置</h3>
                    <div id="globalConfigForm">
                        <div class="form-grid">
                            <div class="form-field">
                                <label>
                                    <input type="checkbox" id="total_enable"> 群聊学习总开关
                                </label>
                                <small>关闭后将不会学习和回复，但仍会记录消息</small>
                            </div>
                            <div class="form-field">
                                <label>单句关键词数量</label>
                                <input type="number" id="KEYWORDS_SIZE" min="2" max="10">
                                <small>影响对一句话的主题词提取效果，建议为3</small>
                            </div>
                            <div class="form-field">
                                <label>跨群回复阈值</label>
                                <input type="number" id="cross_group_threshold" min="1" max="10">
                                <small>N个群均有相同的回复时，则作为全局回复</small>
                            </div>
                            <div class="form-field">
                                <label>最高学习次数</label>
                                <input type="number" id="learn_max_count" min="2" max="20">
                                <small>学习的回复最高能累计到的次数</small>
                            </div>
                        </div>
                        <div class="form-field">
                            <label>全局屏蔽词（用逗号分隔）</label>
                            <input type="text" id="ban_words" placeholder="屏蔽词1,屏蔽词2">
                            <small>含有这些词的消息不会学习和回复</small>
                        </div>
                        <div class="form-field">
                            <label>全局屏蔽用户（用逗号分隔QQ号）</label>
                            <input type="text" id="ban_users" placeholder="123456,789012">
                            <small>这些用户的消息不会学习和回复</small>
                        </div>
                        <div class="btn-group">
                            <button class="btn btn-primary" onclick="saveGlobalConfig()">保存全局配置</button>
                        </div>
                    </div>
                </div>
                
                <div class="config-section">
                    <h3>👥 分群配置</h3>
                    <div class="form-field">
                        <label>选择群聊</label>
                        <select id="groupSelect" onchange="loadGroupConfig()">
                            <option value="">-- 请选择群聊 --</option>
                            ${{groupList.map(g => `<option value="${{g.value}}">${{g.label}}</option>`).join('')}}
                        </select>
                    </div>
                    <div id="groupConfigForm" style="display: none;">
                        <div class="form-grid">
                            <div class="form-field">
                                <label>
                                    <input type="checkbox" id="group_enable"> 群聊学习开关
                                </label>
                                <small>针对该群的学习开关</small>
                            </div>
                            <div class="form-field">
                                <label>回复阈值</label>
                                <input type="number" id="answer_threshold" min="2" max="10">
                                <small>需要学习多少次才会回复</small>
                            </div>
                            <div class="form-field">
                                <label>复读阈值</label>
                                <input type="number" id="repeat_threshold" min="2" max="10">
                                <small>多少人复读后跟着复读</small>
                            </div>
                            <div class="form-field">
                                <label>打断复读概率 (%)</label>
                                <input type="number" id="break_probability" min="0" max="100">
                                <small>达到复读阈值时打断的概率</small>
                            </div>
                            <div class="form-field">
                                <label>
                                    <input type="checkbox" id="speak_enable"> 主动发言开关
                                </label>
                                <small>是否允许主动发言</small>
                            </div>
                            <div class="form-field">
                                <label>主动发言阈值</label>
                                <input type="number" id="speak_threshold" min="0" max="20">
                                <small>值越低，主动发言越频繁</small>
                            </div>
                            <div class="form-field">
                                <label>主动发言最小间隔（秒）</label>
                                <input type="number" id="speak_min_interval" min="0" max="3600">
                                <small>两次主动发言的最小间隔</small>
                            </div>
                            <div class="form-field">
                                <label>连续主动发言概率 (%)</label>
                                <input type="number" id="speak_continuously_probability" min="0" max="100">
                                <small>触发主动发言时连续发言的概率</small>
                            </div>
                            <div class="form-field">
                                <label>最大连续主动发言句数</label>
                                <input type="number" id="speak_continuously_max_len" min="1" max="10">
                                <small>连续主动发言的最大句数</small>
                            </div>
                            <div class="form-field">
                                <label>主动发言附带戳一戳概率 (%)</label>
                                <input type="number" id="speak_poke_probability" min="0" max="100">
                                <small>主动发言时戳人的概率</small>
                            </div>
                        </div>
                        <div class="form-field">
                            <label>屏蔽词（用逗号分隔）</label>
                            <input type="text" id="group_ban_words" placeholder="屏蔽词1,屏蔽词2">
                        </div>
                        <div class="form-field">
                            <label>屏蔽用户（用逗号分隔QQ号）</label>
                            <input type="text" id="group_ban_users" placeholder="123456,789012">
                        </div>
                        <div class="btn-group">
                            <button class="btn btn-primary" onclick="saveGroupConfig()">保存群配置</button>
                            <button class="btn btn-success" onclick="saveGroupConfigToAll()">保存至所有群</button>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('config').innerHTML = html;
            
            // 加载全局配置
            loadGlobalConfigData();
        }}
        
        async function loadGlobalConfigData() {{
            const data = await apiCall('/chat_global_config');
            if (!data) return;
            
            document.getElementById('total_enable').checked = data.total_enable || false;
            document.getElementById('KEYWORDS_SIZE').value = data.KEYWORDS_SIZE || 3;
            document.getElementById('cross_group_threshold').value = data.cross_group_threshold || 3;
            document.getElementById('learn_max_count').value = data.learn_max_count || 6;
            document.getElementById('ban_words').value = (data.ban_words || []).join(',');
            document.getElementById('ban_users').value = (data.ban_users || []).join(',');
        }}
        
        async function saveGlobalConfig() {{
            const config = {{
                total_enable: document.getElementById('total_enable').checked,
                KEYWORDS_SIZE: parseInt(document.getElementById('KEYWORDS_SIZE').value),
                cross_group_threshold: parseInt(document.getElementById('cross_group_threshold').value),
                learn_max_count: parseInt(document.getElementById('learn_max_count').value),
                ban_words: document.getElementById('ban_words').value.split(',').filter(w => w.trim()).map(w => w.trim()),
                ban_users: document.getElementById('ban_users').value.split(',').filter(u => u.trim()).map(u => parseInt(u.trim()))
            }};
            
            const result = await apiCall('/chat_global_config', {{
                method: 'POST',
                body: JSON.stringify(config)
            }});
            
            if (result && result.status === 0) {{
                const msg = document.getElementById('successMsg');
                msg.style.display = 'block';
                setTimeout(() => msg.style.display = 'none', 3000);
            }}
        }}
        
        async function loadGroupConfig() {{
            const groupId = document.getElementById('groupSelect').value;
            if (!groupId) {{
                document.getElementById('groupConfigForm').style.display = 'none';
                return;
            }}
            
            const data = await apiCall(`/chat_group_config?group_id=${{groupId}}`);
            if (!data) return;
            
            document.getElementById('groupConfigForm').style.display = 'block';
            document.getElementById('group_enable').checked = data.enable || false;
            document.getElementById('answer_threshold').value = data.answer_threshold || 4;
            document.getElementById('repeat_threshold').value = data.repeat_threshold || 3;
            document.getElementById('break_probability').value = data.break_probability || 25;
            document.getElementById('speak_enable').checked = data.speak_enable || false;
            document.getElementById('speak_threshold').value = data.speak_threshold || 5;
            document.getElementById('speak_min_interval').value = data.speak_min_interval || 300;
            document.getElementById('speak_continuously_probability').value = data.speak_continuously_probability || 50;
            document.getElementById('speak_continuously_max_len').value = data.speak_continuously_max_len || 3;
            document.getElementById('speak_poke_probability').value = data.speak_poke_probability || 50;
            document.getElementById('group_ban_words').value = (data.ban_words || []).join(',');
            document.getElementById('group_ban_users').value = (data.ban_users || []).join(',');
        }}
        
        async function saveGroupConfig() {{
            const groupId = document.getElementById('groupSelect').value;
            if (!groupId) return;
            
            const config = {{
                enable: document.getElementById('group_enable').checked,
                answer_threshold: parseInt(document.getElementById('answer_threshold').value),
                repeat_threshold: parseInt(document.getElementById('repeat_threshold').value),
                break_probability: parseFloat(document.getElementById('break_probability').value),
                speak_enable: document.getElementById('speak_enable').checked,
                speak_threshold: parseInt(document.getElementById('speak_threshold').value),
                speak_min_interval: parseInt(document.getElementById('speak_min_interval').value),
                speak_continuously_probability: parseFloat(document.getElementById('speak_continuously_probability').value),
                speak_continuously_max_len: parseInt(document.getElementById('speak_continuously_max_len').value),
                speak_poke_probability: parseFloat(document.getElementById('speak_poke_probability').value),
                ban_words: document.getElementById('group_ban_words').value.split(',').filter(w => w.trim()).map(w => w.trim()),
                ban_users: document.getElementById('group_ban_users').value.split(',').filter(u => u.trim()).map(u => parseInt(u.trim())),
                answer_threshold_weights: [10, 30, 60]  // 默认权重
            }};
            
            const result = await apiCall(`/chat_group_config?group_id=${{groupId}}`, {{
                method: 'POST',
                body: JSON.stringify(config)
            }});
            
            if (result && result.status === 0) {{
                const msg = document.getElementById('successMsg');
                msg.style.display = 'block';
                setTimeout(() => msg.style.display = 'none', 3000);
            }}
        }}
        
        async function saveGroupConfigToAll() {{
            if (!confirm('确认将当前配置保存至所有群？这将覆盖所有群的现有配置！')) {{
                return;
            }}
            
            const groupId = document.getElementById('groupSelect').value;
            if (!groupId) {{
                alert('请先选择一个群！');
                return;
            }}
            
            const config = {{
                enable: document.getElementById('group_enable').checked,
                answer_threshold: parseInt(document.getElementById('answer_threshold').value),
                repeat_threshold: parseInt(document.getElementById('repeat_threshold').value),
                break_probability: parseFloat(document.getElementById('break_probability').value),
                speak_enable: document.getElementById('speak_enable').checked,
                speak_threshold: parseInt(document.getElementById('speak_threshold').value),
                speak_min_interval: parseInt(document.getElementById('speak_min_interval').value),
                speak_continuously_probability: parseFloat(document.getElementById('speak_continuously_probability').value),
                speak_continuously_max_len: parseInt(document.getElementById('speak_continuously_max_len').value),
                speak_poke_probability: parseFloat(document.getElementById('speak_poke_probability').value),
                ban_words: document.getElementById('group_ban_words').value.split(',').filter(w => w.trim()).map(w => w.trim()),
                ban_users: document.getElementById('group_ban_users').value.split(',').filter(u => u.trim()).map(u => parseInt(u.trim())),
                answer_threshold_weights: [10, 30, 60]  // 默认权重
            }};
            
            const result = await apiCall('/chat_group_config?group_id=all', {{
                method: 'POST',
                body: JSON.stringify(config)
            }});
            
            if (result && result.status === 0) {{
                const msg = document.getElementById('successMsg');
                msg.textContent = '已成功保存至所有群！';
                msg.style.display = 'block';
                setTimeout(() => {{
                    msg.textContent = '保存成功！';
                    msg.style.display = 'none';
                }}, 3000);
            }}
        }}
        
        // 初始加载
        loadStats();
        loadConfig();
    </script>
</body>
</html>
"""
