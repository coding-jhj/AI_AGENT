<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Search Agent</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Noto+Sans+KR:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<style>
  :root {
    --bg: #f0f2ff;
    --sidebar: #ffffff;
    --main-bg: #f5f6ff;
    --border: #e2e5f5;
    --purple: #6c5ce7;
    --purple-light: #a29bfe;
    --blue: #0984e3;
    --cyan: #00cec9;
    --pink: #e84393;
    --orange: #fd7900;
    --green: #00b894;
    --text: #2d3250;
    --text-muted: #8690b5;
    --text-dim: #b2bad6;
    --mono: 'JetBrains Mono', monospace;
    --sans: 'Noto Sans KR', sans-serif;
    --display: 'Syne', sans-serif;
    --r: 14px;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    display: flex;
    height: 100dvh;
    overflow: hidden;
  }

  /* ── 사이드바 ── */
  #sidebar {
    width: 270px;
    min-width: 270px;
    background: var(--sidebar);
    border-right: 1.5px solid var(--border);
    display: flex;
    flex-direction: column;
    padding: 22px 18px;
    gap: 16px;
    box-shadow: 4px 0 24px rgba(108,92,231,0.06);
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 11px;
  }
  .logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 6px 20px rgba(108,92,231,0.35);
    flex-shrink: 0;
  }
  .logo-text {
    font-family: var(--display);
    font-size: 15px;
    font-weight: 800;
    letter-spacing: -0.4px;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .logo-sub { font-size: 11px; color: var(--text-muted); margin-top: 2px; font-family: var(--mono); }

  .divider { height: 1.5px; background: var(--border); border-radius: 2px; }

  .section-label {
    font-family: var(--mono);
    font-size: 9.5px;
    letter-spacing: 2px;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .key-guide {
    background: linear-gradient(135deg, #f8f6ff, #fff0fb);
    border: 1.5px solid #e8e2ff;
    border-radius: var(--r);
    padding: 12px 13px;
    font-size: 11.5px;
    line-height: 2;
    color: #7a80a0;
  }
  .key-guide a { color: var(--blue); text-decoration: none; font-weight: 500; }
  .key-guide a:hover { text-decoration: underline; }
  .step-num {
    display: inline-flex;
    width: 17px; height: 17px;
    border-radius: 5px;
    background: linear-gradient(135deg, var(--purple), var(--purple-light));
    color: #fff;
    font-family: var(--mono);
    font-size: 10px;
    align-items: center; justify-content: center;
    margin-right: 5px;
    font-weight: 500;
    flex-shrink: 0;
  }

  .input-wrap { position: relative; margin-top: 8px; }
  .input-wrap input {
    width: 100%;
    background: #f8f7ff;
    border: 1.5px solid #ddd9ff;
    border-radius: var(--r);
    color: var(--text);
    font-family: var(--mono);
    font-size: 12px;
    padding: 10px 36px 10px 13px;
    outline: none;
    transition: border-color .2s, box-shadow .2s;
  }
  .input-wrap input:focus {
    border-color: var(--purple);
    box-shadow: 0 0 0 3px rgba(108,92,231,0.12);
  }
  .input-wrap input::placeholder { color: var(--text-dim); }
  #key-status {
    position: absolute; right: 11px; top: 50%;
    transform: translateY(-50%);
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--text-dim);
    transition: background .3s, box-shadow .3s;
  }
  #key-status.ok  { background: var(--green); box-shadow: 0 0 8px rgba(0,184,148,0.5); }
  #key-status.err { background: #ff4757; }

  .model-select {
    width: 100%;
    background: #f8f7ff;
    border: 1.5px solid #ddd9ff;
    border-radius: var(--r);
    color: var(--text);
    font-family: var(--mono);
    font-size: 11.5px;
    padding: 9px 12px;
    outline: none;
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' fill='none'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%238690b5' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    transition: border-color .2s;
  }
  .model-select:focus { border-color: var(--purple); }

  .clear-btn {
    width: 100%;
    background: #fff5f5;
    border: 1.5px solid #ffd0d0;
    border-radius: var(--r);
    color: #e84393;
    font-family: var(--mono);
    font-size: 11.5px;
    padding: 9px;
    cursor: pointer;
    transition: all .2s;
    font-weight: 500;
  }
  .clear-btn:hover { background: #ffe0ee; border-color: var(--pink); }

  .stack-list { list-style: none; display: flex; flex-direction: column; gap: 7px; }
  .stack-list li {
    font-size: 12px; color: var(--text-muted);
    display: flex; align-items: center; gap: 8px;
  }
  .tag {
    font-family: var(--mono);
    font-size: 9.5px;
    padding: 2px 8px;
    border-radius: 5px;
    font-weight: 500;
    letter-spacing: 0.3px;
  }
  .tag-llm   { background: #edeaff; color: var(--purple); border: 1px solid #cfc9ff; }
  .tag-search{ background: #e0f5ff; color: var(--blue);   border: 1px solid #b2deff; }
  .tag-agent { background: #ffe0f3; color: var(--pink);   border: 1px solid #ffbbdf; }
  .tag-api   { background: #d8fff6; color: var(--cyan);   border: 1px solid #9feee8; }

  /* ── 메인 ── */
  #main { flex: 1; display: flex; flex-direction: column; min-width: 0; background: var(--main-bg); }

  #chat-header {
    padding: 15px 28px;
    border-bottom: 1.5px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #fff;
    box-shadow: 0 2px 12px rgba(108,92,231,0.06);
  }
  .header-left { display: flex; align-items: center; gap: 12px; }
  #chat-header h1 {
    font-family: var(--display);
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.3px;
  }
  #chat-header p { font-size: 11px; color: var(--text-muted); margin-top: 2px; font-family: var(--mono); }

  .status-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--text-dim);
    flex-shrink: 0;
    transition: all .3s;
  }
  .status-dot.active {
    background: var(--green);
    box-shadow: 0 0 10px rgba(0,184,148,0.6);
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }

  .news-btn {
    font-family: var(--mono);
    font-size: 11px;
    padding: 7px 16px;
    border-radius: 20px;
    border: 1.5px solid var(--purple);
    background: linear-gradient(135deg, #f0edff, #fce8f8);
    color: var(--purple);
    cursor: pointer;
    transition: all .2s;
    font-weight: 500;
  }
  .news-btn:hover {
    background: linear-gradient(135deg, var(--purple), var(--pink));
    color: #fff;
    border-color: transparent;
    box-shadow: 0 4px 16px rgba(108,92,231,0.3);
    transform: translateY(-1px);
  }

  #messages {
    flex: 1;
    overflow-y: auto;
    padding: 28px 32px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    scroll-behavior: smooth;
  }
  #messages::-webkit-scrollbar { width: 4px; }
  #messages::-webkit-scrollbar-track { background: transparent; }
  #messages::-webkit-scrollbar-thumb { background: #d0d4f0; border-radius: 2px; }

  /* 빈 화면 */
  #empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    padding: 40px 0;
  }
  .empty-orb {
    width: 80px; height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    display: flex; align-items: center; justify-content: center;
    font-size: 36px;
    animation: float 3.5s ease-in-out infinite;
    box-shadow: 0 12px 40px rgba(108,92,231,0.3), 0 4px 16px rgba(232,67,147,0.2);
  }
  @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
  .empty-title {
    font-family: var(--display);
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
  }
  .empty-sub { font-size: 13px; color: var(--text-muted); }

  .quick-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    max-width: 460px;
    width: 100%;
    margin-top: 4px;
  }
  .quick-btn {
    background: #fff;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    color: var(--text-muted);
    font-family: var(--sans);
    font-size: 12px;
    padding: 12px 14px;
    cursor: pointer;
    text-align: left;
    transition: all .2s;
    line-height: 1.4;
    box-shadow: 0 2px 8px rgba(108,92,231,0.05);
  }
  .quick-btn:hover {
    border-color: var(--purple-light);
    color: var(--purple);
    background: #f6f3ff;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108,92,231,0.12);
  }

  /* 메시지 버블 */
  .msg { display: flex; gap: 11px; animation: fadeUp .22s ease; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:none} }
  .msg.user { flex-direction: row-reverse; }

  .avatar {
    width: 32px; height: 32px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0;
  }
  .msg.user .avatar {
    background: linear-gradient(135deg, #e0f0ff, #dce8ff);
    border: 1.5px solid #c0d5ff;
  }
  .msg.ai .avatar {
    background: linear-gradient(135deg, #ede8ff, #fce8f8);
    border: 1.5px solid #cfc9ff;
    box-shadow: 0 4px 12px rgba(108,92,231,0.15);
  }

  .bubble {
    max-width: 70%;
    background: #fff;
    border: 1.5px solid var(--border);
    border-radius: 4px 16px 16px 16px;
    padding: 12px 16px;
    font-size: 13.5px;
    line-height: 1.75;
    color: var(--text);
    box-shadow: 0 2px 12px rgba(108,92,231,0.06);
  }
  .msg.user .bubble {
    background: linear-gradient(135deg, #ede8ff, #f8e8ff);
    border-color: #cfc9ff;
    border-radius: 16px 4px 16px 16px;
    color: #4a3da8;
    box-shadow: 0 2px 12px rgba(108,92,231,0.1);
  }

  .search-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: linear-gradient(135deg, #e0f8ff, #e8f4ff);
    color: var(--blue);
    border: 1.5px solid #b2deff;
    font-family: var(--mono);
    font-size: 10.5px;
    padding: 3px 11px;
    border-radius: 20px;
    margin-bottom: 9px;
    font-weight: 500;
  }
  .search-badge::before { content: '⌕  '; }

  .bubble.error {
    background: #fff5f7;
    border-color: #ffd0dc;
    color: #c0284a;
  }

  /* 타이핑 */
  .typing .bubble { display: flex; align-items: center; gap: 6px; padding: 16px 18px; background: #fff; }
  .dot { width: 7px; height: 7px; border-radius: 50%; animation: blink 1.2s infinite; }
  .dot:nth-child(1) { background: var(--purple); }
  .dot:nth-child(2) { background: var(--pink); animation-delay: .2s; }
  .dot:nth-child(3) { background: var(--cyan); animation-delay: .4s; }
  @keyframes blink { 0%,80%,100%{opacity:.25;transform:scale(0.9)} 40%{opacity:1;transform:scale(1.2)} }

  /* 입력창 */
  #input-area {
    padding: 14px 28px 18px;
    border-top: 1.5px solid var(--border);
    background: #fff;
    box-shadow: 0 -4px 20px rgba(108,92,231,0.06);
  }
  #input-row {
    display: flex; gap: 10px; align-items: flex-end;
    background: #f8f7ff;
    border: 1.5px solid #ddd9ff;
    border-radius: 16px;
    padding: 10px 12px;
    transition: border-color .2s, box-shadow .2s;
  }
  #input-row:focus-within {
    border-color: var(--purple);
    box-shadow: 0 0 0 3px rgba(108,92,231,0.1), 0 4px 20px rgba(108,92,231,0.08);
  }
  #user-input {
    flex: 1; background: transparent; border: none; outline: none;
    color: var(--text); font-family: var(--sans); font-size: 13.5px;
    resize: none; max-height: 120px; line-height: 1.5; padding: 2px 0;
  }
  #user-input::placeholder { color: var(--text-dim); }
  #send-btn {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--purple), var(--pink));
    border: none; border-radius: 10px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; color: #fff;
    transition: opacity .2s, transform .1s, box-shadow .2s;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(108,92,231,0.35);
  }
  #send-btn:hover  { opacity:.88; box-shadow: 0 6px 24px rgba(108,92,231,0.5); }
  #send-btn:active { transform: scale(.93); }
  #send-btn:disabled { opacity: .3; cursor: not-allowed; box-shadow: none; }

  .hint {
    font-size: 10.5px; color: var(--text-dim);
    margin-top: 8px; text-align: center; font-family: var(--mono);
  }
  .hint em { color: var(--purple-light); font-style: normal; }

  @media (max-width: 640px) {
    #sidebar { display: none; }
    #messages { padding: 20px 16px; }
    #input-area { padding: 12px 16px 16px; }
  }
