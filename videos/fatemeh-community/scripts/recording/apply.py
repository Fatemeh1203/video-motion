import json, re, subprocess, numpy as np, wave
P="/home/user/video-motion/videos/fatemeh-community/"
J=json.load(open("plan.json")); plan=J["plan"]; voice=J["voice"]; TEMPO=J["tempo"]
SRC={"s1":("agents-clean.mp4",5.0,0.47),"s2":("about-clean.mp4",6.0,0.62),"s3":("community-clean.mp4",6.0,0.47),
     "s6":("simulators.mp4",6.0,0.47),"s8":("home-ring.mp4",14.0,1.1),"s9":("home-ring-clean.mp4",10.0,0.84)}
FILE={"s1":"s1-hook","s2":"s2-intro","s3":"s3-reveal","s4":"s4-daily","s4b":"s4b-news","s5":"s5-handouts",
      "s6":"s6-simulators","s6b":"s6b-qa","s7":"s7-transform","s8":"s8-site","s9":"s9-cta"}
def fmt(x): return f"{x:.2f}".rstrip("0").rstrip(".")
# ---- sub-compositions
for p in plan:
    n=p["name"]; cid=FILE[n]; f=P+f"compositions/{cid}.html"; h=open(f,encoding="utf-8").read()
    D=fmt(p["D"]); Dn=fmt(p["Dn"])
    h=re.sub(r'(data-composition-id="%s"[^>]*data-duration=")[\d.]+"'%cid, r'\g<1>%s"'%Dn, h, count=1)
    if n in SRC:
        src,L,rate=SRC[n]; nr=min(rate,round((L-0.1)/p["Dn"],3))
        h=re.sub(r'(<video[^>]*src="assets/clips/%s"[^>]*data-duration=")[\d.]+("[^>]*data-playback-rate=")[\d.]+'%re.escape(src),
                 r'\g<1>%s\g<2>%s'%(Dn,nr), h, count=1)
    segs=json.dumps(p["segs"])
    snippet=(f'          // narration retime (Fatemeh\'s recorded voice): [from_second, shift] segments\n'
             f'          const __warp = {segs};\n'
             f'          tl.getChildren(false, true, true).map((c) => [c, c.startTime()]).forEach(([c, st]) => {{\n'
             f'            let s = 0;\n'
             f'            for (const [from, sh] of __warp) if (st >= from) s = sh;\n'
             f'            if (s) c.startTime(st + s);\n'
             f'          }});\n\n')
    mark=f'          window.__timelines["{cid}"] = tl;'
    assert mark in h and "__warp" not in h, cid
    h=h.replace(mark, snippet+mark)
    open(f,"w",encoding="utf-8").write(h)
# ---- index.html
f=P+"index.html"; h=open(f,encoding="utf-8").read()
for p in plan:
    cid=FILE[p["name"]]
    h=re.sub(r'(data-composition-id="%s"\s+data-composition-src="[^"]+"\s+data-start=")[\d.]+("\s+data-duration=")[\d.]+'%cid,
             r'\g<1>%s\g<2>%s'%(fmt(p["new_start"]),fmt(p["Dn"])), h, count=1)
def remap(T):
    k=0
    for i,p in enumerate(plan):
        if T>=p["old_start"]-0.65: k=i
    p=plan[k]; rel=T-p["old_start"]; s=0
    for fr,sh in p["segs"]:
        if rel>=fr: s=sh
    return max(0,p["new_start"]+rel+s)
def sfx(m):
    return m.group(1)+fmt(round(remap(float(m.group(2))),2))
h=re.sub(r'(<audio id="sfx-[^"]+" src="[^"]+" data-start=")([\d.]+)', sfx, h)
h=h.replace("<!-- narration: female Persian voice (sherpa-onnx, mimic3 fa haaniye), voice/lines.tsv -->",
            "<!-- narration: Fatemeh's own recorded voice (voice/fatemeh-take.m4a), cleaned and placed by scripts/place_recording.py -->")
open(f,"w",encoding="utf-8").write(h)
# ---- voice track
clips=np.load("clips.npy",allow_pickle=True); SR=48000
tr=np.zeros(int(SR*120),np.float32)
for c,v in zip(clips,voice):
    c=c.astype(np.float32)
    if TEMPO!=1.0:
        r=subprocess.run(["ffmpeg","-loglevel","error","-f","f32le","-ar","48000","-ac","1","-i","-","-af",f"atempo={TEMPO}","-f","f32le","-"],input=c.tobytes(),capture_output=True,check=True)
        c=np.frombuffer(r.stdout,np.float32)
    k=int(v*SR); e=min(len(tr),k+len(c)); tr[k:e]+=c[:e-k]
with wave.open("voice_placed.wav","wb") as o:
    o.setnchannels(1);o.setsampwidth(2);o.setframerate(SR);o.writeframes((np.clip(tr,-1,1)*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","voice_placed.wav","-af","alimiter=limit=0.89:attack=3:release=60,loudnorm=I=-16:TP=-1.5:LRA=9","-ar","44100","-ac","2",P+"assets/audio/narration.wav"],check=True)
open(P+"voice/lines.tsv","w",encoding="utf-8").write("".join(f"{v}\t{l.split(chr(9),1)[1]}" for v,l in zip(voice,[x for x in open(P+'voice/lines.tsv',encoding='utf-8') if x.strip()])))
print("done; voice starts:",voice)
