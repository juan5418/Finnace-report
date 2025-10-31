import yfinance as yf
from datetime import datetime
import resend

# 🔑 Ta clé API Resend
resend.api_key = "re_PQwVrq7T_JgE4TZMAVNge68ZEY1fb7732"

# Tes symboles
symbols = ["GC=F", "CL=F", "AAPL", "TSLA", "MSFT", "AMZN"]

# Fonction pour récupérer prix + % évolution
def get_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")  # 2 jours pour comparaison
    if len(data) < 2:
        return None, None
    last = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2]
    pct = (last - prev) / prev * 100
    color = "🟢" if pct >= 0 else "🔴"
    return last, f"{pct:.2f}% {color}"

# Construire le contenu HTML
html = "<h2>📈 Daily Finance Report</h2><ul>"
for sym in symbols:
    price, pct = get_price(sym)
    if price is not None:
        html += f"<li>{sym}: ${price:.2f} ({pct})</li>"
html += f"</ul><p>Envoyé le {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"

# Envoyer via Resend
def send_email(to_email, subject, html_content):
    resend.Emails.send({
        "from": "Support <contact@girid.earth>",
        "to": [to_email],
        "subject": subject,
        "html": html_content
    })

# Usage
send_email("12.hugo.pizarro@lafase.cl", "Daily Finance Report", html)
