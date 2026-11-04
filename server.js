const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const PORT = 8899;

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.method === 'GET' && (req.url === '/' || req.url === '/index.html')) {
        const htmlPath = path.join(__dirname, 'lab.html');
        fs.readFile(htmlPath, 'utf8', (err, html) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Error loading lab.html');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(html);
        });
        return;
    }

    if (req.method === 'POST' && req.url === '/api/attack') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
            try {
                const { side, type, payload } = JSON.parse(body);
                executeAttack(side, type, payload, (result) => {
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(result));
                });
            } catch (err) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ERROR', output: err.message }));
            }
        });
        return;
    }

    res.writeHead(404);
    res.end('Not Found');
});

function executeAttack(side, atkType, payload, callback) {
    let pythonCode = '';
    const safePayload = payload.replace(/'/g, "\\'");

    if (side === 'unprotected') {
        pythonCode = `
import sqlite3, subprocess, sys

atk_type = '${atkType}'
payload = '${safePayload}'

if atk_type == 'sqli':
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INT, username TEXT, balance INT)')
    c.execute('INSERT INTO users VALUES (1, "ceo_harshit", 5000000)')
    c.execute('INSERT INTO users VALUES (2, "secret_vip", 9900000)')
    query = f"SELECT username, balance FROM users WHERE username = '{payload}'"
    print(f"Executed Query: {query}")
    c.execute(query)
    rows = c.fetchall()
    print(f"\\n💥 DATABASE DUMPED! Stolen Bank Accounts:\\n{rows}\\n\\n[CRITICAL]: Attacker successfully bypassed authentication!")

elif atk_type == 'rce':
    cmd = 'cmd.exe /c echo Processing report & whoami'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True)
    out, _ = proc.communicate()
    print(f"Executed Shell: {cmd}\\n\\n💥 SHELL EXECUTED! Server System User:\\n{out.strip()}\\n\\n[CRITICAL]: Attacker achieved Remote Code Execution (RCE)!")

elif atk_type == 'path':
    print(f"Attempted File Open: {payload}")
    print("\\n💥 PATH TRAVERSAL BREACHED!\\nNo sandbox barrier detected. Local system files exposed to attacker!")

elif atk_type == 'secret':
    print(f"Application Stderr/Stdout Stream:\\nPayment gateway initialized with Stripe Secret: {payload}")
    print("\\n💥 SECRET LEAKED!\\nLive private API token exposed in plaintext server logs!")
`;
    } else {
        pythonCode = `
import zeroarmor
from zeroarmor import ShieldBlockedException
import sqlite3, subprocess, sys

atk_type = '${atkType}'
payload = '${safePayload}'

try:
    if atk_type == 'sqli':
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        c.execute('CREATE TABLE users (id INT, username TEXT, balance INT)')
        c.execute('INSERT INTO users VALUES (1, "ceo_harshit", 5000000)')
        c.execute('INSERT INTO users VALUES (2, "secret_vip", 9900000)')
        query = f"SELECT username, balance FROM users WHERE username = '{payload}'"
        c.execute(query)
        print("Query executed.")

    elif atk_type == 'rce':
        cmd = 'cmd.exe /c echo Processing ; rm -rf /'
        subprocess.Popen(cmd, shell=True)
        print("Command executed.")

    elif atk_type == 'path':
        with open(payload, 'r') as f:
            pass
        print("File opened.")

    elif atk_type == 'secret':
        print(f"Payment gateway initialized with Stripe Secret: {payload}")

except ShieldBlockedException as e:
    print(f"🛡️ [ZEROARMOR INTERCEPTED & NEUTRALIZED THE ATTACK!]\\n"
          f"    |-- Triggered Shield: {e.rule_name}\\n"
          f"    |-- Defense Reason: {e.details}\\n"
          f"    |-- Intercepted Payload: {e.payload[:80]}\\n"
          f"    \\\\-- Status: Aborted safely at runtime. 0 Data Leaked!")
`;
    }

    const py = spawn('python', ['-u'], {
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });
    let stdout = '';
    let stderr = '';

    py.stdout.on('data', data => { stdout += data.toString(); });
    py.stderr.on('data', data => { stderr += data.toString(); });

    py.on('close', code => {
        const out = stdout || stderr || '';
        const isHacked = side === 'unprotected';
        callback({
            status: isHacked ? 'HACKED' : 'SAFE',
            output: out.trim()
        });
    });

    py.stdin.write(pythonCode);
    py.stdin.end();
}

server.listen(PORT, '0.0.0.0', () => {
    console.log(`[ZeroArmor] Server listening at http://127.0.0.1:${PORT}`);
});
