const API_URL = 'https://willis-lycanthropic-harry.ngrok-free.dev/analyze';
const HEALTH_URL = 'https://willis-lycanthropic-harry.ngrok-free.dev/health';

document.getElementById('analyze').addEventListener('click', async () => {
  const clause = document.getElementById('clause').value;
  if (!clause) return;
  
  document.getElementById('result').innerHTML = '⏳ Analyzing...';
  
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      headers: {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true'
      },
      body: JSON.stringify({ text: clause })
    });
    
    const data = await response.json();
    const riskClass = data.risk.toLowerCase();
    
    document.getElementById('result').innerHTML = `
      <div class="${riskClass}"><strong>Risk: ${data.risk}</strong></div>
      <div>Verdict: ${data.label}</div>
      <div>Confidence: ${Math.round(data.confidence * 100)}%</div>
    `;
  } catch (error) {
    document.getElementById('result').innerHTML = `❌ Error: ${error.message}`;
    console.error('Fetch error:', error);
  }
});