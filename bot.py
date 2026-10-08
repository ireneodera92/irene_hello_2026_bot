import time, requests, yfinance as yf, pandas as pd, websocket, json, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})
def rsi(pr):
    d=pd.Series(pr).diff()
    g=d.where(d>0,0).rolling(14).mean()
    l=-d.where(d<0,0).rolling(14).mean()
    return (100-(100/(1+g/l))).iloc[-1]
def check_forex():
    try:
        data=yf.download("EURUSD=X", period="1d", interval="5m", progress=False)
        p=data['Close'].tolist(); r=rsi(p)
        if r<30: send(f"📈 FOREX BUY EUR/USD RSI {r:.1f}")
        elif r>70: send(f"📉 FOREX SELL EUR/USD RSI {r:.1f}")
    except: pass
def check_vol():
    try:
        ws=websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089")
        ws.send(json.dumps({"ticks_history":"R_75","count":50,"end":"latest","style":"candles","granularity":300}))
        c=json.loads(ws.recv())['candles']; ws.close()
        p=[x['close'] for x in c]; r=rsi(p)
        if r<30: send(f"📈 VOL BUY V75 RSI {r:.1f} {p[-1]:.2f}")
        elif r>70: send(f"📉 VOL SELL V75 RSI {r:.1f} {p[-1]:.2f}")
    except: pass
send("✅ Bot ONLINE V75+EUR/USD 5min RSI")
while True:
    check_forex(); time.sleep(5); check_vol(); time.sleep(300)
