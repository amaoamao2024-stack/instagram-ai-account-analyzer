from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import urllib.error
import urllib.request


WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("请先设置 MAKE_WEBHOOK_URL 环境变量")


PAGE = """<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instagram AI Account Analyzer</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;max-width:720px;margin:48px auto;padding:0 20px;color:#172033}
.card{border:1px solid #dfe3ea;border-radius:14px;padding:24px;box-shadow:0 8px 30px #18233a12}
label{display:block;margin:16px 0 6px;font-weight:650}
input{width:100%;box-sizing:border-box;padding:12px;border:1px solid #bbc3d1;border-radius:8px;font-size:15px}
button{margin-top:20px;border:0;border-radius:9px;padding:12px 18px;background:#6c42e8;color:white;font-weight:700;cursor:pointer}
button:disabled{opacity:.55}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f7f9;padding:14px;border-radius:9px;min-height:42px}
.note{color:#5d6678;font-size:14px}
</style>
<div class="card">
<h2>Instagram AI Account Analyzer</h2>
<p class="note">Make 场景需处于 Active。密钥只用于本次请求，不会保存在页面中。</p>
<form id="f">
<label>Instagram 账户链接</label>
<input id="url" type="url" required placeholder="https://www.instagram.com/用户名/">
<label>Webhook API Key</label>
<input id="key" type="password" required autocomplete="off" placeholder="输入 Webhook API Key">
<button id="send">生成分析报告</button>
</form>
<h3>结果</h3><pre id="out">等待提交</pre>
</div>
<script>
f.onsubmit=async(e)=>{e.preventDefault();send.disabled=true;out.textContent='已提交，正在等待 Make 完成…';try{const r=await fetch('/run',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({instagram_input:url.value.trim(),api_key:key.value,report_language:'中文',post_limit:20})});const t=await r.text();out.textContent=t||('HTTP '+r.status)}catch(err){out.textContent='发送失败：'+err.message}finally{send.disabled=false;key.value=''}};
</script>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        body = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            api_key = payload.pop("api_key")
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            request = urllib.request.Request(
                WEBHOOK_URL,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "x-make-apikey": api_key,
                },
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                result = response.read()
                status = response.status
                content_type = response.headers.get(
                    "Content-Type", "application/json; charset=utf-8"
                )
        except urllib.error.HTTPError as exc:
            status = exc.code
            result = exc.read()
            content_type = exc.headers.get(
                "Content-Type", "text/plain; charset=utf-8"
            )
        except Exception as exc:
            status = 500
            result = ("本机转发失败：" + str(exc)).encode("utf-8")
            content_type = "text/plain; charset=utf-8"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(result)))
        self.end_headers()
        self.wfile.write(result)


HTTPServer(("127.0.0.1", 8769), Handler).serve_forever()