</style>
</head>
<body>

<!-- ── 사이드바 ── -->
<aside id="sidebar">
  <div class="logo">
    <div class="logo-icon">🤖</div>
    <div>
      <div class="logo-text">AI Search Agent</div>
      <div class="logo-sub">ReAct · Groq + DDG</div>
    </div>
  </div>

  <div class="divider"></div>

  <div>
    <div class="section-label">Google AI Studio API Key</div>
    <div class="key-guide">
      <span class="step-num">1</span> <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a> 접속<br>
      <span class="step-num">2</span> 구글 계정으로 무료 로그인<br>
      <span class="step-num">3</span> Get API Key → Create API Key<br>
      <span class="step-num">4</span> 아래에 붙여넣기
    </div>
    <div class="input-wrap">
      <input type="password" id="api-key" placeholder="AIza..." autocomplete="off" />
      <div id="key-status"></div>
    </div>
  </div>

  <div class="divider"></div>

  <div>
    <div class="section-label">모델 선택</div>
    <select id="model-select" class="model-select">
      <option value="gemini-2.0-flash">⚡ Gemini 2.0 Flash</option>
      <option value="llama-3.3-70b-versatile">🧠 Llama 3.3 70B</option>
    </select>
  </div>

  <div class="divider"></div>

  <button class="clear-btn" onclick="clearChat()">🗑 대화 초기화</button>

  <div class="divider"></div>

  <div>
    <div class="section-label">Tech Stack</div>
    <ul class="stack-list">
      <li><span class="tag tag-llm">LLM</span> Llama 3.3 70B (Groq)</li>
      <li><span class="tag tag-search">검색</span> DuckDuckGo</li>
      <li><span class="tag tag-agent">Agent</span> LangChain ReAct</li>
      <li><span class="tag tag-api">API</span> FastAPI</li>
    </ul>
  </div>
