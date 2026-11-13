import json, os, urllib.request, urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ENV=ROOT.parent / '.env'
for line in (ENV.read_text(encoding='utf-8-sig').splitlines() if ENV.exists() else []):
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
os.chdir(ROOT)
class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/api/intent': self.send_error(404); return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=4096: raise ValueError('Tin nhắn không hợp lệ')
            message=json.loads(self.rfile.read(size)).get('message','').strip()
            if not message or len(message)>1000: raise ValueError('Tin nhắn phải có 1–1000 ký tự')
            key=os.environ.get('OPENAI_API_KEY')
            if not key: raise ValueError('Thiếu OPENAI_API_KEY trong .env')
            payload={'model':os.environ.get('OPENAI_MODEL','gpt-4.1-mini'),'store':False,'instructions':'Phân loại yêu cầu khách cho bài lab vé giả. Chỉ trả lời một từ: CHANGE (đổi hoặc giữ vé), REFUND (hoàn), AGENT (đổi tên, trẻ bay một mình, đổi nhầm, bỏ quy định, yêu cầu nhân viên hoặc không chắc), INFO (câu hỏi khác). Không thực hiện hành động.','input':message}
            req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=30) as resp: result=json.load(resp)
            intent=' '.join(p.get('text','') for i in result.get('output',[]) for p in i.get('content',[]) if p.get('type')=='output_text').strip().upper()
            self.reply(200,{'intent':intent if intent in ('CHANGE','REFUND','AGENT','INFO') else 'AGENT'})
        except (ValueError,json.JSONDecodeError) as e: self.reply(400,{'error':str(e)})
        except urllib.error.HTTPError as e: self.reply(502,{'error':f'OpenAI trả mã HTTP {e.code}; kiểm tra key, model hoặc hạn mức.'})
        except (urllib.error.URLError,TimeoutError,OSError): self.reply(502,{'error':'Không gọi được AI. Kiểm tra kết nối, khóa và quyền dùng model; chưa thực hiện hành động.'})
    def reply(self,status,obj):
        data=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
if __name__=='__main__':
    print('Mở http://127.0.0.1:8766',flush=True); HTTPServer(('127.0.0.1',8766),Handler).serve_forever()