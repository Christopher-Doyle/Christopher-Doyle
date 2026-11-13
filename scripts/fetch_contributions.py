import json,re
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME="Christopher-Doyle"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"contributions.json"
URL=f"https://github.com/users/{USERNAME}/contributions"

def extract_count(cell, tips):
    candidates=[
        cell.get("aria-label",""),
        cell.get("data-count",""),
        cell.get("title",""),
        tips.get(cell.get("id"),"")
    ]
    for text in candidates:
        if not text:
            continue
        m=re.search(r"([\d,]+)\s+contribution", str(text), re.I)
        if m:
            return int(m.group(1).replace(",",""))
    return None

def main():
    r=requests.get(URL,timeout=30,headers={"User-Agent":"Mozilla/5.0 profile-readme-bot"})
    r.raise_for_status()
    s=BeautifulSoup(r.text,"html.parser")

    tips={t.get("for"):t.get_text(" ",strip=True) for t in s.find_all("tool-tip") if t.get("for")}
    by={}
    counts_found=False
    for c in s.select("[data-date]"):
        d=c.get("data-date")
        if not d:
            continue
        level=int(c.get("data-level","0") or 0)
        parsed=extract_count(c,tips)
        if parsed is not None:
            counts_found=True
        count=parsed if parsed is not None else 0
        active=(count>0) or (level>0)
        by[d]={"date":d,"count":count,"level":level,"active":active}

    days=[by[k] for k in sorted(by)]
    active_days=sum(1 for x in days if x["active"])
    total=sum(x["count"] for x in days) if counts_found else None

    run=longest=0
    for x in days:
        if x["active"]:
            run+=1
            longest=max(longest,run)
        else:
            run=0

    current=0
    for x in reversed(days):
        if x["active"]:
            current+=1
        elif current:
            break

    best=max(days,key=lambda x:(x["count"],x["level"]),default={"date":None,"count":0,"level":0})
    monthly={}
    weekday=[0]*7
    for x in days:
        month=x["date"][:7]
        monthly.setdefault(month,{"active_days":0,"intensity":0,"contributions":0})
        if x["active"]:
            monthly[month]["active_days"]+=1
            dt=datetime.fromisoformat(x["date"])
            weekday[dt.weekday()]+=1
        monthly[month]["intensity"]+=x["level"]
        monthly[month]["contributions"]+=x["count"]

    payload={
        "username":USERNAME,
        "fetched_at":datetime.utcnow().isoformat()+"Z",
        "days":days,
        "stats":{
            "total":total,
            "counts_available":counts_found,
            "active_days":active_days,
            "current_streak":current,
            "longest_streak":longest,
            "best_day":best,
            "monthly":monthly,
            "weekday_active_days":weekday
        }
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