</aside>

<!-- ── 메인 ── -->
<div id="main">
  <div id="chat-header">
    <div class="header-left">
      <div class="status-dot" id="status-dot"></div>
      <div>
        <h1>AI Search Agent</h1>
        <p>스스로 검색하고 판단하는 ReAct Agent</p>
      </div>
    </div>
    <button class="news-btn" onclick="sendQuickText('오늘 AI 뉴스 알려줘')">오늘 AI 뉴스 알려줘</button>
  </div>

  <div id="messages">
    <div id="empty-state">
      <div class="empty-orb">🔍</div>
      <div class="empty-title">무엇이든 검색해드릴게요</div>
      <div class="empty-sub">API 키를 입력하면 대화를 시작할 수 있어요</div>
      <div class="quick-grid">
        <button class="quick-btn" onclick="sendQuickText(this.textContent)">RAG가 뭐야?</button>
        <button class="quick-btn" onclick="sendQuickText(this.textContent)">LangGraph vs LangChain</button>
        <button class="quick-btn" onclick="sendQuickText(this.textContent)">파이썬 최신 버전은?</button>
        <button class="quick-btn" onclick="sendQuickText(this.textContent)">오늘 AI 뉴스 알려줘</button>
      </div>
    </div>
  </div>

  <div id="input-area">
    <div id="input-row">
      <textarea id="user-input" placeholder="무엇이든 물어보세요..." rows="1"></textarea>
      <button id="send-btn" onclick="sendMessage()" disabled>➤</button>
    </div>
    <div class="hint">Enter로 전송 · Shift+Enter 줄바꿈 · <em>FastAPI /chat</em> 엔드포인트 사용 중</div>
  </div>
