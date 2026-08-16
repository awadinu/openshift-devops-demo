from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import date

app = FastAPI()
VERSION = "2.0.0"

# In-memory storage (see note at bottom — resets on redeploy, by design for now)
runs = []
next_id = 1

class Run(BaseModel):
    distance_km: float
    duration_min: float

def pace(distance_km, duration_min):
    if distance_km <= 0:
        return "-"
    p = duration_min / distance_km
    return f"{int(p)}:{int((p % 1) * 60):02d} /km"

@app.post("/api/runs")
def add_run(run: Run):
    global next_id
    entry = {
        "id": next_id,
        "date": str(date.today()),
        "distance_km": run.distance_km,
        "duration_min": run.duration_min,
        "pace": pace(run.distance_km, run.duration_min),
    }
    next_id += 1
    runs.append(entry)
    return entry

@app.delete("/api/runs/{run_id}")
def delete_run(run_id: int):
    global runs
    runs = [r for r in runs if r["id"] != run_id]
    return {"deleted": run_id}

@app.get("/api/stats")
def stats():
    total_km = sum(r["distance_km"] for r in runs)
    total_min = sum(r["duration_min"] for r in runs)
    return {
        "count": len(runs),
        "total_km": round(total_km, 2),
        "total_min": round(total_min, 1),
        "avg_pace": pace(total_km, total_min) if total_km else "-",
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root():
    return """<!DOCTYPE html>
<html>
<head>
<title>Run Tracker</title>
<style>
  body { font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; display: flex; justify-content: center; padding: 40px 16px; }
  .app { background: white; border-radius: 16px; padding: 32px; width: 480px; box-shadow: 0 4px 24px rgba(0,0,0,0.1); }
  h1 { margin: 0 0 4px; color: #2b6cb0; }
  .sub { color: #718096; font-size: 13px; margin-bottom: 24px; }
  .stats { display: flex; gap: 12px; margin-bottom: 24px; }
  .stat { flex: 1; background: #ebf4ff; border-radius: 10px; padding: 12px; text-align: center; }
  .stat b { display: block; font-size: 20px; color: #2b6cb0; }
  .stat span { font-size: 11px; color: #4a5568; }
  form { display: flex; gap: 8px; margin-bottom: 20px; }
  input { flex: 1; padding: 10px; border: 1px solid #cbd5e0; border-radius: 8px; font-size: 14px; }
  button { padding: 10px 18px; background: #2b6cb0; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
  button:hover { background: #2c5282; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th { text-align: left; color: #718096; font-size: 11px; text-transform: uppercase; padding: 6px 4px; border-bottom: 2px solid #e2e8f0; }
  td { padding: 8px 4px; border-bottom: 1px solid #edf2f7; }
  .del { color: #c53030; cursor: pointer; background: none; padding: 0; font-size: 14px; }
  .empty { color: #a0aec0; text-align: center; padding: 20px; }
</style>
</head>
<body>
<div class="app">
  <h1>🏃 Run Tracker</h1>
  <div class="sub">v""" + VERSION + """ — deployed from GitHub to OpenShift</div>
  <div class="stats">
    <div class="stat"><b id="s-count">0</b><span>runs</span></div>
    <div class="stat"><b id="s-km">0</b><span>total km</span></div>
    <div class="stat"><b id="s-pace">-</b><span>avg pace</span></div>
  </div>
  <form onsubmit="addRun(event)">
    <input id="dist" type="number" step="0.01" min="0.1" placeholder="Distance (km)" required>
    <input id="dur" type="number" step="0.1" min="1" placeholder="Time (min)" required>
    <button type="submit">Log</button>
  </form>
  <table>
    <tr><th>Date</th><th>Km</th><th>Min</th><th>Pace</th><th></th></tr>
    <tbody id="rows"></tbody>
  </table>
  <div class="empty" id="empty">No runs yet — go for one! 🏃</div>
</div>
<script>
async function refresh() {
  const runs = await (await fetch('/api/runs-list')).json();
  const stats = await (await fetch('/api/stats')).json();
  document.getElementById('s-count').textContent = stats.count;
  document.getElementById('s-km').textContent = stats.total_km;
  document.getElementById('s-pace').textContent = stats.avg_pace;
  const tbody = document.getElementById('rows');
  tbody.innerHTML = '';
  document.getElementById('empty').style.display = runs.length ? 'none' : 'block';
  runs.slice().reverse().forEach(r => {
    tbody.innerHTML += `<tr><td>${r.date}</td><td>${r.distance_km}</td><td>${r.duration_min}</td><td>${r.pace}</td><td><button class="del" onclick="del(${r.id})">✕</button></td></tr>`;
  });
}
async function addRun(e) {
  e.preventDefault();
  await fetch('/api/runs', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({distance_km: parseFloat(document.getElementById('dist').value), duration_min: parseFloat(document.getElementById('dur').value)})
  });
  document.getElementById('dist').value = '';
  document.getElementById('dur').value = '';
  refresh();
}
async function del(id) {
  await fetch('/api/runs/' + id, {method: 'DELETE'});
  refresh();
}
refresh();
</script>
</body>
</html>"""

@app.get("/api/runs-list")
def list_runs():
    return runs
