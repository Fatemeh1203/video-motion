import json, sys
P="/home/user/video-motion/videos/fatemeh-community/"
sched=[float(l.split("\t")[0]) for l in open(P+"voice/lines.tsv",encoding="utf-8") if l.strip()]
TEMPO=float(sys.argv[1]); G_IN=0.25; G_SC=0.45
dur=[r["now"]/TEMPO for r in json.load(open("placed.json"))]
scenes=[("s1",0,10.6,[0,1,2,3]),("s2",10,9.6,[4,5]),("s3",19,12.6,[6,7]),("s4",31,14.6,[8,9]),("s4b",45,10.1,[10]),
("s5",54.5,9.6,[11,12]),("s6",63.5,11.6,[13]),("s6b",74.5,12.1,[14,15]),("s7",86,14.6,[16,17,18,19]),("s8",100,8.6,[20]),("s9",108,12,[21,22])]
prev_end=None; voice=[]; plan=[]
for k,(name,os_,D,lines) in enumerate(scenes):
    t0=sched[lines[0]]-os_
    v=0.4 if prev_end is None else prev_end+G_SC
    ns=v-t0                       # new scene start keeps the first line's lead-in
    segs=[]                        # (old_rel_from, shift)
    for n,j in enumerate(lines):
        t=sched[j]-os_
        if n>0: v=max(ns+t+segs[-1][1], prev_end+G_IN) if False else max(prev_end+G_IN, ns+t+min(0,segs[-1][1]) if False else prev_end+G_IN)
        shift=(v-ns)-t
        segs.append((round(max(0,t-0.15),2),round(shift,2)))
        voice.append(round(v,2)); prev_end=v+dur[j]
    plan.append(dict(name=name,old_start=os_,D=D,new_start=round(ns,2),segs=segs,last_end_rel=round(prev_end-ns,2)))
# scene ends: exit starts when the next scene starts
for k,p in enumerate(plan):
    if k+1<len(plan):
        exit_new=plan[k+1]["new_start"]-p["new_start"]; p["Dn"]=round(exit_new+0.6,2)
        p["segs"].append((round(p["D"]-0.6-0.02,2),round(exit_new-(p["D"]-0.6),2)))
    else:
        p["Dn"]=round(120-p["new_start"],2); p["segs"].append((round(p["D"]-1.0-0.02,2),round(p["Dn"]-p["D"],2)))
    print(f'{p["name"]:4s} {p["old_start"]:6.1f}->{p["new_start"]:6.2f} D {p["D"]:5.1f}->{p["Dn"]:5.2f} voice_end_rel {p["last_end_rel"]:5.2f} segs {p["segs"]}')
print("voice end",round(prev_end,2),"CTA hold after voice",round(120-prev_end,2))
json.dump(dict(plan=plan,voice=voice,tempo=TEMPO),open("plan.json","w"))