</div>

<script>
  const API_BASE = window.location.origin;
  let history = [];
  let isLoading = false;

  const keyInput  = document.getElementById('api-key');
  const keyStatus = document.getElementById('key-status');
  const statusDot = document.getElementById('status-dot');
  const sendBtn   = document.getElementById('send-btn');

  keyInput.addEventListener('change', () => { localStorage.setItem('google_api_key', keyInput.value.trim()); });
  document.getElementById('model-select').addEventListener('change', () => {
    localStorage.setItem('google_model', document.getElementById('model-select').value);
  });
  const savedKey = localStorage.getItem('google_api_key');
  if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
  const savedModel = localStorage.getItem('google_model');
  if (savedModel) { document.getElementById('model-select').value = savedModel; }

  function updateKeyStatus() {
    const val = keyInput.value.trim();
    if (val.startsWith('AIza') && val.length > 20) {
      keyStatus.className = 'ok';
      statusDot.className = 'status-dot active';
      sendBtn.disabled = false;
    } else {
      keyStatus.className = val ? 'err' : '';
      statusDot.className = 'status-dot';
      sendBtn.disabled = true;
    }
  }
  keyInput.addEventListener('input', updateKeyStatus);

  const messagesEl = document.getElementById('messages');
  const emptyStateRef = document.getElementById('empty-state');

  function appendMessage(role, content, searched = false, searchQuery = null, isError = false) {
    const es = document.getElementById('empty-state');
    if (es) es.remove();

    const wrap = document.createElement('div');
    wrap.className = `msg ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const bubble = document.createElement('div');
    bubble.className = 'bubble' + (isError ? ' error' : '');

    if (searched && searchQuery) {
      const badge = document.createElement('div');
      badge.className = 'search-badge';
      badge.textContent = searchQuery;
      bubble.appendChild(badge);
      bubble.appendChild(document.createElement('br'));
    }

    const text = document.createElement('span');
    text.textContent = content;
    bubble.appendChild(text);

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return wrap;
  }

  function showTyping() {
    const wrap = document.createElement('div');
    wrap.className = 'msg ai typing';
    wrap.id = 'typing-indicator';
    wrap.innerHTML = `<div class="avatar">🤖</div><div class="bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function removeTyping() { document.getElementById('typing-indicator')?.remove(); }

  async function sendMessage(text) {
    const apiKey = keyInput.value.trim();
    const input  = (text || document.getElementById('user-input').value).trim();
    if (!input || !apiKey || isLoading) return;

    document.getElementById('user-input').value = '';
    document.getElementById('user-input').style.height = 'auto';
    isLoading = true;
    sendBtn.disabled = true;

    appendMessage('user', input);
    history.push({ role: 'user', content: input });
    showTyping();

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: apiKey,
          user_input: input,
          history: history.slice(0, -1),
          model: document.getElementById('model-select').value
        }),
      });
      removeTyping();

      if (!res.ok) {
        const err = await res.json();
        appendMessage('ai', `오류: ${err.detail || '알 수 없는 오류'}`, false, null, true);
        history.pop(); return;
      }

      const data = await res.json();
      appendMessage('ai', data.answer, data.searched, data.search_query);
      history.push({ role: 'assistant', content: data.answer });
    } catch (e) {
      removeTyping();
      appendMessage('ai', `서버 연결 오류: ${e.message}`, false, null, true);
      history.pop();
    } finally {
      isLoading = false;
      updateKeyStatus();
    }
  }

  function sendQuickText(text) { sendMessage(text.trim()); }

  function clearChat() {
    history = [];
    messagesEl.innerHTML = '';
    const clone = emptyStateRef.cloneNode(true);
    messagesEl.appendChild(clone);
    clone.querySelectorAll('.quick-btn').forEach(b => {
      b.onclick = () => sendQuickText(b.textContent);
    });
  }

  document.getElementById('user-input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });
  document.getElementById('user-input').addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
  });
</script>
</body>
</html>