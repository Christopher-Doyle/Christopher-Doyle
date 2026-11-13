import json,re
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
USERNAME="Christopher-Doyle"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"contributions.json"
URL=f"https://github.com/users/{USERNAME}/contributions"
def main():
 r=requests.get(URL,timeout=30,headers={"User-Agent":"Mozilla/5.0 profile-readme-bot"});r.raise_for_status();s=BeautifulSoup(r.text,"html.parser")
 tips={t.get("for"):t.get_text(" ",strip=True) for t in s.find_all("tool-tip") if t.get("for")}
 by={}
 for c in s.select("[data-date]"):
  d=c.get("data-date")
  if not d: continue
  m=re.search(r"([\\d,]+)\\s+contribution",tips.get(c.get("id"),"")); count=int(m.group(1).replace(",","")) if m else 0
  by[d]={"date":d,"count":count,"level":int(c.get("data-level","0") or 0)}
 days=[by[k] for k in sorted(by)]; total=sum(x["count"] for x in days); best=max(days,key=lambda x:x["count"],default={"date":None,"count":0})
 run=longest=0
 for x in days:
  run=run+1 if x["count"]>0 else 0; longest=max(longest,run)
 current=0
 for x in reversed(days):
  if x["count"]>0: current+=1
  elif current: break
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps({"username":USERNAME,"fetched_at":datetime.utcnow().isoformat()+"Z","days":days,"stats":{"total":total,"current_streak":current,"longest_streak":longest,"best_day":best}},indent=2))
if __name__=="__main__": main()
