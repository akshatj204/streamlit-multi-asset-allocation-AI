import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import requests
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Nifty 500 Signal Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0e1a; color: #e0e6f0; }
h1,h2,h3 { font-family: 'Space Mono', monospace; }
.metric-card {
    background: linear-gradient(135deg,#111827 0%,#1a2235 100%);
    border:1px solid #1e3a5f; border-radius:12px; padding:16px 20px; margin:6px 0;
}
.val-card {
    background: linear-gradient(135deg,#0f1a2e 0%,#162035 100%);
    border:1px solid #1e3a5f; border-radius:10px;
    padding:12px 16px; margin:4px 0; text-align:center;
}
.alloc-bucket {
    background: linear-gradient(135deg,#0d1929 0%,#111f35 100%);
    border:1px solid #1e3a5f; border-radius:12px; padding:18px; margin:8px 0;
}
.val-label  { font-size:11px; color:#8899aa; text-transform:uppercase; letter-spacing:1px; }
.val-value  { font-size:1.2rem; font-family:'Space Mono',monospace; font-weight:700; }
.score-bar-wrap { background:#1a2235; border-radius:8px; height:8px; margin-top:6px; }
div[data-testid="stMetricValue"] { font-family:'Space Mono',monospace; font-size:1.4rem; }
div[data-testid="stMetricLabel"] { font-size:0.75rem; color:#8899aa; text-transform:uppercase; letter-spacing:1px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# STOCK UNIVERSE  (cached 24 h)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def fetch_nifty500_list():
    try:
        headers = {"User-Agent":"Mozilla/5.0","Accept-Language":"en-US,en;q=0.9",
                   "Referer":"https://www.nseindia.com/market-data/live-equity-market"}
        s = requests.Session()
        s.get("https://www.nseindia.com", headers=headers, timeout=10)
        r = s.get("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500",
                  headers=headers, timeout=15)
        stocks = {}
        for item in r.json().get("data", []):
            sym  = item.get("symbol","")
            name = item.get("meta",{}).get("companyName", sym)
            if sym and sym != "NIFTY 500":
                short = name.replace(" Limited","").replace(" Ltd.","").replace(" Ltd","").strip()[:30]
                stocks[short] = f"{sym}.NS"
        return stocks if len(stocks) > 50 else None
    except:
        return None

@st.cache_data(ttl=86400)
def get_fallback():
    return {
        "Reliance":"RELIANCE.NS","TCS":"TCS.NS","HDFC Bank":"HDFCBANK.NS",
        "Infosys":"INFY.NS","ICICI Bank":"ICICIBANK.NS","HUL":"HINDUNILVR.NS",
        "ITC":"ITC.NS","SBI":"SBIN.NS","Bharti Airtel":"BHARTIARTL.NS",
        "Kotak Bank":"KOTAKBANK.NS","LT":"LT.NS","Axis Bank":"AXISBANK.NS",
        "Asian Paints":"ASIANPAINT.NS","HCL Tech":"HCLTECH.NS","Maruti":"MARUTI.NS",
        "Sun Pharma":"SUNPHARMA.NS","Titan":"TITAN.NS","NTPC":"NTPC.NS",
        "Power Grid":"POWERGRID.NS","Wipro":"WIPRO.NS","UltraTech":"ULTRACEMCO.NS",
        "M&M":"M&M.NS","Bajaj Finance":"BAJFINANCE.NS","Tech Mahindra":"TECHM.NS",
        "Bajaj Auto":"BAJAJ-AUTO.NS","ONGC":"ONGC.NS","JSW Steel":"JSWSTEEL.NS",
        "Tata Steel":"TATASTEEL.NS","Adani Ports":"ADANIPORTS.NS","Cipla":"CIPLA.NS",
        "LIC":"LICI.NS","Adani Enterprises":"ADANIENT.NS","Coal India":"COALINDIA.NS",
        "Tata Motors":"TATAMOTORS.NS","BEL":"BEL.NS","Grasim":"GRASIM.NS",
        "Dr Reddys":"DRREDDY.NS","Britannia":"BRITANNIA.NS","Hindalco":"HINDALCO.NS",
        "Eicher Motors":"EICHERMOT.NS","Bajaj Finserv":"BAJAJFINSV.NS",
        "Hero MotoCorp":"HEROMOTOCO.NS","Tata Consumer":"TATACONSUM.NS",
        "Divis Lab":"DIVISLAB.NS","Apollo Hospitals":"APOLLOHOSP.NS",
        "IndusInd Bank":"INDUSINDBK.NS","Shriram Finance":"SHRIRAMFIN.NS",
        "Trent":"TRENT.NS","Jio Financial":"JIOFIN.NS",
        "Havells":"HAVELLS.NS","Pidilite":"PIDILITIND.NS","Marico":"MARICO.NS",
        "Muthoot Finance":"MUTHOOTFIN.NS","Godrej Consumer":"GODREJCP.NS",
        "Torrent Pharma":"TORNTPHARM.NS","Lupin":"LUPIN.NS",
        "Aurobindo":"AUROPHARMA.NS","Biocon":"BIOCON.NS",
        "Polycab":"POLYCAB.NS","ABB India":"ABB.NS","Siemens":"SIEMENS.NS",
        "Cummins India":"CUMMINSIND.NS","HAL":"HAL.NS","BHEL":"BHEL.NS",
        "IRFC":"IRFC.NS","PFC":"PFC.NS","REC":"RECLTD.NS","IRCTC":"IRCTC.NS",
        "Zomato":"ZOMATO.NS","Nykaa":"NYKAA.NS","PB Fintech":"POLICYBZR.NS",
        "Info Edge":"NAUKRI.NS","Persistent":"PERSISTENT.NS","Coforge":"COFORGE.NS",
        "KPIT Tech":"KPITTECH.NS","LTIMindtree":"LTIM.NS","Tata Elxsi":"TATAELXSI.NS",
        "Max Healthcare":"MAXHEALTH.NS","Fortis":"FORTIS.NS",
        "Dr Lal PathLabs":"LALPATHLAB.NS","Ipca Lab":"IPCALAB.NS","Alkem":"ALKEM.NS",
        "SRF":"SRF.NS","PI Industries":"PIIND.NS","UPL":"UPL.NS",
        "Tata Power":"TATAPOWER.NS","Adani Green":"ADANIGREEN.NS",
        "JSW Energy":"JSWENERGY.NS","NHPC":"NHPC.NS",
        "Bank of Baroda":"BANKBARODA.NS","PNB":"PNB.NS","Canara Bank":"CANBK.NS",
        "Federal Bank":"FEDERALBNK.NS","IDFC First":"IDFCFIRSTB.NS",
        "AU Small Finance":"AUBANK.NS","Cholamandalam":"CHOLAFIN.NS",
        "L&T Finance":"LTF.NS","HDFC Life":"HDFCLIFE.NS","SBI Life":"SBILIFE.NS",
        "DLF":"DLF.NS","Macrotech":"LODHA.NS","Godrej Properties":"GODREJPROP.NS",
        "Deepak Nitrite":"DEEPAKNTR.NS","Aarti Industries":"AARTIIND.NS",
        "MRF":"MRF.NS","Apollo Tyres":"APOLLOTYRE.NS","Balkrishna Ind":"BALKRISIND.NS",
        "Bosch":"BOSCHLTD.NS","Exide":"EXIDEIND.NS","Tube Investments":"TIINDIA.NS",
        "Page Industries":"PAGEIND.NS","Varun Beverages":"VBL.NS",
        "Dabur":"DABUR.NS","Colgate":"COLPAL.NS","Emami":"EMAMILTD.NS",
        "Dixon Tech":"DIXON.NS","Kaynes Tech":"KAYNES.NS","Amber Enterprises":"AMBER.NS",
        "Kajaria Ceramics":"KAJARIACER.NS","ACC":"ACC.NS",
        "Ambuja Cements":"AMBUJACEM.NS","Shree Cement":"SHREECEM.NS",
        "Dalmia Bharat":"DALBHARAT.NS","Container Corp":"CONCOR.NS",
        "Indian Hotels":"INDHOTEL.NS","Lemon Tree":"LEMONTREE.NS",
        "PVR INOX":"PVRINOX.NS","Sun TV":"SUNTV.NS","Zee Entertainment":"ZEEL.NS",
        "Kalyan Jewellers":"KALYANKJIL.NS","Avenue Supermarts":"DMART.NS",
        "NMDC":"NMDC.NS","Vedanta":"VEDL.NS","National Aluminium":"NATIONALUM.NS",
        "SAIL":"SAIL.NS","Torrent Power":"TORNTPOWER.NS","CESC":"CESC.NS",
        "Gujarat Gas":"GUJGASLTD.NS","Indraprastha Gas":"IGL.NS",
    }

with st.spinner("Loading stock list..."):
    STOCKS = fetch_nifty500_list() or get_fallback()

ALL_NAMES   = sorted(STOCKS.keys())
SECTORS_ALL = ["Technology","Financial Services","Healthcare","Consumer Cyclical",
               "Consumer Defensive","Energy","Basic Materials","Industrials",
               "Utilities","Communication Services","Real Estate"]
STYLE_SECTORS = {
    "Growth":   ["Technology","Communication Services","Consumer Cyclical","Healthcare"],
    "Value":    ["Financial Services","Energy","Basic Materials","Utilities","Industrials"],
    "Dividend": ["Utilities","Energy","Consumer Defensive","Financial Services"],
    "Momentum": [],
}

# ══════════════════════════════════════════════════════════════════════════════
# INDICATOR FUNCTIONS  (pure computation — no I/O)
# ══════════════════════════════════════════════════════════════════════════════
def compute_rsi(s, p=14):
    d = s.diff(); g = d.clip(lower=0).rolling(p).mean()
    l = (-d.clip(upper=0)).rolling(p).mean()
    return 100 - 100/(1 + g/l.replace(0,np.nan))

def compute_macd(s, fast=12, slow=26, sig=9):
    m = s.ewm(span=fast,adjust=False).mean() - s.ewm(span=slow,adjust=False).mean()
    sl = m.ewm(span=sig,adjust=False).mean()
    return m, sl, m-sl

def compute_bb(s, w=20, n=2):
    sma = s.rolling(w).mean(); std = s.rolling(w).std()
    u = sma+n*std; l = sma-n*std
    return u, sma, l, (s-l)/(u-l+1e-9)

def compute_adx(df, p=14):
    hi,lo,cl = df["High"],df["Low"],df["Close"]
    pdm = hi.diff().clip(lower=0); mdm = (-lo.diff()).clip(lower=0)
    tr  = pd.concat([(hi-lo),(hi-cl.shift()).abs(),(lo-cl.shift()).abs()],axis=1).max(axis=1)
    atr = tr.ewm(span=p,adjust=False).mean()
    pdi = 100*pdm.ewm(span=p,adjust=False).mean()/atr
    mdi = 100*mdm.ewm(span=p,adjust=False).mean()/atr
    dx  = 100*(pdi-mdi).abs()/(pdi+mdi+1e-9)
    return dx.ewm(span=p,adjust=False).mean(), pdi, mdi

def compute_obv(df):
    return (np.sign(df["Close"].diff()).fillna(0)*df["Volume"]).cumsum()

def compute_sr(df, w=20):
    h = df["High"].rolling(w,center=True).max()
    l = df["Low"].rolling(w,center=True).min()
    return (l.dropna().iloc[-1] if not l.dropna().empty else None,
            h.dropna().iloc[-1] if not h.dropna().empty else None)

def compute_signals(df):
    c = df["Close"]; v = df["Volume"]
    df["MA50"]  = c.rolling(50).mean()
    df["MA200"] = c.rolling(200).mean()
    df["RSI"]   = compute_rsi(c)
    df["MACD"],df["MACD_S"],df["MACD_H"] = compute_macd(c)
    df["BBU"],df["BBM"],df["BBL"],df["BBP"] = compute_bb(c)
    df["ADX"],df["PDI"],df["MDI"] = compute_adx(df)
    df["OBV"]   = compute_obv(df)
    df["OBVMA"] = df["OBV"].rolling(20).mean()
    df["VA"]    = v.rolling(20).mean()
    df["VS"]    = v > df["VA"]*2
    sup, res    = compute_sr(df)
    row = df.iloc[-1]; prev = df.iloc[-2]

    sc = {}
    rsi = float(row["RSI"]) if pd.notna(row["RSI"]) else 50
    sc["RSI"]      = 2 if rsi<30 else (1 if rsi<40 else (-2 if rsi>70 else (-1 if rsi>60 else 0)))
    sc["MACD"]     = (2  if row["MACD"]>row["MACD_S"] and prev["MACD"]<=prev["MACD_S"] else
                     (-2 if row["MACD"]<row["MACD_S"] and prev["MACD"]>=prev["MACD_S"] else
                     (0.5 if row["MACD"]>row["MACD_S"] else -0.5)))
    if pd.notna(row["MA50"]) and pd.notna(row["MA200"]):
        sc["MA"] = (2  if row["MA50"]>row["MA200"] and prev["MA50"]<=prev["MA200"] else
                   (-2  if row["MA50"]<row["MA200"] and prev["MA50"]>=prev["MA200"] else
                   (1   if row["MA50"]>row["MA200"] else -1)))
    else: sc["MA"] = 0
    bbp = float(row["BBP"]) if pd.notna(row["BBP"]) else 0.5
    sc["BB"]  = 1 if bbp<0.05 else (-1 if bbp>0.95 else 0)
    sc["ADX"] = (1 if pd.notna(row["ADX"]) and float(row["ADX"])>25 and row["PDI"]>row["MDI"]
                 else (-1 if pd.notna(row["ADX"]) and float(row["ADX"])>25 and row["PDI"]<row["MDI"] else 0))
    if pd.notna(row["OBVMA"]):
        slope = float(row["OBV"]) - float(df["OBV"].iloc[-5])
        sc["OBV"] = 1 if slope>0 else (-1 if slope<0 else 0)
    else: sc["OBV"] = 0
    sc["Vol"] = (0.5 if row["VS"] and row["Close"]>prev["Close"] else
                (-0.5 if row["VS"] else 0))
    if sup and res:
        pos = (float(row["Close"])-float(sup))/(float(res)-float(sup)+1e-9)
        sc["SR"] = 0.5 if pos<0.15 else (-0.5 if pos>0.85 else 0)
    else: sc["SR"] = 0

    raw   = sum(sc.values())
    tscore = round(min(10,max(0,(raw+10)/2)),1)
    signal = "BUY" if raw>=2.5 else ("SELL" if raw<=-2.5 else "HOLD")

    def sf(x,d=2):
        try: v=float(x); return round(v,d) if pd.notna(v) else None
        except: return None

    return dict(
        signal=signal, tech_score=tscore, score_raw=raw, scores=sc,
        rsi=sf(row["RSI"],1), macd=sf(row["MACD"]), macd_sig=sf(row["MACD_S"]),
        ma50=sf(row["MA50"]), ma200=sf(row["MA200"]),
        bb_upper=sf(row["BBU"]), bb_lower=sf(row["BBL"]),
        bb_mid=sf(row["BBM"]), bb_pctb=sf(row["BBP"],3),
        adx=sf(row["ADX"],1), plus_di=sf(row["PDI"],1), minus_di=sf(row["MDI"],1),
        obv_trend=("▲ Rising" if sc.get("OBV",0)>0 else ("▼ Falling" if sc.get("OBV",0)<0 else "→ Flat")),
        vol_spike=bool(row["VS"]),
        close=sf(row["Close"]), open_=sf(row["Open"]),
        change_pct=round(((float(row["Close"])-float(prev["Close"]))/float(prev["Close"]))*100,2),
        support=round(float(sup),2) if sup else None,
        resistance=round(float(res),2) if res else None,
        df=df,
    )

# ══════════════════════════════════════════════════════════════════════════════
# DATA FETCH  (price + fundamentals) — called ONCE via "Pull Universe Data"
# These functions are NOT called anywhere in the tab rendering code.
# ══════════════════════════════════════════════════════════════════════════════
def _fetch_one_price(ticker, period):
    df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
    if df.empty: return None
    df.columns = [c[0] if isinstance(c,tuple) else c for c in df.columns]
    return df

def _fetch_one_fund(ticker):
    try:
        info = yf.Ticker(ticker).info
        def gv(k):
            v=info.get(k); return round(float(v),2) if v and str(v)!="None" else None
        roe=gv("returnOnEquity"); dy=gv("dividendYield")

        # ── Analyst consensus ──────────────────────────────────────────────────
        rec_key  = info.get("recommendationKey","")   # strong_buy/buy/hold/sell/strong_sell
        n_analyst= info.get("numberOfAnalystOpinions")
        target   = gv("targetMeanPrice")
        cur_price= gv("currentPrice") or gv("regularMarketPrice")
        upside   = None
        if target and cur_price and cur_price > 0:
            upside = round((target - cur_price) / cur_price * 100, 1)

        # Normalise recommendationKey to display label
        rec_label_map = {
            "strong_buy":  "⭐ Strong Buy",
            "buy":         "🟢 Buy",
            "hold":        "🟡 Hold",
            "underperform":"🟠 Underperform",
            "sell":        "🔴 Sell",
            "strong_sell": "🔴 Strong Sell",
        }
        rec_label = rec_label_map.get(rec_key.lower().replace(" ","_"), rec_key.title() if rec_key else "—")

        return dict(
            pe=gv("trailingPE"), pb=gv("priceToBook"),
            roe=round(roe*100,1) if roe else None,
            de=gv("debtToEquity"),
            dy=round(dy*100,2) if dy else None,
            ev_ebitda=gv("enterpriseToEbitda"), peg=gv("pegRatio"),
            mcap_cr=round(float(info["marketCap"])/1e7,0) if info.get("marketCap") else None,
            sector=info.get("sector","—"), industry=info.get("industry","—"),
            # Analyst fields
            analyst_rec=rec_label,
            analyst_n=int(n_analyst) if n_analyst else None,
            analyst_target=target,
            analyst_upside=upside,
        )
    except: return {}

def pull_universe(names, period, fetch_fund):
    """
    Fetch price + signals + fundamentals for every name in `names`.
    Results are stored directly into st.session_state so nothing else
    ever needs to call yfinance again until the user explicitly refreshes.
    """
    results = {}; fundamentals = {}; failed = []

    bar  = st.progress(0, text="Initialising…")
    info = st.empty()
    n    = len(names)

    for i, name in enumerate(names):
        ticker = STOCKS[name]
        info.markdown(f"⏳ Fetching **{name}** `{ticker.replace('.NS','')}` — {i+1} / {n}")
        try:
            df = _fetch_one_price(ticker, period)
            if df is not None and len(df) > 60:
                results[name] = compute_signals(df)
                if fetch_fund:
                    fundamentals[name] = _fetch_one_fund(ticker)
            else:
                failed.append(name)
        except:
            failed.append(name)
        bar.progress((i+1)/n, text=f"{round((i+1)/n*100)}% complete")

    bar.empty(); info.empty()

    # ── Save previous signals for change detection before overwriting ──────────
    if "universe" in st.session_state:
        prev = {name: r["signal"] for name, r in st.session_state["universe"].items()}
        st.session_state["prev_signals"] = prev
        st.session_state["prev_pulled_at"] = st.session_state.get("pulled_at","")

    st.session_state["universe"]        = results
    st.session_state["fundamentals"]    = fundamentals
    st.session_state["universe_names"]  = names
    st.session_state["universe_period"] = period
    st.session_state["pulled_at"]       = datetime.now().strftime("%d %b %Y %H:%M")
    st.session_state["failed"]          = failed

# ══════════════════════════════════════════════════════════════════════════════
# ALLOCATION HELPERS  (pure computation)
# ══════════════════════════════════════════════════════════════════════════════
def classify_cap(mcap_cr):
    if mcap_cr is None: return "Unknown"
    return "Large Cap" if mcap_cr>=20000 else ("Mid Cap" if mcap_cr>=5000 else "Small Cap")

def style_score(r, f, style):
    ts  = r.get("tech_score",5)
    pe  = f.get("pe"); dy = f.get("dy"); roe = f.get("roe"); pb = f.get("pb")
    if style == "Growth":
        s = ts
        if roe and roe>15: s+=1
        if pe  and pe<40:  s+=0.5
        return s
    if style == "Value":
        s = 0
        if pe  and pe<20:  s+=2
        if pb  and pb<2:   s+=2
        if roe and roe>10: s+=1
        if r["signal"]!="SELL": s+=1
        return s
    if style == "Dividend":
        s = 0
        if dy and dy>2: s+=3
        if dy and dy>1: s+=1
        if r["signal"]!="SELL": s+=1
        return s
    if style == "Momentum":
        s = ts
        if r["signal"]=="BUY": s+=2
        if r.get("adx") and r["adx"]>25: s+=1
        return s
    return ts

@st.cache_data(ttl=600)
def fetch_corr_prices(tickers_tuple, period):
    prices = {}
    for t in list(tickers_tuple):
        df = yf.download(t, period=period, progress=False, auto_adjust=True)
        if not df.empty:
            df.columns = [c[0] if isinstance(c,tuple) else c for c in df.columns]
            prices[t] = df["Close"]
    return pd.DataFrame(prices).dropna(how="all") if prices else pd.DataFrame()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  — Universe settings + Pull button only
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌐 Universe Settings")
    st.caption("Configure what to pull. Then click **Pull Data** once.")

    cap_filter = st.selectbox("Quick Filter",["Custom","Top 50","Top 100","Top 200","All"])
    if   cap_filter=="All":     def_stocks = ALL_NAMES
    elif cap_filter=="Top 50":  def_stocks = ALL_NAMES[:50]
    elif cap_filter=="Top 100": def_stocks = ALL_NAMES[:100]
    elif cap_filter=="Top 200": def_stocks = ALL_NAMES[:200]
    else:                       def_stocks = ALL_NAMES[:20]

    universe_names = st.multiselect(
        "Stocks to pull",
        options=ALL_NAMES,
        default=def_stocks[:20],
        help="Select all stocks you want available across all tabs.",
    )
    period       = st.selectbox("Data Period",["1mo","3mo","6mo","1y","2y"],index=2)
    fetch_fund   = st.checkbox("Include Valuation Ratios", value=True,
                               help="Adds ~1s per stock but enables P/E, ROE etc.")

    st.caption(f"~{len(universe_names)*1.5:.0f}s estimated pull time")

    pull_btn     = st.button("🔄 Pull Universe Data", type="primary", use_container_width=True)
    refresh_btn  = st.button("♻️ Refresh (clear cache)", use_container_width=True,
                             help="Wipes cached data and re-fetches fresh prices.")

    # Status
    if "pulled_at" in st.session_state:
        n_pulled = len(st.session_state.get("universe",{}))
        st.success(f"✅ {n_pulled} stocks loaded\n\n🕐 {st.session_state['pulled_at']}")
        if st.session_state.get("failed"):
            st.warning(f"⚠️ {len(st.session_state['failed'])} failed")
    else:
        st.info("No data pulled yet.")

    st.markdown("---")
    st.markdown("**🔍 These filters apply instantly** across all tabs without re-fetching:")
    st.markdown("• Signal type • Min score • Sector")
    st.markdown("---")
    st.caption("Data: Yahoo Finance · 15-min delay")

# Handle refresh
if refresh_btn:
    for k in ["universe","fundamentals","universe_names","universe_period","pulled_at","failed"]:
        st.session_state.pop(k, None)
    st.rerun()

# Handle pull
if pull_btn:
    if not universe_names:
        st.sidebar.error("Select at least one stock.")
    else:
        pull_universe(universe_names, period, fetch_fund)
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MACRO DATA FETCH  (cached 15 min)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=900)
def fetch_macro():
    """Fetch Nifty VIX, USD/INR, 10Y G-Sec yield proxy, Nifty 50 index."""
    results = {}
    tickers = {
        "Nifty VIX":    "^INDIAVIX",
        "USD/INR":      "USDINR=X",
        "Nifty 50":     "^NSEI",
        "10Y G-Sec":    "0P0000YRWN.BO",   # HDFC Gilt fund as proxy
        "Brent Crude":  "BZ=F",
    }
    for label, ticker in tickers.items():
        try:
            df = yf.download(ticker, period="5d", progress=False, auto_adjust=True)
            if df.empty: continue
            df.columns = [c[0] if isinstance(c,tuple) else c for c in df.columns]
            price = float(df["Close"].iloc[-1])
            prev  = float(df["Close"].iloc[-2])
            chg   = round((price - prev) / prev * 100, 2)
            results[label] = {"price": round(price,2), "chg": chg}
        except:
            pass
    return results

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("# 📈 Nifty 500 Signal Dashboard")
st.markdown(f"*{len(STOCKS)} stocks in universe · {datetime.now().strftime('%d %b %Y, %H:%M IST')}*")

# Initialize session state defaults once per session
st.session_state.setdefault("universe", {})
st.session_state.setdefault("fundamentals", {})
st.session_state.setdefault("universe_names", [])
st.session_state.setdefault("universe_period", "1y")
st.session_state.setdefault("pulled_at", "")
st.session_state.setdefault("failed", [])
st.session_state.setdefault("prev_signals", {})
st.session_state.setdefault("prev_pulled_at", "")

# Guard — nothing to show if no data pulled yet
universe = st.session_state.get("universe", {})
fundamentals = st.session_state.get("fundamentals", {})
pulled_period = st.session_state.get("universe_period", "1y")

if not universe:
    st.info("👈 Select stocks in the sidebar and click **🔄 Pull Universe Data** to begin. You only need to do this once per session.")
    st.stop()

all_scanned = sorted(universe.keys())

st.markdown(f"*Universe: **{len(universe)} stocks** · Data as of **{st.session_state.get('pulled_at', 'not available')}***")

# ── Macro Header Bar ───────────────────────────────────────────────────────────
macro = fetch_macro()
if macro:
    mcols = st.columns(len(macro))
    macro_meta = {
        "Nifty 50":    {"icon":"📊", "fmt": lambda p: f"{p:,.0f}",   "unit":""},
        "Nifty VIX":   {"icon":"⚡", "fmt": lambda p: f"{p:.2f}",    "unit":"",
                        "note": lambda v: "🟢 Low fear" if v<15 else ("🟡 Elevated" if v<20 else "🔴 High fear")},
        "USD/INR":     {"icon":"💱", "fmt": lambda p: f"₹{p:.2f}",   "unit":""},
        "10Y G-Sec":   {"icon":"🏦", "fmt": lambda p: f"₹{p:.2f}",   "unit":"(NAV proxy)"},
        "Brent Crude": {"icon":"🛢️", "fmt": lambda p: f"${p:.2f}",   "unit":"/bbl"},
    }
    for idx, (label, data) in enumerate(macro.items()):
        with mcols[idx]:
            meta   = macro_meta.get(label, {"icon":"📈","fmt":lambda p:f"{p:.2f}","unit":""})
            chg    = data["chg"]
            price  = data["price"]
            cc     = "#00e5a0" if chg >= 0 else "#ff4d6d"
            arrow  = "▲" if chg >= 0 else "▼"
            note   = meta.get("note","")
            note_s = note(price) if callable(note) else ""
            st.markdown(f"""
            <div class="val-card">
              <div class="val-label">{meta['icon']} {label}</div>
              <div class="val-value" style="color:#e0e6f0">{meta['fmt'](price)}</div>
              <div style="font-size:12px;color:{cc}">{arrow} {chg:+.2f}%</div>
              <div style="font-size:10px;color:#667788">{meta['unit']} {note_s}</div>
            </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Instant sidebar filters (no fetch) ──────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Live Filters")
    sig_filter   = st.multiselect("Signal", ["BUY","HOLD","SELL"], default=["BUY","HOLD","SELL"])
    min_score    = st.slider("Min Tech Score", 0.0, 10.0, 0.0, 0.5)
    sector_filter= st.multiselect("Sector", SECTORS_ALL, default=[])

# Apply filters — pure pandas, instant
def apply_filters(universe, fundamentals):
    filtered = {}
    for name, r in universe.items():
        if r["signal"] not in sig_filter: continue
        if r["tech_score"] < min_score:   continue
        if sector_filter:
            sec = fundamentals.get(name,{}).get("sector","—")
            if sec not in sector_filter: continue
        filtered[name] = r
    return filtered

filtered = apply_filters(universe, fundamentals)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_signals, tab_detail, tab_alloc, tab_global, tab_combined = st.tabs([
    "📊 Signal Dashboard",
    "📉 Deep Dive Chart",
    "🗂️ India Allocation",
    "🌍 Global Allocation",
    "🔀 Combined Portfolio",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — SIGNAL DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
with tab_signals:
    if not filtered:
        st.warning("No stocks match the current filters. Adjust the Signal / Score / Sector filters in the sidebar.")
    else:
        buys  = sum(1 for r in filtered.values() if r["signal"]=="BUY")
        sells = sum(1 for r in filtered.values() if r["signal"]=="SELL")
        holds = sum(1 for r in filtered.values() if r["signal"]=="HOLD")
        vols  = sum(1 for r in filtered.values() if r["vol_spike"])
        avg_sc= round(np.mean([r["tech_score"] for r in filtered.values()]),1)
        n     = len(filtered)

        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("📊 Showing",    n, f"of {len(universe)}")
        c2.metric("🟢 BUY",        buys,  f"{round(buys/n*100)}%")
        c3.metric("🔴 SELL",       sells, f"{round(sells/n*100)}%")
        c4.metric("🟡 HOLD",       holds, f"{round(holds/n*100)}%")
        c5.metric("⚡ Vol Spikes", vols,  f"{round(vols/n*100)}%")
        c6.metric("⭐ Avg Score",  f"{avg_sc}/10")
        st.markdown("---")

        st.markdown("### 📊 Signal & Valuation Table")
        rows = []
        for name, r in filtered.items():
            f = fundamentals.get(name,{})
            rows.append({
                "Stock":name, "Ticker":STOCKS[name].replace(".NS",""),
                "Price (₹)":r["close"],
                "Change %":f"{'+' if r['change_pct']>0 else ''}{r['change_pct']}%",
                "Signal":r["signal"], "Score /10":r["tech_score"],
                "RSI":r["rsi"], "ADX":r["adx"], "BB %B":r["bb_pctb"],
                "OBV":r["obv_trend"],
                "Vol Spike":"⚡" if r["vol_spike"] else "—",
                "P/E":f.get("pe"), "P/B":f.get("pb"), "ROE %":f.get("roe"),
                "D/E":f.get("de"), "Div Yld %":f.get("dy"),
                "EV/EBITDA":f.get("ev_ebitda"), "Sector":f.get("sector","—"),
                "Analyst":f.get("analyst_rec","—"),
                "# Analysts":f.get("analyst_n"),
                "Target ₹":f.get("analyst_target"),
                "Upside %":f.get("analyst_upside"),
            })

        df_tbl = pd.DataFrame(rows).sort_values(["Signal","Score /10"],ascending=[True,False])

        def hl_sig(v):
            return {"BUY":"color:#00e5a0;font-weight:bold","SELL":"color:#ff4d6d;font-weight:bold"}.get(v,"color:#f0a500;font-weight:bold")
        def hl_chg(v):
            try: x=float(str(v).replace("%","").replace("+","")); return f"color:{'#00e5a0' if x>0 else '#ff4d6d'}"
            except: return ""
        def hl_sc(v):
            try: x=float(v); return ("color:#00e5a0;font-weight:bold" if x>=7 else ("color:#f0a500" if x>=5 else "color:#ff4d6d"))
            except: return ""

        fmt = {"Score /10":"{:.1f}","P/E":"{:.1f}","P/B":"{:.2f}","ROE %":"{:.1f}",
               "D/E":"{:.1f}","Div Yld %":"{:.2f}","EV/EBITDA":"{:.1f}","BB %B":"{:.2f}",
               "Target ₹":"{:.1f}","Upside %":"{:.1f}%"}

        def hl_analyst(v):
            if "Strong Buy" in str(v): return "color:#00e5a0;font-weight:bold"
            if "Buy"        in str(v): return "color:#00b37a"
            if "Hold"       in str(v): return "color:#f0a500"
            if "Underperform" in str(v): return "color:#ff8844"
            if "Sell"       in str(v): return "color:#ff4d6d;font-weight:bold"
            return "color:#8899aa"

        def hl_upside(v):
            try:
                x = float(str(v).replace("%",""))
                return ("color:#00e5a0;font-weight:bold" if x >= 15 else
                        ("color:#00b37a" if x >= 5 else
                         ("color:#f0a500" if x >= 0 else "color:#ff4d6d")))
            except: return ""

        styled = (df_tbl.style
                  .map(hl_sig,     subset=["Signal"])
                  .map(hl_chg,     subset=["Change %"])
                  .map(hl_sc,      subset=["Score /10"])
                  .map(hl_analyst, subset=["Analyst"])
                  .map(hl_upside,  subset=["Upside %"])
                  .set_properties(**{"background-color":"#0f1623","border-color":"#1e3a5f"})
                  .format(fmt, na_rep="—"))
        st.dataframe(styled, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download CSV", df_tbl.to_csv(index=False), "signals.csv", "text/csv", key="dl_signals")
        st.markdown("---")

        st.markdown("### 🔍 Screeners")
        sc1,sc2,sc3,sc4 = st.tabs([f"🟢 BUY ({buys})",f"🔴 SELL ({sells})",f"⚡ Vol ({vols})","⭐ Top 12"])

        def render_cards(items):
            if not items: st.info("None."); return
            cols = st.columns(min(4,len(items)))
            for i,(name,r) in enumerate(items):
                with cols[i%4]:
                    sig   = r["signal"]
                    color = {"BUY":"#00e5a0","SELL":"#ff4d6d","HOLD":"#f0a500"}[sig]
                    arrow = {"BUY":"▲","SELL":"▼","HOLD":"●"}[sig]
                    cc    = "#00e5a0" if r["change_pct"]>0 else "#ff4d6d"
                    f     = fundamentals.get(name,{})
                    pe    = f"P/E {f['pe']:.0f}" if f.get("pe") else ""
                    roe   = f"ROE {f['roe']}%" if f.get("roe") else ""
                    st.markdown(f"""<div class="metric-card" style="border-color:{color}">
                      <b>{name}</b> <span style="color:#445566;font-size:11px">{STOCKS[name].replace('.NS','')}</span><br/>
                      <span style="color:{color};font-family:'Space Mono'">{arrow} {sig}</span>
                      <span style="float:right;color:#aac;font-family:'Space Mono';font-size:13px">⭐{r['tech_score']}</span><br/>
                      ₹{r['close']} &nbsp;<span style="color:{cc}">{'+' if r['change_pct']>0 else ''}{r['change_pct']}%</span><br/>
                      <span style="font-size:11px;color:#8899aa">RSI:{r['rsi']} · ADX:{r['adx']} · {r['obv_trend']}</span><br/>
                      <span style="font-size:11px;color:#667788">{pe} {roe}</span>
                    </div>""", unsafe_allow_html=True)

        with sc1: render_cards([(nm,r) for nm,r in filtered.items() if r["signal"]=="BUY"])
        with sc2: render_cards([(nm,r) for nm,r in filtered.items() if r["signal"]=="SELL"])
        with sc3: render_cards([(nm,r) for nm,r in filtered.items() if r["vol_spike"]])
        with sc4: render_cards(sorted(filtered.items(),key=lambda x:x[1]["tech_score"],reverse=True)[:12])

        st.markdown("---")

        # ── SIGNAL CHANGE DETECTION ────────────────────────────────────────────
        prev_signals = st.session_state.get("prev_signals", {})
        if prev_signals:
            prev_at = st.session_state.get("prev_pulled_at","previous scan")
            st.markdown(f"### 🔔 Signal Changes  *(since {prev_at})*")
            st.caption("Stocks whose signal flipped since the last Pull Universe Data.")

            changes = []
            flip_priority = {
                ("HOLD","BUY"):  ("🚀 HOLD → BUY",  "#00e5a0", 1),
                ("SELL","BUY"):  ("⚡ SELL → BUY",  "#00e5a0", 2),
                ("BUY","SELL"):  ("💀 BUY → SELL",  "#ff4d6d", 3),
                ("HOLD","SELL"): ("⬇️ HOLD → SELL", "#ff4d6d", 4),
                ("BUY","HOLD"):  ("⚠️ BUY → HOLD",  "#f0a500", 5),
                ("SELL","HOLD"): ("↗️ SELL → HOLD",  "#f0a500", 6),
            }
            for name, r in universe.items():
                old_sig = prev_signals.get(name)
                new_sig = r["signal"]
                if old_sig and old_sig != new_sig:
                    key = (old_sig, new_sig)
                    label, color, priority = flip_priority.get(
                        key, (f"{old_sig}→{new_sig}", "#8899aa", 9))
                    f = fundamentals.get(name, {})
                    changes.append({
                        "priority": priority,
                        "name":     name,
                        "ticker":   STOCKS[name].replace(".NS",""),
                        "label":    label,
                        "color":    color,
                        "from":     old_sig,
                        "to":       new_sig,
                        "score":    r["tech_score"],
                        "rsi":      r["rsi"],
                        "close":    r["close"],
                        "chg":      r["change_pct"],
                        "sector":   f.get("sector","—"),
                    })

            changes.sort(key=lambda x: x["priority"])

            if changes:
                # Summary badges
                upgrades   = [c for c in changes if c["to"]=="BUY"]
                downgrades = [c for c in changes if c["to"]=="SELL"]
                neutral    = [c for c in changes if c["to"]=="HOLD"]
                b1,b2,b3,b4 = st.columns(4)
                b1.metric("📋 Total Changes", len(changes))
                b2.metric("🟢 → BUY",   len(upgrades),   delta=f"+{len(upgrades)}")
                b3.metric("🔴 → SELL",  len(downgrades), delta=f"-{len(downgrades)}", delta_color="inverse")
                b4.metric("🟡 → HOLD",  len(neutral))

                # Change cards
                ch_cols = st.columns(min(4, len(changes)))
                for i, c in enumerate(changes):
                    with ch_cols[i % 4]:
                        cc = "#00e5a0" if c["chg"] > 0 else "#ff4d6d"
                        st.markdown(f"""
                        <div class="metric-card" style="border-left:4px solid {c['color']}">
                          <b>{c['name']}</b>
                          <span style="color:#445566;font-size:11px"> {c['ticker']}</span><br/>
                          <span style="color:{c['color']};font-family:'Space Mono';font-size:13px">{c['label']}</span><br/>
                          ₹{c['close']} <span style="color:{cc}">{'+' if c['chg']>0 else ''}{c['chg']}%</span><br/>
                          <span style="font-size:11px;color:#8899aa">Score:{c['score']} · RSI:{c['rsi']}</span><br/>
                          <span style="font-size:10px;color:#556677">{c['sector']}</span>
                        </div>""", unsafe_allow_html=True)
            else:
                st.success("✅ No signal changes since the last scan — all signals are stable.")
        else:
            st.info("🔔 Signal changes will appear here after your **second** Pull Universe Data. "
                    "Pull now, make changes, pull again to see what flipped.")

        st.markdown("---")

        # ── SECTOR ROTATION HEATMAP ───────────────────────────────────────────
        st.markdown("### 🌡️ Sector Rotation Heatmap")
        st.caption("Which sectors have the most BUY / HOLD / SELL signals? "
                   "Warm colours = bullish momentum. Cool colours = bearish.")

        # Build sector × signal matrix from full universe (not just filtered)
        sector_rows = []
        for name, r in universe.items():
            sec = fundamentals.get(name, {}).get("sector", "Unknown")
            if sec in ("—", "", None): sec = "Unknown"
            sector_rows.append({
                "Sector": sec,
                "Signal": r["signal"],
                "Score":  r["tech_score"],
            })

        if sector_rows:
            sec_df = pd.DataFrame(sector_rows)

            # Pivot: sector × signal → count
            pivot_count = (sec_df.groupby(["Sector","Signal"])
                           .size().unstack(fill_value=0)
                           .reindex(columns=["BUY","HOLD","SELL"], fill_value=0))

            avg_score = sec_df.groupby("Sector")["Score"].mean().round(1)
            pivot_count["Total"]      = pivot_count.sum(axis=1)
            pivot_count["Sentiment"]  = (
                (pivot_count["BUY"] - pivot_count["SELL"]) /
                pivot_count["Total"].replace(0, np.nan)
            ).fillna(0).round(3)          # -1 = all SELL, +1 = all BUY
            pivot_count["Bull Ratio"] = (
                pivot_count["BUY"] /
                (pivot_count["BUY"] + pivot_count["SELL"]).replace(0, np.nan)
            ).fillna(0.5).round(2)
            pivot_count["Avg Score"]  = avg_score
            pivot_count = pivot_count.sort_values("Sentiment", ascending=False)

            sectors   = pivot_count.index.tolist()
            buy_vals  = pivot_count["BUY"].tolist()
            hold_vals = pivot_count["HOLD"].tolist()
            sell_vals = pivot_count["SELL"].tolist()
            sent_vals = pivot_count["Sentiment"].tolist()

            # Max per column for opacity scaling
            max_buy  = max(buy_vals)  or 1
            max_hold = max(hold_vals) or 1
            max_sell = max(sell_vals) or 1

            # Build RGBA colours: fixed hue per column, opacity = count/max
            def rgba_green(count, mx):
                a = round(0.15 + 0.85 * count / mx, 2)
                return f"rgba(0,229,160,{a})"

            def rgba_amber(count, mx):
                a = round(0.15 + 0.85 * count / mx, 2)
                return f"rgba(240,165,0,{a})"

            def rgba_red(count, mx):
                a = round(0.15 + 0.85 * count / mx, 2)
                return f"rgba(255,77,109,{a})"

            def sentiment_color(s):
                # s in [-1, +1]  →  red at -1, amber at 0, green at +1
                if s >= 0.3:   return "rgba(0,229,160,0.85)"
                if s >= 0.05:  return "rgba(0,179,122,0.75)"
                if s >= -0.05: return "rgba(240,165,0,0.80)"
                if s >= -0.3:  return "rgba(255,136,68,0.80)"
                return "rgba(255,77,109,0.85)"

            # Build one subplot with 4 traces (BUY, HOLD, SELL, Sentiment)
            from plotly.subplots import make_subplots as _msp
            fig_hm = _msp(
                rows=1, cols=4,
                column_widths=[0.22, 0.32, 0.22, 0.24],
                horizontal_spacing=0.01,
                subplot_titles=["🟢 BUY", "🟡 HOLD", "🔴 SELL", "📊 Sentiment"],
            )

            common_yaxis = dict(
                tickfont=dict(size=11, color="#c0ccd8"),
                showgrid=False, zeroline=False,
            )
            common_xaxis = dict(
                showticklabels=False, showgrid=False, zeroline=False,
            )

            # ── BUY trace ──────────────────────────────────────────────────────
            fig_hm.add_trace(go.Heatmap(
                z=[[v] for v in buy_vals],
                y=sectors, x=["BUY"],
                text=[[str(v)] for v in buy_vals],
                texttemplate="<b>%{text}</b>",
                textfont=dict(size=13, color="#e0e6f0"),
                colorscale=[[0,"rgba(0,229,160,0.05)"],[1,"rgba(0,229,160,1)"]],
                zmin=0, zmax=max_buy,
                showscale=False,
                hovertemplate="<b>%{y}</b><br>BUY: %{z}<extra></extra>",
            ), row=1, col=1)

            # ── HOLD trace ─────────────────────────────────────────────────────
            fig_hm.add_trace(go.Heatmap(
                z=[[v] for v in hold_vals],
                y=sectors, x=["HOLD"],
                text=[[str(v)] for v in hold_vals],
                texttemplate="<b>%{text}</b>",
                textfont=dict(size=13, color="#e0e6f0"),
                colorscale=[[0,"rgba(240,165,0,0.05)"],[1,"rgba(240,165,0,1)"]],
                zmin=0, zmax=max_hold,
                showscale=False,
                hovertemplate="<b>%{y}</b><br>HOLD: %{z}<extra></extra>",
            ), row=1, col=2)

            # ── SELL trace ─────────────────────────────────────────────────────
            fig_hm.add_trace(go.Heatmap(
                z=[[v] for v in sell_vals],
                y=sectors, x=["SELL"],
                text=[[str(v)] for v in sell_vals],
                texttemplate="<b>%{text}</b>",
                textfont=dict(size=13, color="#e0e6f0"),
                colorscale=[[0,"rgba(255,77,109,0.05)"],[1,"rgba(255,77,109,1)"]],
                zmin=0, zmax=max_sell,
                showscale=False,
                hovertemplate="<b>%{y}</b><br>SELL: %{z}<extra></extra>",
            ), row=1, col=3)

            # ── Sentiment score trace (-1 to +1) ───────────────────────────────
            fig_hm.add_trace(go.Heatmap(
                z=[[v] for v in sent_vals],
                y=sectors, x=["Sentiment"],
                text=[[f"{v:+.2f}"] for v in sent_vals],
                texttemplate="<b>%{text}</b>",
                textfont=dict(size=12, color="#e0e6f0"),
                colorscale=[
                    [0.0,  "rgba(255,77,109,0.9)"],
                    [0.35, "rgba(255,136,68,0.7)"],
                    [0.5,  "rgba(240,165,0,0.6)"],
                    [0.65, "rgba(0,179,122,0.7)"],
                    [1.0,  "rgba(0,229,160,0.9)"],
                ],
                zmin=-1, zmax=1,
                showscale=True,
                colorbar=dict(
                    title=dict(text="Sentiment", font=dict(color="#8899aa", size=11)),
                    tickvals=[-1,-0.5,0,0.5,1],
                    ticktext=["All SELL","-0.5","Neutral","+0.5","All BUY"],
                    tickfont=dict(color="#8899aa", size=9),
                    len=0.8, thickness=12,
                    x=1.01,
                ),
                hovertemplate="<b>%{y}</b><br>Sentiment: %{z:.2f}<extra></extra>",
            ), row=1, col=4)

            # Shared layout
            n_sec = len(sectors)
            fig_hm.update_layout(
                height=max(320, n_sec * 40 + 100),
                paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623",
                font=dict(color="#e0e6f0", family="DM Sans"),
                margin=dict(l=10, r=60, t=50, b=10),
                showlegend=False,
            )
            # Y-axes: show labels only on col 1
            fig_hm.update_yaxes(showticklabels=True,  tickfont=dict(size=11,color="#c0ccd8"),
                                 showgrid=False, row=1, col=1)
            fig_hm.update_yaxes(showticklabels=False, showgrid=False, row=1, col=2)
            fig_hm.update_yaxes(showticklabels=False, showgrid=False, row=1, col=3)
            fig_hm.update_yaxes(showticklabels=False, showgrid=False, row=1, col=4)
            # X-axes: hide ticks (labels are subplot titles)
            for c in [1,2,3,4]:
                fig_hm.update_xaxes(showticklabels=False, showgrid=False, row=1, col=c)

            st.plotly_chart(fig_hm, use_container_width=True)

            # ── Bull ratio bar chart ──────────────────────────────────────────
            st.markdown("**📊 Sector Bull Ratio**  *(BUY signals as % of BUY+SELL)*")
            st.caption("100% = all BUY signals in sector · 0% = all SELL · 50% = balanced")

            br_df = pivot_count.reset_index()[["Sector","Bull Ratio","BUY","SELL","Avg Score","Total"]]
            br_df["Bull %"] = (br_df["Bull Ratio"] * 100).round(1)
            br_df = br_df.sort_values("Bull %", ascending=True)

            bar_colors = [
                "#00e5a0" if v >= 70 else
                ("#f0a500" if v >= 40 else "#ff4d6d")
                for v in br_df["Bull %"]
            ]

            fig_br = go.Figure(go.Bar(
                x=br_df["Bull %"], y=br_df["Sector"],
                orientation="h",
                marker_color=bar_colors,
                text=[f"{v}%  (↑{b} ↓{s}  n={t})"
                      for v,b,s,t in zip(br_df["Bull %"],
                                          br_df["BUY"],
                                          br_df["SELL"],
                                          br_df["Total"])],
                textposition="outside",
                textfont=dict(size=11, color="#8899aa"),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Bull Ratio: %{x:.1f}%<br>"
                    "<extra></extra>"
                ),
            ))
            fig_br.add_vline(x=50, line_dash="dash", line_color="#445566", line_width=1)
            fig_br.update_layout(
                height=max(280, len(br_df)*36 + 80),
                paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623",
                font=dict(color="#8899aa", family="DM Sans"),
                xaxis=dict(range=[0, 115], gridcolor="#1a2535",
                           title="Bull Ratio %", showgrid=True),
                yaxis=dict(gridcolor="#1a2535"),
                margin=dict(l=10, r=10, t=20, b=20),
            )
            st.plotly_chart(fig_br, use_container_width=True)

            # ── Sector summary table ──────────────────────────────────────────
            with st.expander("📋 Full sector breakdown table"):
                display_sec = pivot_count.reset_index()[
                    ["Sector","BUY","HOLD","SELL","Total","Sentiment","Bull Ratio","Avg Score"]
                ].sort_values("Sentiment", ascending=False)

                def hl_sent(v):
                    try:
                        x = float(v)
                        return ("color:#00e5a0;font-weight:bold" if x >= 0.3
                                else ("color:#00b37a" if x >= 0.05
                                else ("color:#f0a500" if x >= -0.05
                                else ("color:#ff8844" if x >= -0.3
                                else "color:#ff4d6d;font-weight:bold"))))
                    except: return ""

                st.dataframe(
                    display_sec.style
                    .map(hl_sent, subset=["Sentiment"])
                    .set_properties(**{"background-color":"#0f1623","border-color":"#1e3a5f"})
                    .format({"Sentiment":"{:+.2f}","Bull Ratio":"{:.0%}","Avg Score":"{:.1f}"}),
                    use_container_width=True, hide_index=True
                )

        st.caption("⚠️ Educational only. Not financial advice.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DEEP DIVE CHART  (stock picker is fully independent of data fetch)
# ─────────────────────────────────────────────────────────────────────────────
with tab_detail:
    st.markdown("### 📉 Deep Dive Chart")
    st.caption("Select any stock from the pulled universe. Chart renders instantly from cached data — no re-fetch.")

    if not all_scanned:
        st.info("No stock data is available yet. Pull universe data first.")
        st.stop()

    # Stock picker — only stocks already in universe
    if not all_scanned:
        st.warning("No stocks available. Please pull universe data first.")
        st.stop()
    
    detail_stock = st.selectbox(
        "Choose stock",
        options=all_scanned,
        index=0,
        key="detail_stock_picker",
    )

    if not detail_stock:
        st.warning("Please select a stock from the pulled universe.")
        st.stop()

    if detail_stock not in universe:
        st.session_state.pop("detail_stock_picker", None)
        st.warning("The selected stock is no longer available. Please refresh the data.")
        st.stop()

    try:
        r = universe.get(detail_stock)
        if r is None:
            raise KeyError(f"Stock {detail_stock} not found in universe")
    except KeyError as e:
        st.session_state.pop("detail_stock_picker", None)
        st.error(f"Stock data could not be loaded: {str(e)}")
        st.stop()

    df = r["df"].copy()
    f  = fundamentals.get(detail_stock,{})
    tk = STOCKS[detail_stock].replace(".NS","")

    # ── Valuation row ──────────────────────────────────────────────────────────
    if f:
        st.markdown("#### 💰 Valuation Ratios")
        def vc(label,value,color="#e0e6f0",suffix="",note=""):
            disp  = f"{value}{suffix}" if value is not None else "N/A"
            style = f"color:{color}" if value is not None else "color:#445566"
            return f"""<div class="val-card"><div class="val-label">{label}</div>
              <div class="val-value" style="{style}">{disp}</div>
              <div style="font-size:10px;color:#445566">{note}</div></div>"""
        pe_c ="#00e5a0" if f.get("pe") and f["pe"]<25 else("#ff4d6d" if f.get("pe") and f["pe"]>50 else "#f0a500")
        pb_c ="#00e5a0" if f.get("pb") and f["pb"]<3  else("#ff4d6d" if f.get("pb") and f["pb"]>10 else "#f0a500")
        roe_c="#00e5a0" if f.get("roe") and f["roe"]>15 else("#ff4d6d" if f.get("roe") and f["roe"]<8 else "#f0a500")
        de_c ="#00e5a0" if f.get("de") and f["de"]<50  else("#ff4d6d" if f.get("de") and f["de"]>150 else "#f0a500")
        dy_c ="#00e5a0" if f.get("dy") and f["dy"]>1.5 else "#8899aa"
        v1,v2,v3,v4,v5,v6,v7,v8 = st.columns(8)
        with v1: st.markdown(vc("P/E",f.get("pe"),pe_c,"","<25 cheap"),unsafe_allow_html=True)
        with v2: st.markdown(vc("P/B",f.get("pb"),pb_c,"","<3 cheap"),unsafe_allow_html=True)
        with v3: st.markdown(vc("ROE %",f.get("roe"),roe_c,"%",">15% good"),unsafe_allow_html=True)
        with v4: st.markdown(vc("D/E",f.get("de"),de_c,"","<50 safe"),unsafe_allow_html=True)
        with v5: st.markdown(vc("Div Yield",f.get("dy"),dy_c,"%",">1.5%"),unsafe_allow_html=True)
        with v6: st.markdown(vc("EV/EBITDA",f.get("ev_ebitda"),"#e0e6f0","x","<15 ok"),unsafe_allow_html=True)
        with v7: st.markdown(vc("PEG",f.get("peg"),"#e0e6f0","","<1 cheap"),unsafe_allow_html=True)
        with v8:
            mc=f.get("mcap_cr")
            st.markdown(vc("Mkt Cap",f"₹{int(mc):,}Cr" if mc else None,"#e0e6f0"),unsafe_allow_html=True)
        st.markdown(f"<span style='color:#667788;font-size:12px'>Sector: {f.get('sector','—')} · Industry: {f.get('industry','—')}</span>",unsafe_allow_html=True)

        # ── Analyst Consensus row ──────────────────────────────────────────────
        rec       = f.get("analyst_rec","—")
        n_an      = f.get("analyst_n")
        target    = f.get("analyst_target")
        upside    = f.get("analyst_upside")
        cur_close = r.get("close")

        rec_color = ("#00e5a0" if "Strong Buy" in str(rec) else
                     "#00b37a"  if "Buy"        in str(rec) else
                     "#f0a500"  if "Hold"       in str(rec) else
                     "#ff8844"  if "Underperform" in str(rec) else
                     "#ff4d6d"  if "Sell"       in str(rec) else "#8899aa")
        up_color  = ("#00e5a0" if upside and upside>=15 else
                     "#00b37a"  if upside and upside>=5  else
                     "#f0a500"  if upside and upside>=0  else
                     "#ff4d6d"  if upside                else "#8899aa")

        st.markdown(f"""
        <div class="metric-card" style="margin-top:8px;border-left:4px solid {rec_color}">
          <span style="font-size:11px;color:#8899aa;text-transform:uppercase;letter-spacing:1px">
            🏦 Analyst Consensus · {f'{n_an} analysts' if n_an else 'coverage unknown'}
          </span><br/>
          <span style="font-family:'Space Mono';font-size:1.3rem;color:{rec_color}">{rec}</span>
          &nbsp;&nbsp;
          <span style="font-size:13px;color:#8899aa">
            Target: <b style="color:#e0e6f0">{'₹'+str(target) if target else 'N/A'}</b>
            &nbsp;·&nbsp;
            Upside: <b style="color:{up_color}">{('+'+str(upside)+'%') if upside is not None else 'N/A'}</b>
            &nbsp;·&nbsp;
            Current: <b style="color:#e0e6f0">{'₹'+str(cur_close) if cur_close else 'N/A'}</b>
          </span>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")

    # ── Score breakdown ────────────────────────────────────────────────────────
    st.markdown("#### ⭐ Technical Score")
    sig=r["signal"]; sc={"BUY":"#00e5a0","SELL":"#ff4d6d","HOLD":"#f0a500"}[sig]
    left,right=st.columns([2,1])
    with left:
        pct=int(r["tech_score"]*10)
        st.markdown(f"""<div class="metric-card" style="border-color:{sc}">
          <span style="font-family:'Space Mono';font-size:2rem;color:{sc}">{r['tech_score']}
          <span style="font-size:1rem;color:#8899aa">/ 10</span></span>
          &nbsp;&nbsp;<span style="color:{sc};font-size:1.2rem;font-family:'Space Mono'">▶ {sig}</span>
          <div class="score-bar-wrap"><div style="width:{pct}%;background:{sc};height:8px;border-radius:8px;"></div></div><br/>
          <span style="font-size:12px;color:#8899aa">
            RSI:{r['rsi']} · ADX:{r['adx']} · OBV:{r['obv_trend']} · BB%B:{r['bb_pctb']} · VolSpike:{'⚡' if r['vol_spike'] else 'No'}<br/>
            Support:₹{r['support']} · Resistance:₹{r['resistance']} · MA50:{r['ma50']} · MA200:{r['ma200']}
          </span></div>""",unsafe_allow_html=True)
    with right:
        lbl={"RSI":"RSI","MACD":"MACD","MA":"MA Cross","BB":"Bollinger","ADX":"ADX","OBV":"OBV","Vol":"Volume","SR":"S/R"}
        for k,v in r["scores"].items():
            bc="#00e5a0" if v>0 else("#ff4d6d" if v<0 else "#334455")
            icon="▲" if v>0 else("▼" if v<0 else "→")
            st.markdown(f"""<div style="display:flex;justify-content:space-between;margin:4px 0;font-size:13px">
              <span style="color:#8899aa">{lbl.get(k,k)}</span>
              <span style="color:{bc};font-family:'Space Mono'">{icon} {v:+.1f}</span></div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"#### 📈 {detail_stock} ({tk})")

    # 5-panel chart
    fig=make_subplots(rows=5,cols=1,shared_xaxes=True,vertical_spacing=0.03,
        row_heights=[0.38,0.15,0.15,0.17,0.15],
        subplot_titles=("Price · Bollinger · MAs · S/R","MACD","RSI","ADX + DI","OBV"))

    fig.add_trace(go.Candlestick(x=df.index,open=df["Open"],high=df["High"],low=df["Low"],close=df["Close"],
        increasing_line_color="#00e5a0",decreasing_line_color="#ff4d6d",name="Price"),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["BBU"],name="BB Upper",line=dict(color="#7b61ff",width=1,dash="dot")),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["BBL"],name="BB Lower",line=dict(color="#7b61ff",width=1,dash="dot"),fill="tonexty",fillcolor="rgba(123,97,255,0.06)",showlegend=False),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["BBM"],name="BB Mid",line=dict(color="#7b61ff",width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MA50"],name="MA50",line=dict(color="#f0a500",width=1.5)),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MA200"],name="MA200",line=dict(color="#ff9966",width=1.5)),row=1,col=1)
    if r["support"]:    fig.add_hline(y=r["support"],   line_dash="dot",line_color="#00e5a0",annotation_text=f"S ₹{r['support']}",   row=1,col=1)
    if r["resistance"]: fig.add_hline(y=r["resistance"],line_dash="dot",line_color="#ff4d6d",annotation_text=f"R ₹{r['resistance']}",row=1,col=1)
    ch=["#00e5a0" if v>=0 else "#ff4d6d" for v in df["MACD_H"].fillna(0)]
    fig.add_trace(go.Bar(x=df.index,y=df["MACD_H"],name="Hist",marker_color=ch,opacity=0.6),row=2,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MACD"],name="MACD",line=dict(color="#00cfff",width=1.5)),row=2,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MACD_S"],name="MACD Sig",line=dict(color="#ff9966",width=1.5)),row=2,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["RSI"],name="RSI",line=dict(color="#d4a0ff",width=1.5)),row=3,col=1)
    fig.add_hline(y=70,line_dash="dash",line_color="#ff4d6d",line_width=1,row=3,col=1)
    fig.add_hline(y=30,line_dash="dash",line_color="#00e5a0",line_width=1,row=3,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["ADX"],name="ADX",line=dict(color="#f0a500",width=2)),row=4,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["PDI"],name="+DI",line=dict(color="#00e5a0",width=1.2)),row=4,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MDI"],name="−DI",line=dict(color="#ff4d6d",width=1.2)),row=4,col=1)
    fig.add_hline(y=25,line_dash="dash",line_color="#aaaaaa",line_width=1,row=4,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["OBV"],name="OBV",line=dict(color="#00cfff",width=1.5)),row=5,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["OBVMA"],name="OBV MA20",line=dict(color="#f0a500",width=1,dash="dot")),row=5,col=1)

    fig.update_layout(height=950,paper_bgcolor="#0a0e1a",plot_bgcolor="#0f1623",
        font=dict(color="#8899aa",family="DM Sans"),xaxis_rangeslider_visible=False,
        legend=dict(orientation="h",yanchor="bottom",y=1.01,xanchor="right",x=1,
                    bgcolor="rgba(0,0,0,0)",font=dict(size=10)),
        margin=dict(l=10,r=10,t=40,b=10),hovermode="x unified")
    fig.update_xaxes(gridcolor="#1a2535",showgrid=True)
    fig.update_yaxes(gridcolor="#1a2535",showgrid=True)
    st.plotly_chart(fig,use_container_width=True)
    st.caption("⚠️ Educational only. Not financial advice.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ASSET ALLOCATION  (all sliders / pickers are fully independent)
# ── Multi-asset instrument definitions ────────────────────────────────────────
FIXED_INCOME_INSTRUMENTS = {
    "LIQUIDBEES (Short-term G-Sec)": {
        "ticker":   "LIQUIDBEES.NS",
        "duration": "Short",
        "desc":     "Nippon Liquid BeES — overnight/short-term government securities",
        "asset_class": "Fixed Income",
    },
    "GSEC10YBEES (10Y G-Sec ETF)": {
        "ticker":   "GSEC10YBEES.NS",
        "duration": "Long",
        "desc":     "Nippon 10-Year G-Sec ETF — benchmark government bond",
        "asset_class": "Fixed Income",
    },
}

COMMODITY_INSTRUMENTS = {
    "GOLDBEES (Gold ETF)": {
        "ticker":   "GOLDBEES.NS",
        "desc":     "Nippon Gold BeES — tracks domestic MCX gold price",
        "asset_class": "Gold",
    },
    "SILVERBEES (Silver ETF)": {
        "ticker":   "SILVERBEES.NS",
        "desc":     "Nippon Silver ETF — tracks domestic MCX silver price",
        "asset_class": "Silver",
    },
}

@st.cache_data(ttl=300)
def fetch_instrument_data(ticker):
    """Fetch price + basic info for a non-equity instrument (ETF)."""
    try:
        df = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
        if df.empty: return None, None
        df.columns = [c[0] if isinstance(c,tuple) else c for c in df.columns]
        info  = yf.Ticker(ticker).info
        price = round(float(df["Close"].iloc[-1]), 2)
        prev  = round(float(df["Close"].iloc[-2]), 2)
        chg   = round((price - prev) / prev * 100, 2)
        # 6-month return
        ret6m = round((price - float(df["Close"].iloc[0])) / float(df["Close"].iloc[0]) * 100, 1)
        # Annualised volatility
        vol   = round(df["Close"].pct_change().dropna().std() * (252**0.5) * 100, 1)
        return {
            "price":   price,
            "change":  chg,
            "ret_6m":  ret6m,
            "vol_ann": vol,
            "name":    info.get("longName", ticker),
        }, df
    except:
        return None, None

# ─────────────────────────────────────────────────────────────────────────────
with tab_alloc:
    st.markdown("## 🗂️ Multi-Asset Portfolio Builder")
    st.caption("Build a portfolio across Equities · Fixed Income · Gold · Silver. All decisions are instant — no re-fetching.")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 0 — ASSET CLASS WEIGHTS  (top-level split)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### Step 0 — Asset Class Weights  *(must sum to 100%)*")
    st.caption("Set the top-level allocation across all asset classes first.")

    ac1,ac2,ac3,ac4,ac5 = st.columns(5)
    with ac1:
        st.markdown('<div class="alloc-bucket"><b style="color:#00cfff">📈 India Equities</b><br/><span style="font-size:11px;color:#8899aa">Nifty 500 stocks</span></div>',unsafe_allow_html=True)
        w_eq = st.slider("India Equities %", 0, 100, 55, 5, key="w_eq")
    with ac2:
        st.markdown('<div class="alloc-bucket"><b style="color:#00e5a0">🏦 Fixed Income</b><br/><span style="font-size:11px;color:#8899aa">G-Sec / Bond ETFs</span></div>',unsafe_allow_html=True)
        w_fi = st.slider("Fixed Income %",   0, 100, 20, 5, key="w_fi")
    with ac3:
        st.markdown('<div class="alloc-bucket"><b style="color:#f0a500">🥇 Gold</b><br/><span style="font-size:11px;color:#8899aa">MCX Gold ETF</span></div>',unsafe_allow_html=True)
        w_gd = st.slider("Gold %",           0, 100, 10, 5, key="w_gd")
    with ac4:
        st.markdown('<div class="alloc-bucket"><b style="color:#d4a0ff">🥈 Silver</b><br/><span style="font-size:11px;color:#8899aa">MCX Silver ETF</span></div>',unsafe_allow_html=True)
        w_sv = st.slider("Silver %",         0, 100,  5, 5, key="w_sv")
    with ac5:
        st.markdown('<div class="alloc-bucket"><b style="color:#ff9966">🌍 Global</b><br/><span style="font-size:11px;color:#8899aa">US / APAC / Oil / Defense</span></div>',unsafe_allow_html=True)
        w_gl = st.slider("Global %",         0, 100, 10, 5, key="w_gl")

    ac_sum = w_eq + w_fi + w_gd + w_sv + w_gl
    (st.success if ac_sum==100 else st.warning)(
        f"Asset class weights: **{ac_sum}%** {'✅' if ac_sum==100 else '— must equal 100%'}")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 1 — FIXED INCOME SPLIT
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### Step 1 — Fixed Income Split  *(must sum to 100%)*")
    st.caption("Split your Fixed Income allocation across short and long duration.")

    fi1, fi2 = st.columns(2)
    with fi1:
        st.markdown(f"**💵 LIQUIDBEES** — {FIXED_INCOME_INSTRUMENTS['LIQUIDBEES (Short-term G-Sec)']['desc']}")
        w_liquid = st.slider("LIQUIDBEES %", 0, 100, 50, 10, key="w_liquid")
    with fi2:
        st.markdown(f"**📜 GSEC10YBEES** — {FIXED_INCOME_INSTRUMENTS['GSEC10YBEES (10Y G-Sec ETF)']['desc']}")
        w_gsec10 = st.slider("GSEC10YBEES %", 0, 100, 50, 10, key="w_gsec10")

    fi_sum = w_liquid + w_gsec10
    (st.success if fi_sum==100 else st.warning)(
        f"Fixed Income split: **{fi_sum}%** {'✅' if fi_sum==100 else '— must equal 100%'}")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 2 — EQUITY: STOCK SELECTION METHOD
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### Step 2 — Equity: Stock Selection Method")
    method = st.radio("How should stocks be selected within each equity bucket?",
        ["1️⃣  Top N by Technical Score",
         "2️⃣  BUY-signal stocks only (equal weight)",
         "3️⃣  Manual Picker"],
        horizontal=False, key="alloc_method")
    method_key = method[0]
    top_n = st.slider("Top N per bucket", 1, 10, 3, key="alloc_topn") if method_key=="1" else 5
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 3 — EQUITY STYLE WEIGHTS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### Step 3 — Equity Style Weights  *(must sum to 100%)*")
    s1,s2,s3,s4 = st.columns(4)
    with s1:
        st.markdown('<div class="alloc-bucket"><b style="color:#00cfff">📈 Growth</b><br/><span style="font-size:11px;color:#8899aa">High ROE · expanding revenue</span></div>',unsafe_allow_html=True)
        w_gr = st.slider("Growth %",   0, 100, 40, 5, key="w_gr")
    with s2:
        st.markdown('<div class="alloc-bucket"><b style="color:#f0a500">💰 Value</b><br/><span style="font-size:11px;color:#8899aa">Low P/E · Low P/B</span></div>',unsafe_allow_html=True)
        w_va = st.slider("Value %",    0, 100, 25, 5, key="w_va")
    with s3:
        st.markdown('<div class="alloc-bucket"><b style="color:#00e5a0">🏦 Dividend</b><br/><span style="font-size:11px;color:#8899aa">High yield · stable cash flows</span></div>',unsafe_allow_html=True)
        w_di = st.slider("Dividend %", 0, 100, 20, 5, key="w_di")
    with s4:
        st.markdown('<div class="alloc-bucket"><b style="color:#d4a0ff">⚡ Momentum</b><br/><span style="font-size:11px;color:#8899aa">High score · BUY signal · ADX>25</span></div>',unsafe_allow_html=True)
        w_mo = st.slider("Momentum %", 0, 100, 15, 5, key="w_mo")

    style_sum = w_gr + w_va + w_di + w_mo
    (st.success if style_sum==100 else st.warning)(
        f"Style weights: **{style_sum}%** {'✅' if style_sum==100 else '— must equal 100%'}")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 4 — SECTOR CONSTRAINTS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### Step 4 — Sector Constraints *(optional)*")
    use_sec = st.checkbox("Apply max sector exposure", value=False, key="use_sec")
    sec_max = {}
    if use_sec:
        scols = st.columns(4)
        for i,sec in enumerate(SECTORS_ALL):
            with scols[i%4]:
                sec_max[sec] = st.slider(f"{sec} max %", 0, 50, 30, 5, key=f"secmax_{sec}")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 5 — MARKET CAP WEIGHTS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("### Step 5 — Market Cap Weights  *(must sum to 100%)*")
    ca,cb,cc_ = st.columns(3)
    with ca:  w_lg = st.slider("Large Cap %", 0, 100, 60, 5, key="w_lg"); st.caption("Mkt Cap > ₹20,000 Cr")
    with cb:  w_md = st.slider("Mid Cap %",   0, 100, 30, 5, key="w_md"); st.caption("₹5,000 – ₹20,000 Cr")
    with cc_: w_sm = st.slider("Small Cap %", 0, 100, 10, 5, key="w_sm"); st.caption("< ₹5,000 Cr")

    cap_sum = w_lg + w_md + w_sm
    (st.success if cap_sum==100 else st.warning)(
        f"Cap weights: **{cap_sum}%** {'✅' if cap_sum==100 else '— must equal 100%'}")
    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 6 — MANUAL PICKER (method 3 only)
    # ══════════════════════════════════════════════════════════════════════════
    manual_picks = {}
    if method_key=="3":
        st.markdown("### Step 6 — Manual Stock Picker")
        p1,p2,p3,p4 = st.columns(4)
        with p1: st.markdown("**📈 Growth**");   manual_picks["Growth"]   = st.multiselect("Growth",   all_scanned,key="mp_gr")
        with p2: st.markdown("**💰 Value**");    manual_picks["Value"]    = st.multiselect("Value",    all_scanned,key="mp_va")
        with p3: st.markdown("**🏦 Dividend**"); manual_picks["Dividend"] = st.multiselect("Dividend", all_scanned,key="mp_di")
        with p4: st.markdown("**⚡ Momentum**"); manual_picks["Momentum"] = st.multiselect("Momentum", all_scanned,key="mp_mo")
        st.markdown("---")

    # ── Build button ───────────────────────────────────────────────────────────
    build_btn = st.button("🏗️ Build Portfolio", type="primary", key="build_port")

    if build_btn:
        # Validate
        errors = []
        if ac_sum    != 100: errors.append("Asset class weights must sum to 100% (check Global % in Step 0).")
        if fi_sum    != 100: errors.append("Fixed Income split must sum to 100%.")
        if style_sum != 100: errors.append("Equity style weights must sum to 100%.")
        if cap_sum   != 100: errors.append("Market cap weights must sum to 100%.")
        if errors:
            for e in errors: st.error(e)
        else:
            port_rows = []

            # ── A) EQUITIES ─────────────────────────────────────────────────
            style_wts = {"Growth":w_gr,"Value":w_va,"Dividend":w_di,"Momentum":w_mo}
            cap_wts   = {"Large Cap":w_lg,"Mid Cap":w_md,"Small Cap":w_sm}

            candidates = []
            for name, r in universe.items():
                f   = fundamentals.get(name,{})
                cap = classify_cap(f.get("mcap_cr"))
                candidates.append({"name":name,"ticker":STOCKS[name],"r":r,"f":f,
                                    "cap":cap,"sector":f.get("sector","Unknown")})

            for style, sw in style_wts.items():
                if sw == 0: continue
                for cap_label, cw in cap_wts.items():
                    if cw == 0: continue
                    # Weight of this bucket as fraction of TOTAL portfolio
                    bw = round(w_eq/100 * sw/100 * cw/100, 6)
                    if bw < 1e-5: continue

                    if method_key == "3":
                        pool = [c for c in candidates if c["name"] in manual_picks.get(style,[]) and c["cap"]==cap_label]
                    elif method_key == "2":
                        pool = [c for c in candidates if c["cap"]==cap_label and c["r"]["signal"]=="BUY"]
                    else:
                        pool = [c for c in candidates if c["cap"]==cap_label]

                    if use_sec and sec_max:
                        pool = [c for c in pool if sec_max.get(c["sector"],30)>0]
                    if not pool:
                        pool = [c for c in candidates if c["cap"]==cap_label]
                    if not pool: continue

                    pool = sorted(pool, key=lambda c: style_score(c["r"],c["f"],style), reverse=True)
                    sel  = pool[:top_n] if method_key=="1" else pool
                    if not sel: continue

                    psw = round(bw / len(sel), 6)
                    for c in sel:
                        r = c["r"]; f = c["f"]

                        # Inclusion reason
                        reasons = []
                        if method_key=="1":
                            reasons.append(f"Top {top_n} by Tech Score ({r['tech_score']}/10) in {style}·{cap_label}")
                        elif method_key=="2":
                            reasons.append(f"BUY signal — {style}·{cap_label}")
                        else:
                            reasons.append(f"Manual pick — {style}·{cap_label}")

                        if style=="Growth":
                            d=[]
                            if r.get("tech_score") and r["tech_score"]>=6: d.append(f"Score {r['tech_score']}")
                            if f.get("roe") and f["roe"]>15: d.append(f"ROE {f['roe']}%")
                            if f.get("pe")  and f["pe"]<40:  d.append(f"P/E {f['pe']:.1f}")
                            if d: reasons.append("Growth: "+" · ".join(d))
                        elif style=="Value":
                            d=[]
                            if f.get("pe") and f["pe"]<20: d.append(f"Low P/E {f['pe']:.1f}")
                            if f.get("pb") and f["pb"]<2:  d.append(f"Low P/B {f['pb']:.2f}")
                            if d: reasons.append("Value: "+" · ".join(d))
                        elif style=="Dividend":
                            d=[]
                            if f.get("dy") and f["dy"]>0: d.append(f"Yield {f['dy']}%")
                            if d: reasons.append("Dividend: "+" · ".join(d))
                        elif style=="Momentum":
                            d=[]
                            if r.get("tech_score"): d.append(f"Score {r['tech_score']}/10")
                            if r.get("signal")=="BUY": d.append("BUY signal")
                            if r.get("adx") and r["adx"]>25: d.append(f"ADX {r['adx']}")
                            if d: reasons.append("Momentum: "+" · ".join(d))

                        top_signals = sorted([(k,v) for k,v in r.get("scores",{}).items() if v>0],
                                             key=lambda x:x[1],reverse=True)[:3]
                        sig_labels  = {"RSI":"RSI oversold","MACD":"MACD crossover","MA":"MA crossover",
                                       "BB":"Near BB lower band","ADX":"Strong ADX","OBV":"OBV rising",
                                       "Vol":"Vol spike","SR":"Near support"}
                        if top_signals:
                            reasons.append("Signals: "+" · ".join(sig_labels.get(k,k) for k,_ in top_signals))

                        port_rows.append({
                            "Stock":            c["name"],
                            "Ticker":           c["ticker"].replace(".NS",""),
                            "Asset Class":      "Equities",
                            "Style":            style,
                            "Cap":              c["cap"],
                            "Sector":           c["sector"],
                            "Signal":           r["signal"],
                            "Tech Score":       r["tech_score"],
                            "Price (₹)":        r["close"],
                            "Alloc %":          round(psw*100, 4),
                            "6M Return %":      None,
                            "Ann. Vol %":       None,
                            "P/E":              f.get("pe"),
                            "P/B":              f.get("pb"),
                            "ROE %":            f.get("roe"),
                            "Div Yield %":      f.get("dy"),
                            "Inclusion Reason": " | ".join(reasons),
                            "_full":            c["ticker"],
                        })

            # ── B) FIXED INCOME ─────────────────────────────────────────────
            if w_fi > 0:
                fi_allocs = {
                    "LIQUIDBEES (Short-term G-Sec)":  w_liquid / 100,
                    "GSEC10YBEES (10Y G-Sec ETF)":    w_gsec10 / 100,
                }
                for inst_name, fi_split in fi_allocs.items():
                    if fi_split <= 0: continue
                    inst    = FIXED_INCOME_INSTRUMENTS[inst_name]
                    alloc_w = round(w_fi / 100 * fi_split * 100, 4)
                    data, _ = fetch_instrument_data(inst["ticker"])
                    price   = data["price"]   if data else None
                    ret6m   = data["ret_6m"]  if data else None
                    vol     = data["vol_ann"] if data else None
                    port_rows.append({
                        "Stock":            inst_name,
                        "Ticker":           inst["ticker"].replace(".NS",""),
                        "Asset Class":      "Fixed Income",
                        "Style":            inst["duration"] + " Duration",
                        "Cap":              "—",
                        "Sector":           "Government Securities",
                        "Signal":           "—",
                        "Tech Score":       None,
                        "Price (₹)":        price,
                        "Alloc %":          alloc_w,
                        "6M Return %":      ret6m,
                        "Ann. Vol %":       vol,
                        "P/E":              None,
                        "P/B":              None,
                        "ROE %":            None,
                        "Div Yield %":      None,
                        "Inclusion Reason": f"Fixed Income {inst['duration']} duration | {inst['desc']} | Weight: {w_fi}% × {round(fi_split*100)}%",
                        "_full":            inst["ticker"],
                    })

            # ── C) GOLD ─────────────────────────────────────────────────────
            if w_gd > 0:
                inst     = COMMODITY_INSTRUMENTS["GOLDBEES (Gold ETF)"]
                data, _  = fetch_instrument_data(inst["ticker"])
                port_rows.append({
                    "Stock":            "GOLDBEES (Gold ETF)",
                    "Ticker":           "GOLDBEES",
                    "Asset Class":      "Gold",
                    "Style":            "Commodity",
                    "Cap":              "—",
                    "Sector":           "Precious Metals",
                    "Signal":           "—",
                    "Tech Score":       None,
                    "Price (₹)":        data["price"]   if data else None,
                    "Alloc %":          float(w_gd),
                    "6M Return %":      data["ret_6m"]  if data else None,
                    "Ann. Vol %":       data["vol_ann"] if data else None,
                    "P/E":              None,"P/B":None,"ROE %":None,"Div Yield %":None,
                    "Inclusion Reason": f"Gold hedge | {inst['desc']} | Asset class weight: {w_gd}%",
                    "_full":            inst["ticker"],
                })

            # ── D) SILVER ───────────────────────────────────────────────────
            if w_sv > 0:
                inst     = COMMODITY_INSTRUMENTS["SILVERBEES (Silver ETF)"]
                data, _  = fetch_instrument_data(inst["ticker"])
                port_rows.append({
                    "Stock":            "SILVERBEES (Silver ETF)",
                    "Ticker":           "SILVERBEES",
                    "Asset Class":      "Silver",
                    "Style":            "Commodity",
                    "Cap":              "—",
                    "Sector":           "Precious Metals",
                    "Signal":           "—",
                    "Tech Score":       None,
                    "Price (₹)":        data["price"]   if data else None,
                    "Alloc %":          float(w_sv),
                    "6M Return %":      data["ret_6m"]  if data else None,
                    "Ann. Vol %":       data["vol_ann"] if data else None,
                    "P/E":              None,"P/B":None,"ROE %":None,"Div Yield %":None,
                    "Inclusion Reason": f"Silver exposure | {inst['desc']} | Asset class weight: {w_sv}%",
                    "_full":            inst["ticker"],
                })

            if not port_rows:
                st.error("No holdings generated. Check your settings.")
            else:
                pdf = pd.DataFrame(port_rows)

                # Normalise equity weights to their correct proportion, keeping FI/Gold/Silver fixed
                eq_rows  = pdf["Asset Class"] == "Equities"
                eq_total = pdf.loc[eq_rows,"Alloc %"].sum()
                if eq_total > 0 and w_eq > 0:
                    pdf.loc[eq_rows,"Alloc %"] = (pdf.loc[eq_rows,"Alloc %"] / eq_total * w_eq).round(4)

                # Deduplicate equity stocks that appear across multiple buckets
                def join_unique(s): return " · ".join(sorted(set(str(x) for x in s if pd.notna(x) and str(x)!="None")))

                eq_pdf   = pdf[eq_rows].copy()
                non_eq   = pdf[~eq_rows].copy()

                if not eq_pdf.empty:
                    eq_agg = (eq_pdf.groupby(["Stock","Ticker","_full"],as_index=False)
                              .agg({
                                  "Alloc %":          "sum",
                                  "Tech Score":       "mean",
                                  "Price (₹)":        "first",
                                  "Signal":           "first",
                                  "Asset Class":      "first",
                                  "Style":            join_unique,
                                  "Cap":              "first",
                                  "Sector":           "first",
                                  "P/E":              "first",
                                  "P/B":              "first",
                                  "ROE %":            "first",
                                  "Div Yield %":      "first",
                                  "6M Return %":      "first",
                                  "Ann. Vol %":       "first",
                                  "Inclusion Reason": join_unique,
                              }))
                    eq_agg["Tech Score"] = eq_agg["Tech Score"].round(1)
                    pagg = pd.concat([eq_agg, non_eq], ignore_index=True)
                else:
                    pagg = non_eq.copy()

                pagg["Alloc %"] = pagg["Alloc %"].round(2)
                pagg = pagg.sort_values(["Asset Class","Alloc %"],ascending=[True,False]).reset_index(drop=True)

                st.session_state["portfolio_pagg"] = pagg
                st.session_state["portfolio_pdf"]  = pdf
                st.session_state["portfolio_meta"] = {
                    "w_eq":w_eq,"w_fi":w_fi,"w_gd":w_gd,"w_sv":w_sv,"w_gl":w_gl,
                    "w_gr":w_gr,"w_va":w_va,"w_di":w_di,"w_mo":w_mo,
                    "w_lg":w_lg,"w_md":w_md,"w_sm":w_sm,
                    "w_liquid":w_liquid,"w_gsec10":w_gsec10,
                    "method_key":method_key,
                }

    # ── Render portfolio output — reads from session state, always visible ──────
    if "portfolio_pagg" in st.session_state:
        pagg = st.session_state["portfolio_pagg"]
        pdf  = st.session_state["portfolio_pdf"]
        meta = st.session_state["portfolio_meta"]

        st.markdown("---")
        st.markdown("### 🏆 Portfolio Summary")

        # Per asset class totals
        ac_totals = pagg.groupby("Asset Class")["Alloc %"].sum().to_dict()
        eq_stocks = len(pagg[pagg["Asset Class"]=="Equities"])
        ts        = len(pagg)
        avg_ts    = round(pagg["Tech Score"].dropna().mean(), 1) if not pagg["Tech Score"].dropna().empty else "—"
        bp        = (pagg["Signal"]=="BUY").sum()
        ap        = round(pagg["P/E"].dropna().mean(),1)   if not pagg["P/E"].dropna().empty   else None
        ar        = round(pagg["ROE %"].dropna().mean(),1) if not pagg["ROE %"].dropna().empty else None

        pm1,pm2,pm3,pm4,pm5,pm6,pm7 = st.columns(7)
        pm1.metric("📋 Holdings",     ts)
        pm2.metric("📈 Equities",     f"{ac_totals.get('Equities',0):.1f}%",  f"{eq_stocks} stocks")
        pm3.metric("🏦 Fixed Income", f"{ac_totals.get('Fixed Income',0):.1f}%")
        pm4.metric("🥇 Gold",         f"{ac_totals.get('Gold',0):.1f}%")
        pm5.metric("🥈 Silver",       f"{ac_totals.get('Silver',0):.1f}%")
        pm6.metric("⭐ Avg Eq Score", f"{avg_ts}/10")
        pm7.metric("🟢 BUY signals",  bp)
        st.markdown("---")

        # Holdings table
        st.markdown("### 📋 Holdings")
        col_order = [
            "Asset Class","Stock","Ticker","Style","Cap","Sector",
            "Signal","Tech Score","Alloc %","Price (₹)",
            "6M Return %","Ann. Vol %",
            "P/E","P/B","ROE %","Div Yield %",
            "Inclusion Reason",
        ]
        disp = pagg[[c for c in col_order if c in pagg.columns]]

        def hl_ac(v):
            return {"Equities":"color:#00cfff","Fixed Income":"color:#00e5a0",
                    "Gold":"color:#f0a500","Silver":"color:#d4a0ff"}.get(v,"")
        def hl_s(v):
            return {"BUY":"color:#00e5a0;font-weight:bold","SELL":"color:#ff4d6d;font-weight:bold"}.get(v,"color:#f0a500")
        def hl_a(v):
            try:
                x = float(v)
                return "color:#00e5a0;font-weight:bold" if x>=5 else ("color:#e0e6f0" if x>=2 else "color:#8899aa")
            except: return ""
        def hl_ret(v):
            try:
                x = float(v)
                return f"color:{'#00e5a0' if x>0 else '#ff4d6d'}"
            except: return ""

        ps = (disp.style
              .map(hl_ac, subset=["Asset Class"])
              .map(hl_s,  subset=["Signal"])
              .map(hl_a,  subset=["Alloc %"])
              .map(hl_ret,subset=["6M Return %"])
              .set_properties(**{"background-color":"#0f1623","border-color":"#1e3a5f"})
              .format({"Alloc %":"{:.2f}%","Tech Score":"{:.1f}","P/E":"{:.1f}",
                       "P/B":"{:.2f}","ROE %":"{:.1f}","Div Yield %":"{:.2f}",
                       "6M Return %":"{:.1f}%","Ann. Vol %":"{:.1f}%"},na_rep="—")
              .bar(subset=["Alloc %"],color=["#1a3a2a","#00e5a0"]))
        st.dataframe(ps, use_container_width=True, hide_index=True)
        st.markdown("---")

        # Breakdown charts — 4 charts for multi-asset
        st.markdown("### 📊 Allocation Breakdown")
        ch1,ch2,ch3,ch4 = st.columns(4)

        with ch1:
            # By Asset Class
            ac_s = pagg.groupby("Asset Class")["Alloc %"].sum().reset_index()
            fig_ac = px.pie(ac_s,names="Asset Class",values="Alloc %",
                title="By Asset Class",hole=0.45,
                color_discrete_map={"Equities":"#00cfff","Fixed Income":"#00e5a0",
                                    "Gold":"#f0a500","Silver":"#d4a0ff"})
            fig_ac.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0a0e1a",
                font=dict(color="#e0e6f0",family="DM Sans"),
                legend=dict(bgcolor="rgba(0,0,0,0)"),margin=dict(t=40,b=10,l=5,r=5))
            st.plotly_chart(fig_ac,use_container_width=True)

        with ch2:
            # By Style (equities only)
            eq_only = pdf[pdf["Asset Class"]=="Equities"]
            if not eq_only.empty:
                ss = eq_only.groupby("Style")["Alloc %"].sum().reset_index()
                fig_s = px.pie(ss,names="Style",values="Alloc %",
                    title="Equity by Style",hole=0.45,
                    color_discrete_map={"Growth":"#00cfff","Value":"#f0a500",
                                        "Dividend":"#00e5a0","Momentum":"#d4a0ff"})
                fig_s.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0a0e1a",
                    font=dict(color="#e0e6f0",family="DM Sans"),
                    legend=dict(bgcolor="rgba(0,0,0,0)"),margin=dict(t=40,b=10,l=5,r=5))
                st.plotly_chart(fig_s,use_container_width=True)

        with ch3:
            # By Cap (equities only)
            if not eq_only.empty:
                cap_s = eq_only.groupby("Cap")["Alloc %"].sum().reset_index()
                fig_c = px.pie(cap_s,names="Cap",values="Alloc %",
                    title="Equity by Market Cap",hole=0.45,
                    color_discrete_map={"Large Cap":"#00cfff","Mid Cap":"#f0a500",
                                        "Small Cap":"#d4a0ff","Unknown":"#445566"})
                fig_c.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0a0e1a",
                    font=dict(color="#e0e6f0",family="DM Sans"),
                    legend=dict(bgcolor="rgba(0,0,0,0)"),margin=dict(t=40,b=10,l=5,r=5))
                st.plotly_chart(fig_c,use_container_width=True)

        with ch4:
            # Top sectors (equities only)
            if not eq_only.empty:
                sec_s = pagg[pagg["Asset Class"]=="Equities"].groupby("Sector")["Alloc %"].sum().nlargest(7).reset_index()
                fig_sec = px.bar(sec_s,x="Alloc %",y="Sector",orientation="h",
                    title="Top Equity Sectors",color="Alloc %",
                    color_continuous_scale=["#1a3a5f","#00cfff"])
                fig_sec.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0f1623",
                    font=dict(color="#e0e6f0",family="DM Sans"),
                    coloraxis_showscale=False,margin=dict(t=40,b=10,l=5,r=5))
                st.plotly_chart(fig_sec,use_container_width=True)

        st.markdown("---")

        # Correlation heatmap
        st.markdown("### 🔗 Correlation Heatmap")
        st.caption("Includes equities + fixed income ETFs + gold + silver. Lower correlation = better diversification.")
        tickers_t = tuple(pagg["_full"].tolist())
        with st.spinner("Computing correlations…"):
            ph = fetch_corr_prices(tickers_t, pulled_period)

        if not ph.empty and ph.shape[1] >= 2:
            corr = ph.pct_change().dropna().corr()
            # Label columns with short names
            inst_map = {v["ticker"]:k for k,v in {**FIXED_INCOME_INSTRUMENTS,**COMMODITY_INSTRUMENTS}.items()}
            t2n = {v:k for k,v in STOCKS.items()}
            def label(t):
                if t in inst_map: return inst_map[t].split(" ")[0]
                return t2n.get(t, t.replace(".NS",""))
            corr.columns = [label(c) for c in corr.columns]
            corr.index   = corr.columns

            fig_corr = go.Figure(go.Heatmap(
                z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
                colorscale=[[0,"#ff4d6d"],[0.5,"#0f1623"],[1,"#00e5a0"]],
                zmin=-1, zmax=1,
                text=corr.round(2).values, texttemplate="%{text}",
                textfont=dict(size=9),
                hovertemplate="%{y} vs %{x}<br>Corr: %{z:.2f}<extra></extra>",
            ))
            fig_corr.update_layout(
                height=max(400, len(corr)*28+100),
                paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623",
                font=dict(color="#e0e6f0",family="DM Sans",size=10),
                margin=dict(l=10,r=10,t=20,b=10),
                xaxis=dict(tickangle=-45),
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            avg_corr = round(corr.values[np.triu_indices_from(corr.values,k=1)].mean(),2)
            msg = ("✅ Well diversified" if avg_corr<0.4 else
                   ("🟡 Moderate diversification" if avg_corr<0.65 else
                    "🔴 High concentration — consider adding uncorrelated asset classes"))
            st.markdown(f"{msg} · Avg pairwise correlation: **{avg_corr}**")
        else:
            st.info("Need at least 2 holdings with price history for correlation.")

        st.markdown("---")

        # Download
        export = disp.copy()
        export["Asset Class Weights"] = (f"India Equities:{meta['w_eq']}% Fixed Income:{meta['w_fi']}% "
                                          f"Gold:{meta['w_gd']}% Silver:{meta['w_sv']}% Global:{meta.get('w_gl',0)}%")
        export["Style Weights"]       = (f"Growth:{meta['w_gr']}% Value:{meta['w_va']}% "
                                          f"Dividend:{meta['w_di']}% Momentum:{meta['w_mo']}%")
        export["Cap Weights"]         = f"Large:{meta['w_lg']}% Mid:{meta['w_md']}% Small:{meta['w_sm']}%"
        export["FI Split"]            = f"LIQUIDBEES:{meta['w_liquid']}% GSEC10Y:{meta['w_gsec10']}%"
        export["Method"]              = {"1":"Top N by Tech Score","2":"BUY-only","3":"Manual"}[meta["method_key"]]
        export["Generated"]           = datetime.now().strftime("%d %b %Y %H:%M")
        st.download_button(
            "⬇️ Download Portfolio CSV",
            export.to_csv(index=False),
            file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", key="dl_portfolio",
        )

        if st.button("🗑️ Clear Portfolio", key="clear_port"):
            for k in ["portfolio_pagg","portfolio_pdf","portfolio_meta"]:
                st.session_state.pop(k,None)
            st.rerun()

    st.caption("⚠️ Educational only. Not financial advice.")

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTRUMENTS DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════
GLOBAL_INSTRUMENTS = {
    "US Equity — S&P 500 (SPY)": {
        "ticker":    "SPY",
        "region":    "US",
        "theme":     "Broad Equity",
        "desc":      "SPDR S&P 500 ETF — tracks 500 largest US companies",
        "color":     "#00cfff",
        "default_w": 0,
    },
    "US Mag 7 (QQQ)": {
        "ticker":    "QQQ",
        "region":    "US",
        "theme":     "Mega-Cap Tech",
        "desc":      "Invesco QQQ — Nasdaq-100, dominated by Apple, NVDA, Microsoft, Meta, Alphabet, Amazon, Tesla",
        "color":     "#00e5a0",
        "default_w": 40,
    },
    "APAC Tech — China (KWEB)": {
        "ticker":    "KWEB",
        "region":    "China",
        "theme":     "APAC Tech",
        "desc":      "KraneShares CSI China Internet ETF — Alibaba, Tencent, Meituan, JD",
        "color":     "#ff4d6d",
        "default_w": 15,
    },
    "APAC Tech — HK + Korea + Taiwan (EWT/EWY blend)": {
        "ticker":    "EWT",       # Taiwan (TSMC heavy)
        "ticker2":   "EWY",       # Korea (Samsung heavy)
        "region":    "APAC ex-China",
        "theme":     "APAC Tech",
        "desc":      "EWT (Taiwan, TSMC-heavy) + EWY (Korea, Samsung-heavy) — semiconductor & hardware leaders",
        "color":     "#f0a500",
        "default_w": 15,
    },
    "US Crude Oil (USO)": {
        "ticker":    "USO",
        "region":    "US",
        "theme":     "Commodity",
        "desc":      "United States Oil Fund — tracks WTI crude oil futures",
        "color":     "#ffcc44",
        "default_w": 10,
    },
    "Europe Defense (DFEN / NATO ETF)": {
        "ticker":    "DFEN",
        "region":    "Europe/US",
        "theme":     "Defense",
        "desc":      "Direxion Daily Aerospace & Defense Bull 3X — exposure to NATO defense contractors (Airbus, BAE, Lockheed, RTX)",
        "color":     "#d4a0ff",
        "default_w": 20,
    },
}

@st.cache_data(ttl=300)
def fetch_global_instrument(ticker, period="6mo"):
    """Fetch OHLCV + derived metrics for a global ETF (USD-denominated)."""
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty: return None, None
        df.columns = [c[0] if isinstance(c,tuple) else c for c in df.columns]
        price  = round(float(df["Close"].iloc[-1]),  2)
        prev   = round(float(df["Close"].iloc[-2]),  2)
        open0  = round(float(df["Close"].iloc[0]),   2)
        chg    = round((price-prev)/prev*100, 2)
        ret6m  = round((price-open0)/open0*100, 1)
        vol    = round(df["Close"].pct_change().dropna().std()*(252**0.5)*100, 1)
        return {"price":price,"change":chg,"ret_6m":ret6m,"vol_ann":vol}, df
    except:
        return None, None

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — GLOBAL ALLOCATION
# ══════════════════════════════════════════════════════════════════════════════
with tab_global:
    st.markdown("## 🌍 Global Allocation Builder")
    st.caption(
        "Allocate across US Equity, Mag 7, APAC Tech, US Crude Oil, and Europe Defense. "
        "The Global % from Step 0 (India Allocation tab) determines how much of the total "
        "portfolio flows here. Set sub-weights below to split that allocation."
    )
    st.info(
        "💡 Set the **Global %** slider in the **🗂️ India Allocation → Step 0** first, "
        "then configure the split here. The two tabs combine in **🔀 Combined Portfolio**."
    )
    st.markdown("---")

    # ── Live market snapshot ──────────────────────────────────────────────────
    st.markdown("### 📡 Live Global Market Snapshot")
    snap_cols = st.columns(len(GLOBAL_INSTRUMENTS))
    snap_data = {}
    for idx, (iname, inst) in enumerate(GLOBAL_INSTRUMENTS.items()):
        with snap_cols[idx]:
            with st.spinner(""):
                data, df_inst = fetch_global_instrument(inst["ticker"])
            snap_data[iname] = (data, df_inst)
            if data:
                chg_color = "#00e5a0" if data["change"] >= 0 else "#ff4d6d"
                arrow     = "▲" if data["change"] >= 0 else "▼"
                st.markdown(f"""
                <div class="val-card" style="border-left:3px solid {inst['color']}">
                  <div class="val-label">{inst['ticker']}</div>
                  <div class="val-value" style="color:{inst['color']}">${data['price']}</div>
                  <div style="font-size:12px;color:{chg_color}">{arrow} {data['change']:+.2f}%</div>
                  <div style="font-size:10px;color:#8899aa">6M: {data['ret_6m']:+.1f}% · Vol: {data['vol_ann']:.1f}%</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="val-card"><div class="val-label">{inst['ticker']}</div>
                <div style="color:#556677;font-size:12px">Data unavailable</div></div>""",
                unsafe_allow_html=True)
    st.markdown("---")

    # ── Sub-weight sliders ────────────────────────────────────────────────────
    st.markdown("### Step G1 — Global Sub-Weights  *(must sum to 100%)*")
    st.caption("These split your Global % allocation across the instruments below.")

    gl_weights = {}
    gl_cols = st.columns(3)
    inst_list = list(GLOBAL_INSTRUMENTS.items())

    for idx, (iname, inst) in enumerate(inst_list):
        with gl_cols[idx % 3]:
            st.markdown(
                f'<div class="alloc-bucket" style="border-left:3px solid {inst["color"]}">'
                f'<b style="color:{inst["color"]}">{inst["ticker"]}</b> '
                f'<span style="font-size:10px;color:#8899aa">({inst["region"]} · {inst["theme"]})</span><br/>'
                f'<span style="font-size:11px;color:#8899aa">{inst["desc"][:70]}…</span></div>',
                unsafe_allow_html=True
            )
            gl_weights[iname] = st.slider(
                f"{inst['ticker']} %", 0, 100,
                inst["default_w"], 5,
                key=f"gl_{inst['ticker']}"
            )

    gl_sum = sum(gl_weights.values())
    (st.success if gl_sum==100 else st.warning)(
        f"Global sub-weights: **{gl_sum}%** {'✅' if gl_sum==100 else '— must equal 100%'}"
    )
    st.markdown("---")

    # ── Price charts ──────────────────────────────────────────────────────────
    st.markdown("### 📈 Price History (6 months, USD)")
    selected_charts = st.multiselect(
        "Select instruments to chart",
        options=list(GLOBAL_INSTRUMENTS.keys()),
        default=["US Mag 7 (QQQ)", "Europe Defense (DFEN / NATO ETF)", "US Crude Oil (USO)"],
        key="gl_chart_select"
    )

    if selected_charts:
        fig_gl = go.Figure()
        for iname in selected_charts:
            inst       = GLOBAL_INSTRUMENTS[iname]
            data, df_i = snap_data.get(iname, (None, None))
            if df_i is not None and not df_i.empty:
                # Normalise to 100 for comparison
                norm = df_i["Close"] / df_i["Close"].iloc[0] * 100
                fig_gl.add_trace(go.Scatter(
                    x=df_i.index, y=norm,
                    name=inst["ticker"],
                    line=dict(color=inst["color"], width=2),
                    hovertemplate=f"{inst['ticker']}: %{{y:.1f}}<extra></extra>",
                ))
        fig_gl.add_hline(y=100, line_dash="dash", line_color="#334455", line_width=1)
        fig_gl.update_layout(
            height=380, paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623",
            font=dict(color="#8899aa", family="DM Sans"),
            legend=dict(orientation="h", yanchor="bottom", y=1.01,
                        xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10,r=10,t=40,b=10), hovermode="x unified",
            yaxis_title="Indexed (base=100)",
        )
        fig_gl.update_xaxes(gridcolor="#1a2535", showgrid=True)
        fig_gl.update_yaxes(gridcolor="#1a2535", showgrid=True)
        st.plotly_chart(fig_gl, use_container_width=True)

    # ── Save global config to session state (instant, no build btn needed) ────
    st.session_state["global_weights"]   = gl_weights
    st.session_state["global_snap_data"] = snap_data
    st.markdown("---")

    # ── Correlation within global instruments ─────────────────────────────────
    st.markdown("### 🔗 Correlation Within Global Instruments")
    st.caption("How correlated are the global instruments with each other?")

    gl_tickers = []
    for iname, inst in GLOBAL_INSTRUMENTS.items():
        gl_tickers.append(inst["ticker"])
        if "ticker2" in inst:
            gl_tickers.append(inst["ticker2"])

    gl_prices = {}
    for t in gl_tickers:
        _, df_t = fetch_global_instrument(t)
        if df_t is not None: gl_prices[t] = df_t["Close"]

    if len(gl_prices) >= 2:
        gl_corr_df = pd.DataFrame(gl_prices).dropna(how="all")
        gl_corr    = gl_corr_df.pct_change().dropna().corr().round(2)
        fig_gc = go.Figure(go.Heatmap(
            z=gl_corr.values, x=gl_corr.columns.tolist(), y=gl_corr.index.tolist(),
            colorscale=[[0,"#ff4d6d"],[0.5,"#0f1623"],[1,"#00e5a0"]],
            zmin=-1, zmax=1,
            text=gl_corr.values, texttemplate="%{text}",
            textfont=dict(size=11),
            hovertemplate="%{y} vs %{x}: %{z:.2f}<extra></extra>",
        ))
        fig_gc.update_layout(
            height=350, paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623",
            font=dict(color="#e0e6f0",family="DM Sans",size=11),
            margin=dict(l=10,r=10,t=10,b=10),
        )
        st.plotly_chart(fig_gc, use_container_width=True)

    st.caption("⚠️ Global ETF prices in USD. Currency risk applies for INR-based investors.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — COMBINED PORTFOLIO VIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_combined:
    st.markdown("## 🔀 Combined Multi-Asset Portfolio")
    st.caption("Merges your India allocation (equities + FI + gold + silver) with your global allocation into one unified view.")

    india_ready  = "portfolio_pagg" in st.session_state
    global_ready = "global_weights" in st.session_state

    if not india_ready and not global_ready:
        st.info("👈 Build your **India Allocation** first, then configure **Global Allocation**, then come back here.")
        st.stop()

    # ── Retrieve India portfolio ──────────────────────────────────────────────
    if india_ready:
        india_pagg = st.session_state["portfolio_pagg"].copy()
        india_meta = st.session_state["portfolio_meta"]
        w_gl_total = india_meta.get("w_gl", 0)     # global % of total portfolio
        w_india    = 100 - w_gl_total               # everything else is India
        # Scale India weights to their share of total portfolio
        india_pagg["Alloc % (Total)"] = (india_pagg["Alloc %"] * w_india / 100).round(3)
        india_pagg["Geography"] = "India"
    else:
        st.warning("India portfolio not built yet. Go to **🗂️ India Allocation** and click **Build Portfolio**.")
        india_pagg = pd.DataFrame()
        w_gl_total = st.session_state.get("global_weights", {})
        w_gl_total = 10   # fallback
        w_india    = 90

    # ── Build global rows ─────────────────────────────────────────────────────
    gl_rows = []
    if global_ready:
        gl_weights   = st.session_state["global_weights"]
        gl_snap_data = st.session_state.get("global_snap_data", {})
        gl_sum_check = sum(gl_weights.values())

        if gl_sum_check != 100:
            st.warning(f"⚠️ Global sub-weights sum to {gl_sum_check}% (not 100%). "
                        "Go to **🌍 Global Allocation** and fix the sliders. Showing unnormalised weights.")

        for iname, inst in GLOBAL_INSTRUMENTS.items():
            sub_w  = gl_weights.get(iname, 0)
            if sub_w == 0: continue
            # Weight in total portfolio
            total_w = round(w_gl_total * sub_w / 100, 3)
            data, _ = gl_snap_data.get(iname, (None, None))

            # Handle EWT+EWY blend — show as one row, average price metrics
            if "ticker2" in inst:
                data2, _ = fetch_global_instrument(inst["ticker2"])
                if data and data2:
                    price  = round((data["price"] + data2["price"]) / 2, 2)
                    ret6m  = round((data["ret_6m"] + data2["ret_6m"]) / 2, 1)
                    vol    = round((data["vol_ann"] + data2["vol_ann"]) / 2, 1)
                    chg    = round((data["change"]  + data2["change"])  / 2, 2)
                elif data:
                    price=data["price"]; ret6m=data["ret_6m"]; vol=data["vol_ann"]; chg=data["change"]
                else:
                    price=ret6m=vol=chg=None
            else:
                price  = data["price"]   if data else None
                ret6m  = data["ret_6m"]  if data else None
                vol    = data["vol_ann"] if data else None
                chg    = data["change"]  if data else None

            gl_rows.append({
                "Stock":             iname,
                "Ticker":            inst["ticker"] + (f"+{inst['ticker2']}" if "ticker2" in inst else ""),
                "Geography":         "Global",
                "Asset Class":       f"Global · {inst['theme']}",
                "Region":            inst["region"],
                "Theme":             inst["theme"],
                "Style":             inst["theme"],
                "Cap":               "—",
                "Sector":            inst["theme"],
                "Signal":            "—",
                "Tech Score":        None,
                "Price (USD)":       price,
                "Day Chg %":         chg,
                "6M Return %":       ret6m,
                "Ann. Vol %":        vol,
                "Alloc %":           sub_w,
                "Alloc % (Total)":   total_w,
                "Currency":          "USD",
                "Inclusion Reason":  f"Global allocation | {inst['desc']} | Sub-weight: {sub_w}% of Global {w_gl_total}%",
            })

    gl_df = pd.DataFrame(gl_rows) if gl_rows else pd.DataFrame()

    # ── Unified combined DataFrame ────────────────────────────────────────────
    india_cols = ["Stock","Ticker","Geography","Asset Class","Style","Cap","Sector",
                  "Signal","Tech Score","Price (₹)","6M Return %","Ann. Vol %",
                  "Alloc %","Alloc % (Total)","Inclusion Reason"]

    if not india_pagg.empty:
        india_pagg["Geography"]    = "India"
        india_pagg["Price (USD)"]  = None
        india_pagg["Day Chg %"]    = None
        india_pagg["Currency"]     = "INR"
        india_pagg["Region"]       = "India"
        india_pagg["Theme"]        = india_pagg.get("Asset Class", "Equity")

    combined = pd.concat([
        india_pagg if not india_pagg.empty else pd.DataFrame(),
        gl_df      if not gl_df.empty      else pd.DataFrame(),
    ], ignore_index=True)

    if combined.empty:
        st.warning("Nothing to show yet. Build both India and Global allocations.")
        st.stop()

    # Normalise Alloc % (Total) to sum to 100
    total_alloc = combined["Alloc % (Total)"].sum()
    if total_alloc > 0:
        combined["Alloc % (Total)"] = (combined["Alloc % (Total)"] / total_alloc * 100).round(2)

    combined = combined.sort_values(["Geography","Alloc % (Total)"], ascending=[True, False])

    # ── Summary metrics ───────────────────────────────────────────────────────
    st.markdown("### 🏆 Combined Portfolio Summary")

    geo_split   = combined.groupby("Geography")["Alloc % (Total)"].sum().to_dict()
    total_holds = len(combined)
    ac_split    = combined.groupby("Asset Class")["Alloc % (Total)"].sum().nlargest(5).to_dict()

    sm1,sm2,sm3,sm4,sm5 = st.columns(5)
    sm1.metric("📋 Total Holdings",   total_holds)
    sm2.metric("🇮🇳 India",           f"{geo_split.get('India',0):.1f}%")
    sm3.metric("🌍 Global",           f"{geo_split.get('Global',0):.1f}%")
    sm4.metric("📈 India Equity",     f"{combined[combined['Asset Class']=='Equities']['Alloc % (Total)'].sum():.1f}%")
    sm5.metric("🔵 Global Equity",    f"{combined[combined['Geography']=='Global']['Alloc % (Total)'].sum():.1f}%")
    st.markdown("---")

    # ── Combined holdings table ───────────────────────────────────────────────
    st.markdown("### 📋 All Holdings")

    disp_cols = ["Geography","Asset Class","Stock","Ticker","Region","Style","Cap",
                 "Alloc % (Total)","6M Return %","Ann. Vol %","Inclusion Reason"]
    disp_combined = combined[[c for c in disp_cols if c in combined.columns]]

    def hl_geo(v):
        return {"India":"color:#00cfff","Global":"color:#ff9966"}.get(v,"")
    def hl_ac2(v):
        if "Equities" in str(v):      return "color:#00cfff"
        if "Fixed Income" in str(v):  return "color:#00e5a0"
        if "Gold" in str(v):          return "color:#f0a500"
        if "Silver" in str(v):        return "color:#d4a0ff"
        if "Global" in str(v):        return "color:#ff9966"
        return ""
    def hl_alloc2(v):
        try:
            x = float(v)
            return "color:#00e5a0;font-weight:bold" if x>=5 else ("color:#e0e6f0" if x>=1 else "color:#8899aa")
        except: return ""
    def hl_ret2(v):
        try: x=float(v); return f"color:{'#00e5a0' if x>0 else '#ff4d6d'}"
        except: return ""

    fmt2 = {"Alloc % (Total)":"{:.2f}%","6M Return %":"{:.1f}%","Ann. Vol %":"{:.1f}%"}
    styled_c = (disp_combined.style
                .map(hl_geo,    subset=["Geography"])
                .map(hl_ac2,   subset=["Asset Class"])
                .map(hl_alloc2,subset=["Alloc % (Total)"])
                .map(hl_ret2,  subset=["6M Return %"])
                .set_properties(**{"background-color":"#0f1623","border-color":"#1e3a5f"})
                .format(fmt2, na_rep="—")
                .bar(subset=["Alloc % (Total)"], color=["#1a3a2a","#00e5a0"]))
    st.dataframe(styled_c, use_container_width=True, hide_index=True)
    st.markdown("---")

    # ── Breakdown charts ──────────────────────────────────────────────────────
    st.markdown("### 📊 Portfolio Breakdown")
    bc1,bc2,bc3 = st.columns(3)

    with bc1:
        geo_df = combined.groupby("Geography")["Alloc % (Total)"].sum().reset_index()
        fig_geo = px.pie(geo_df, names="Geography", values="Alloc % (Total)",
            title="India vs Global", hole=0.45,
            color_discrete_map={"India":"#00cfff","Global":"#ff9966"})
        fig_geo.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0a0e1a",
            font=dict(color="#e0e6f0",family="DM Sans"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),margin=dict(t=40,b=10,l=5,r=5))
        st.plotly_chart(fig_geo, use_container_width=True)

    with bc2:
        # Top asset classes
        ac_df = combined.groupby("Asset Class")["Alloc % (Total)"].sum().nlargest(8).reset_index()
        fig_ac2 = px.bar(ac_df, x="Alloc % (Total)", y="Asset Class", orientation="h",
            title="By Asset Class", color="Alloc % (Total)",
            color_continuous_scale=["#1a3a5f","#00e5a0"])
        fig_ac2.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0f1623",
            font=dict(color="#e0e6f0",family="DM Sans"),
            coloraxis_showscale=False,margin=dict(t=40,b=10,l=5,r=5))
        st.plotly_chart(fig_ac2, use_container_width=True)

    with bc3:
        # Global theme split
        if not gl_df.empty:
            theme_df = gl_df.groupby("Theme")["Alloc % (Total)"].sum().reset_index()
            fig_th = px.pie(theme_df, names="Theme", values="Alloc % (Total)",
                title="Global by Theme", hole=0.45,
                color_discrete_map={
                    "Mega-Cap Tech":"#00e5a0","Broad Equity":"#00cfff",
                    "APAC Tech":"#f0a500","Commodity":"#ffcc44","Defense":"#d4a0ff",
                })
            fig_th.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0a0e1a",
                font=dict(color="#e0e6f0",family="DM Sans"),
                legend=dict(bgcolor="rgba(0,0,0,0)"),margin=dict(t=40,b=10,l=5,r=5))
            st.plotly_chart(fig_th, use_container_width=True)
        else:
            st.info("Configure Global Allocation to see theme breakdown.")

    st.markdown("---")

    # ── Cross-asset correlation (India top holdings + global ETFs) ────────────
    st.markdown("### 🔗 Cross-Asset Correlation (India Top 10 + Global)")
    st.caption("How well does your global allocation diversify against Indian holdings?")

    # Pick top 10 India equity holdings by weight
    india_eq = combined[combined["Asset Class"]=="Equities"].nlargest(10,"Alloc % (Total)")
    india_tickers_corr = []
    for _, row in india_eq.iterrows():
        t = row.get("_full", STOCKS.get(row["Stock"],""))
        if t: india_tickers_corr.append(t)

    # Add global ETF tickers
    gl_tickers_corr = []
    if global_ready:
        for iname, inst in GLOBAL_INSTRUMENTS.items():
            if st.session_state["global_weights"].get(iname,0) > 0:
                gl_tickers_corr.append(inst["ticker"])

    all_corr_tickers = tuple(set(india_tickers_corr + gl_tickers_corr))
    if len(all_corr_tickers) >= 2:
        # Use the period from universe pull if available, else default to 6mo
        corr_period = st.session_state.get("universe_period", "6mo")

        with st.spinner("Fetching cross-asset price data…"):
            cross_prices = {}
            for t in all_corr_tickers:
                try:
                    if ".NS" in t:
                        # India equity — already in universe cache if pulled
                        cached = st.session_state.get("universe", {})
                        name   = next((n for n,r in cached.items()
                                       if r.get("df") is not None
                                       and STOCKS.get(n,"") == t), None)
                        if name and cached[name].get("df") is not None:
                            df_t = cached[name]["df"]
                        else:
                            # Fallback: fetch fresh
                            df_t = yf.download(t, period=corr_period,
                                               progress=False, auto_adjust=True)
                            if not df_t.empty:
                                df_t.columns = [c[0] if isinstance(c,tuple) else c
                                                for c in df_t.columns]
                    else:
                        # Global ETF
                        _, df_t = fetch_global_instrument(t)

                    if df_t is not None and not df_t.empty:
                        # Normalise column names
                        if isinstance(df_t.columns[0], tuple):
                            df_t.columns = [c[0] for c in df_t.columns]
                        cross_prices[t] = df_t["Close"]
                except Exception:
                    pass  # silently skip tickers that fail

        if len(cross_prices) >= 2:
            cross_df   = pd.DataFrame(cross_prices).dropna(how="all")
            cross_corr = cross_df.pct_change().dropna().corr().round(2)
            # Label with short names
            t2n = {v:k for k,v in STOCKS.items()}
            gl_short = {inst["ticker"]: inst["ticker"] for inst in GLOBAL_INSTRUMENTS.values()}
            cross_corr.columns = [t2n.get(c, gl_short.get(c, c.replace(".NS",""))) for c in cross_corr.columns]
            cross_corr.index   = cross_corr.columns

            fig_cross = go.Figure(go.Heatmap(
                z=cross_corr.values, x=cross_corr.columns.tolist(), y=cross_corr.index.tolist(),
                colorscale=[[0,"#ff4d6d"],[0.5,"#0f1623"],[1,"#00e5a0"]],
                zmin=-1, zmax=1,
                text=cross_corr.values, texttemplate="%{text}",
                textfont=dict(size=9),
                hovertemplate="%{y} vs %{x}: %{z:.2f}<extra></extra>",
            ))
            fig_cross.update_layout(
                height=max(350, len(cross_corr)*28+80),
                paper_bgcolor="#0a0e1a", plot_bgcolor="#0f1623",
                font=dict(color="#e0e6f0",family="DM Sans",size=9),
                margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(tickangle=-45),
            )
            st.plotly_chart(fig_cross, use_container_width=True)

            avg_cross = round(cross_corr.values[np.triu_indices_from(cross_corr.values,k=1)].mean(),2)
            msg = ("✅ Global holdings provide strong diversification" if avg_cross<0.35 else
                   ("🟡 Moderate cross-asset diversification" if avg_cross<0.6 else
                    "🔴 High correlation — global holdings may not reduce India risk sufficiently"))
            st.markdown(f"{msg} · Avg India-Global correlation: **{avg_cross}**")

    st.markdown("---")

    # ── Download combined portfolio ───────────────────────────────────────────
    export_c = disp_combined.copy()
    if india_ready:
        export_c["India Asset Weights"] = (
            f"India Eq:{india_meta.get('w_eq',0)}% FI:{india_meta.get('w_fi',0)}% "
            f"Gold:{india_meta.get('w_gd',0)}% Silver:{india_meta.get('w_sv',0)}% "
            f"Global:{india_meta.get('w_gl',0)}%"
        )
    if global_ready:
        export_c["Global Sub-Weights"] = " | ".join(
            f"{GLOBAL_INSTRUMENTS[k]['ticker']}:{v}%"
            for k,v in st.session_state["global_weights"].items() if v>0
        )
    export_c["Generated"] = datetime.now().strftime("%d %b %Y %H:%M")
    st.download_button(
        "⬇️ Download Combined Portfolio CSV",
        export_c.to_csv(index=False),
        file_name=f"combined_portfolio_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv", key="dl_combined",
    )

    st.caption("⚠️ Educational only. Not financial advice. Global ETFs priced in USD — factor in currency risk and international taxation.")
