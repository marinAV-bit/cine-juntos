const http = require('http');
const { WebSocketServer } = require('ws');
const srv = http.createServer((q, r) => { r.writeHead(200); r.end('Cine Juntos OK'); });
const wss = new WebSocketServer({ server: srv });
const rooms = new Map(); let n = 0;
const send = (ws, s) => { if (ws.readyState === 1) ws.send(s); };
function peers(code) {
  const r = rooms.get(code); if (!r) return;
  const s = JSON.stringify({ t: 'peers', list: [...r].map(([id, c]) => ({ id, pres: c.pres })) });
  r.forEach(c => send(c.ws, s));
}
wss.on('connection', ws => {
  const id = Math.random().toString(36).slice(2, 9) + (++n); let code = null; ws.alive = true;
  ws.on('pong', () => ws.alive = true);
  ws.on('message', raw => {
    let m; try { m = JSON.parse(raw); } catch { return; }
    if (m.t === 'join' && typeof m.room === 'string' && !code) {
      code = m.room.slice(0, 40);
      if (!rooms.has(code)) rooms.set(code, new Map());
      const r = rooms.get(code);
      if (r.size >= 6) { ws.close(); code = null; return; }
      r.set(id, { ws, pres: (m.pres && typeof m.pres === 'object') ? m.pres : {} });
      send(ws, JSON.stringify({ t: 'hello', id })); peers(code);
    } else if (!code) { return; }
    else if (m.t === 'emit') {
      const s = JSON.stringify({ t: 'msg', topic: String(m.topic).slice(0, 40), data: m.data, from: id });
      rooms.get(code).forEach(c => send(c.ws, s));
    } else if (m.t === 'pres') {
      const c = rooms.get(code).get(id);
      if (c && m.patch && typeof m.patch === 'object') { Object.assign(c.pres, m.patch); peers(code); }
    }
  });
  ws.on('close', () => {
    if (!code) return; const r = rooms.get(code); if (!r) return;
    r.delete(id); if (!r.size) rooms.delete(code); else peers(code);
  });
});
setInterval(() => wss.clients.forEach(ws => { if (!ws.alive) return ws.terminate(); ws.alive = false; ws.ping(); }), 25000);
srv.listen(process.env.PORT || 8080);
