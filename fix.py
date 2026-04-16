with open("static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

old = """
  const savedKey = localStorage.getItem('groq_api_key');
  if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
  const savedModel = localStorage.getItem('groq_model');
  if (savedModel) { document.getElementById('model-select').value = savedModel; }
  keyInput.addEventListener('change', () => { localStorage.setItem('groq_api_key', keyInput.value.trim()); });
  document.getElementById('model-select').addEventListener('change', () => {
    localStorage.setItem('groq_model', document.getElementById('model-select').value);
  });
"""
html = html.replace(old, "", 1)

new_storage = """
  keyInput.addEventListener('change', () => { localStorage.setItem('groq_api_key', keyInput.value.trim()); });
  document.getElementById('model-select').addEventListener('change', () => {
    localStorage.setItem('groq_model', document.getElementById('model-select').value);
  });
  const savedKey = localStorage.getItem('groq_api_key');
  if (savedKey) { keyInput.value = savedKey; keyInput.dispatchEvent(new Event('input')); }
  const savedModel = localStorage.getItem('groq_model');
  if (savedModel) { document.getElementById('model-select').value = savedModel; }
"""
html = html.replace("  keyInput.addEventListener('input', () => {", new_storage + "\n  keyInput.addEventListener('input', () => {", 1)

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("완료!")