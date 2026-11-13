import json,calendar
from pathlib import Path
from datetime import datetime

R=Path(__file__).resolve().parents[1]
D=json.loads((R/"data/contributions.json").read_text(encoding="utf-8"))
S=D.get("stats",{})
monthly=S.get("monthly",{})
items=sorted(monthly.items())[-12:]
while len(items)<12:
    items=[("",{"active_days":0,"intensity":0})]+items

W,H=840,285
bars=[]
labels=[]
max_active=max([v.get("active_days",0) for _,v in items]+[1])
for i,(m,v) in enumerate(items):
    x=34+i*65
    val=v.get("active_days",0)
    h=105*(val/max_active)
    y=205-h
    bars.append(f'<rect x="{x}" y="{y:.1f}" width="38" height="{h:.1f}" rx="6" fill="url(#bar)" opacity=".9"><animate attributeName="height" from="0" to="{h:.1f}" dur=".7s" begin="{i*.05:.2f}s" fill="freeze"/><animate attributeName="y" from="205" to="{y:.1f}" dur=".7s" begin="{i*.05:.2f}s" fill="freeze"/></rect>')
    label=m[5:] if m else "--"
    labels.append(f'<text x="{x+19}" y="224" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#728c85">{label}</text>')

active=S.get("active_days",0)
current=S.get("current_streak",0)
longest=S.get("longest_streak",0)
weekday=S.get("weekday_active_days",[0]*7)
wd_names=["M","T","W","T","F","S","S"]
max_w=max(weekday+[1])
rhythm=[]
for i,val in enumerate(weekday):
    bx=520+i*40
    bh=46*(val/max_w)
    rhythm.append(f'<rect x="{bx}" y="{105-bh:.1f}" width="22" height="{bh:.1f}" rx="4" fill="#6fe7bd" opacity=".65"/><text x="{bx+11}" y="122" text-anchor="middle" font-family="monospace" font-size="10" fill="#718881">{wd_names[i]}</text>')

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="edge" x1="0" x2="1"><stop stop-color="#54ffd0"/><stop offset=".55" stop-color="#64d9ff"/><stop offset="1" stop-color="#c58cff"/></linearGradient>
 <linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#176748"/><stop offset=".55" stop-color="#41d4a0"/><stop offset="1" stop-color="#80ffe0"/></linearGradient>
</defs>
<rect width="840" height="285" rx="16" fill="#05070a"/>
<rect x="2" y="2" width="836" height="281" rx="14" fill="none" stroke="url(#edge)" opacity=".45"/>
<text x="24" y="31" fill="#7dffd8" font-family="monospace" font-size="15">$ ./activity-monitor --live</text>
<text x="24" y="55" fill="#637a74" font-family="monospace" font-size="10.5">12-MONTH ACTIVE-DAY TELEMETRY</text>

<g font-family="monospace">
 <rect x="24" y="72" width="144" height="53" rx="8" fill="#07110f" stroke="#17382f"/>
 <text x="38" y="91" fill="#6c817b" font-size="10">ACTIVE DAYS</text><text x="38" y="116" fill="#7dffd8" font-size="22">{active}</text>
 <rect x="181" y="72" width="144" height="53" rx="8" fill="#07110f" stroke="#17382f"/>
 <text x="195" y="91" fill="#6c817b" font-size="10">CURRENT STREAK</text><text x="195" y="116" fill="#69dcff" font-size="22">{current}d</text>
 <rect x="338" y="72" width="144" height="53" rx="8" fill="#07110f" stroke="#17382f"/>
 <text x="352" y="91" fill="#6c817b" font-size="10">LONGEST STREAK</text><text x="352" y="116" fill="#c58cff" font-size="22">{longest}d</text>
</g>

<text x="520" y="72" fill="#637a74" font-family="monospace" font-size="10">WEEKDAY RHYTHM</text>
{''.join(rhythm)}

<line x1="24" y1="205" x2="812" y2="205" stroke="#15352e"/>
{''.join(bars)}
{''.join(labels)}
<text x="24" y="254" fill="#657d77" font-family="monospace" font-size="10.5">signal: GitHub contribution calendar  •  refresh: automatic  •  status:</text>
<text x="557" y="254" fill="#7dffd8" font-family="monospace" font-size="10.5">LIVE</text>
<circle cx="589" cy="250" r="4" fill="#65ffd1"><animate attributeName="opacity" values="1;.2;1" dur="1s" repeatCount="indefinite"/></circle>
</svg>'''
(R/"activity-dashboard.svg").write_text(svg,encoding="utf-8")
