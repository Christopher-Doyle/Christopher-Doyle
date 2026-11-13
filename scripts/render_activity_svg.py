import json
from pathlib import Path

R=Path(__file__).resolve().parents[1]
D=json.loads((R/"data/contributions.json").read_text(encoding="utf-8"))
S=D.get("stats",{})
monthly=S.get("monthly",{})
items=sorted(monthly.items())[-12:]
while len(items)<12:
    items=[("",{"active_days":0,"intensity":0})]+items

active=S.get("active_days",0)
current=S.get("current_streak",0)
longest=S.get("longest_streak",0)

W,H=840,330
base_y=258
front_w=34
depth_x=10
depth_y=8
gap=25
start_x=48
max_active=max([v.get("active_days",0) for _,v in items]+[1])

cols=[]
labels=[]
for i,(m,v) in enumerate(items):
    val=v.get("active_days",0)
    h=118*(val/max_active)
    x=start_x+i*(front_w+gap)
    y=base_y-h
    delay=i*.055
    top=f"{x},{y:.1f} {x+depth_x},{y-depth_y:.1f} {x+front_w+depth_x},{y-depth_y:.1f} {x+front_w},{y:.1f}"
    side=f"{x+front_w},{y:.1f} {x+front_w+depth_x},{y-depth_y:.1f} {x+front_w+depth_x},{base_y-depth_y:.1f} {x+front_w},{base_y:.1f}"
    front=f"{x},{y:.1f} {x+front_w},{y:.1f} {x+front_w},{base_y:.1f} {x},{base_y:.1f}"
    cols.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".28s" fill="freeze"/>'
        f'<polygon points="{front}" fill="url(#front)" stroke="#62f1c4" stroke-opacity=".42"/>'
        f'<polygon points="{top}" fill="url(#top)" stroke="#a7ffe7" stroke-opacity=".65"/>'
        f'<polygon points="{side}" fill="url(#side)" stroke="#5fcae9" stroke-opacity=".38"/>'
        f'<line x1="{x+front_w/2:.1f}" y1="{y:.1f}" x2="{x+front_w/2+depth_x:.1f}" y2="{y-depth_y:.1f}" stroke="#d8fff5" stroke-opacity=".24"/>'
        f'</g>'
    )
    label=m[5:] if m else "--"
    labels.append(f'<text x="{x+front_w/2+3:.1f}" y="283" text-anchor="middle" font-family="monospace" font-size="10.5" fill="#748b85">{label}</text>')

# Perspective floor grid
grid=[]
for j in range(5):
    y=base_y+j*9
    grid.append(f'<line x1="33" y1="{y}" x2="808" y2="{y}" stroke="#173b33" stroke-opacity="{0.55-j*.08}"/>')
for j in range(13):
    x=40+j*62
    grid.append(f'<line x1="{x}" y1="{base_y}" x2="{x+38}" y2="304" stroke="#173b33" stroke-opacity=".42"/>')

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="edge" x1="0" x2="1"><stop stop-color="#54ffd0"/><stop offset=".55" stop-color="#64d9ff"/><stop offset="1" stop-color="#c58cff"/></linearGradient>
 <linearGradient id="front" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#123d30"/><stop offset=".55" stop-color="#25a778"/><stop offset="1" stop-color="#71ffd2"/></linearGradient>
 <linearGradient id="top" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#b9fff0"/><stop offset="1" stop-color="#65d9ff"/></linearGradient>
 <linearGradient id="side" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#236b61"/><stop offset="1" stop-color="#5e7fc4"/></linearGradient>
 <filter id="glow"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="840" height="330" rx="16" fill="#05070a"/>
<rect x="2" y="2" width="836" height="326" rx="14" fill="none" stroke="url(#edge)" opacity=".48"/>
<text x="24" y="31" fill="#7dffd8" font-family="monospace" font-size="15">$ ./activity-monitor --3d --live</text>
<text x="24" y="54" fill="#607871" font-family="monospace" font-size="10.5">12-MONTH ACTIVE-DAY TELEMETRY // PERSPECTIVE MODE</text>

<g font-family="monospace">
 <rect x="24" y="70" width="154" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="38" y="91" fill="#647b74" font-size="10">ACTIVE DAYS</text><text x="38" y="119" fill="#7dffd8" font-size="24">{active}</text>
 <rect x="193" y="70" width="154" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="207" y="91" fill="#647b74" font-size="10">CURRENT STREAK</text><text x="207" y="119" fill="#69dcff" font-size="24">{current}d</text>
 <rect x="362" y="70" width="154" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="376" y="91" fill="#647b74" font-size="10">LONGEST STREAK</text><text x="376" y="119" fill="#c58cff" font-size="24">{longest}d</text>
 <rect x="531" y="70" width="285" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="545" y="91" fill="#647b74" font-size="10">SYSTEM</text>
 <text x="545" y="116" fill="#7dffd8" font-size="13">ACTIVITY FEED ONLINE</text>
 <circle cx="786" cy="106" r="5" fill="#62ffd0"><animate attributeName="opacity" values="1;.18;1" dur="1s" repeatCount="indefinite"/></circle>
</g>

<g>{''.join(grid)}</g>
<g filter="url(#glow)">{''.join(cols)}</g>
{''.join(labels)}
<text x="30" y="313" fill="#627a73" font-family="monospace" font-size="10.5">height = active days / month  •  signal = GitHub contribution calendar  •  auto-refresh enabled</text>
</svg>'''
(R/"activity-dashboard.svg").write_text(svg,encoding="utf-8")
