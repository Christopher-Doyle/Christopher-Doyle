import json
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

R=Path(__file__).resolve().parents[1]
D=json.loads((R/"data/contributions.json").read_text(encoding="utf-8"))
S=D.get("stats",{})
by_date={d["date"]: d for d in D.get("days",[])}

tz=ZoneInfo("Africa/Johannesburg")
today=datetime.now(tz).date()

# Today is intentionally on the FAR LEFT, then previous days move right.
items=[]
for offset in range(14):
    day=today-timedelta(days=offset)
    key=day.isoformat()
    raw=by_date.get(key, {"date":key,"count":0,"level":0,"active":False})
    items.append((day,raw))

active=S.get("active_days",0)
current=S.get("current_streak",0)
longest=S.get("longest_streak",0)

W,H=840,340
base_y=266
front_w=30
depth_x=9
depth_y=7
gap=22
start_x=38

# Height uses exact contribution count when available; otherwise activity level.
counts_available=bool(S.get("counts_available",False))
values=[]
for _,d in items:
    values.append(int(d.get("count",0)) if counts_available else int(d.get("level",0)))
max_value=max(values+[1])

cols=[]
labels=[]
for i,((day,d),val) in enumerate(zip(items,values)):
    h=126*(val/max_value)
    x=start_x+i*(front_w+gap)
    y=base_y-h
    delay=i*.045
    is_today=(i==0)

    top=f"{x},{y:.1f} {x+depth_x},{y-depth_y:.1f} {x+front_w+depth_x},{y-depth_y:.1f} {x+front_w},{y:.1f}"
    side=f"{x+front_w},{y:.1f} {x+front_w+depth_x},{y-depth_y:.1f} {x+front_w+depth_x},{base_y-depth_y:.1f} {x+front_w},{base_y:.1f}"
    front=f"{x},{y:.1f} {x+front_w},{y:.1f} {x+front_w},{base_y:.1f} {x},{base_y:.1f}"

    stroke="#c58cff" if is_today else "#62f1c4"
    glow="url(#todayFront)" if is_today else "url(#front)"
    topfill="url(#todayTop)" if is_today else "url(#top)"
    sidefill="url(#todaySide)" if is_today else "url(#side)"

    cols.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".25s" fill="freeze"/>'
        f'<polygon points="{front}" fill="{glow}" stroke="{stroke}" stroke-opacity=".55"/>'
        f'<polygon points="{top}" fill="{topfill}" stroke="#d8fff5" stroke-opacity=".62"/>'
        f'<polygon points="{side}" fill="{sidefill}" stroke="#5fcae9" stroke-opacity=".35"/>'
        f'</g>'
    )

    label=day.strftime("%d/%m")
    label_color="#c58cff" if is_today else "#748b85"
    label_weight=' font-weight="700"' if is_today else ""
    labels.append(
        f'<text x="{x+front_w/2+3:.1f}" y="291" text-anchor="middle" font-family="monospace" font-size="9.7" fill="{label_color}"{label_weight}>{label}</text>'
    )

grid=[]
for j in range(5):
    y=base_y+j*9
    grid.append(f'<line x1="28" y1="{y}" x2="812" y2="{y}" stroke="#173b33" stroke-opacity="{0.55-j*.08}"/>')
for j in range(15):
    x=32+j*54
    grid.append(f'<line x1="{x}" y1="{base_y}" x2="{x+34}" y2="309" stroke="#173b33" stroke-opacity=".38"/>')

metric="contributions / day" if counts_available else "activity intensity / day"
today_label=today.strftime("%d %b %Y")

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="edge" x1="0" x2="1"><stop stop-color="#54ffd0"/><stop offset=".55" stop-color="#64d9ff"/><stop offset="1" stop-color="#c58cff"/></linearGradient>
 <linearGradient id="front" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#123d30"/><stop offset=".55" stop-color="#25a778"/><stop offset="1" stop-color="#71ffd2"/></linearGradient>
 <linearGradient id="top" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#b9fff0"/><stop offset="1" stop-color="#65d9ff"/></linearGradient>
 <linearGradient id="side" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#236b61"/><stop offset="1" stop-color="#5e7fc4"/></linearGradient>
 <linearGradient id="todayFront" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#33234b"/><stop offset=".55" stop-color="#7b55c7"/><stop offset="1" stop-color="#d296ff"/></linearGradient>
 <linearGradient id="todayTop" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f0d6ff"/><stop offset="1" stop-color="#9a84ff"/></linearGradient>
 <linearGradient id="todaySide" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#6d4aa1"/><stop offset="1" stop-color="#507db1"/></linearGradient>
 <filter id="glow"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="840" height="340" rx="16" fill="#05070a"/>
<rect x="2" y="2" width="836" height="336" rx="14" fill="none" stroke="url(#edge)" opacity=".48"/>
<text x="24" y="31" fill="#7dffd8" font-family="monospace" font-size="15">$ ./activity-monitor --3d --daily --live</text>
<text x="24" y="54" fill="#607871" font-family="monospace" font-size="10.5">ROLLING 14-DAY ACTIVITY // TODAY FIRST // {today_label}</text>

<g font-family="monospace">
 <rect x="24" y="70" width="154" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="38" y="91" fill="#647b74" font-size="10">ACTIVE DAYS</text><text x="38" y="119" fill="#7dffd8" font-size="24">{active}</text>
 <rect x="193" y="70" width="154" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="207" y="91" fill="#647b74" font-size="10">CURRENT STREAK</text><text x="207" y="119" fill="#69dcff" font-size="24">{current}d</text>
 <rect x="362" y="70" width="154" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="376" y="91" fill="#647b74" font-size="10">LONGEST STREAK</text><text x="376" y="119" fill="#c58cff" font-size="24">{longest}d</text>
 <rect x="531" y="70" width="285" height="58" rx="9" fill="#07110f" stroke="#17382f"/>
 <text x="545" y="91" fill="#647b74" font-size="10">SYSTEM</text>
 <text x="545" y="116" fill="#7dffd8" font-size="13">DAILY FEED ONLINE</text>
 <circle cx="786" cy="106" r="5" fill="#62ffd0"><animate attributeName="opacity" values="1;.18;1" dur="1s" repeatCount="indefinite"/></circle>
</g>

<text x="32" y="155" fill="#c58cff" font-family="monospace" font-size="10.5">TODAY →</text>
<g>{''.join(grid)}</g>
<g filter="url(#glow)">{''.join(cols)}</g>
{''.join(labels)}
<text x="30" y="322" fill="#627a73" font-family="monospace" font-size="10.5">height = {metric}  •  left = newest  •  rolls after midnight SAST  •  auto-refresh enabled</text>
</svg>'''
(R/"activity-dashboard.svg").write_text(svg,encoding="utf-8")
