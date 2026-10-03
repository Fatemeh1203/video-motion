import wave, numpy as np, json, subprocess, sys
TEMPO=float(sys.argv[1])
rec=[(1.43,4.95),(5.6,7.22),(7.80,9.55),(10.17,12.35),(12.98,19.07),(19.57,21.92),(22.49,29.12),(29.74,34.56),
(35.15,43.44),(44.29,49.99),(53.12,59.48),(61.10,66.96),(67.98,71.96),(73.20,81.35),(83.08,88.88),(89.93,92.96),
(95.05,98.40),(99.18,105.54),(106.43,109.85),(111.66,115.01),(116.04,121.97),(123.45,125.88),(126.83,130.10)]
sil=[tuple(map(float,l.split())) for l in open("sil.tsv")]
SR=48000
w=wave.open("clean.wav"); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
def ramp(n,a0,a1): return np.linspace(a0,a1,n,dtype=np.float32)
clips=[]
for i,(s,e) in enumerate(rec):
    nx=rec[i+1][0] if i+1<len(rec) else e+0.5
    s0,e0=s-0.08,min(e+0.3,nx-0.05)
    pauses=[(ps,pe) for ps,pe in sil if ps>s+0.1 and pe<e-0.1]
    parts=[]; cur=s0
    for ps,pe in pauses:
        L=pe-ps; tgt=0.30 if L<0.75 else 0.42
        if L<=tgt+0.05: continue
        keep_a=ps+tgt/2; keep_b=pe-tgt/2
        parts.append(a[int(cur*SR):int(keep_a*SR)]); cur=keep_b
    parts.append(a[int(cur*SR):int(e0*SR)])
    xf=int(0.012*SR); c=parts[0]
    for p in parts[1:]:
        c=np.concatenate([c[:-xf], c[-xf:]*ramp(xf,1,0)+p[:xf]*ramp(xf,0,1), p[xf:]])
    f=int(0.02*SR); c[:f]*=ramp(f,0,1); g=int(0.08*SR); c[-g:]*=ramp(g,1,0)
    clips.append(c)
    print(f"{i:02d} {e-s:5.2f} -> {len(c)/SR:5.2f}  pauses {len(pauses)}")
np.save("clips.npy",np.array(clips,dtype=object),allow_pickle=True)
json.dump([dict(now=len(c)/SR) for c in clips],open("placed.json","w"))
print("sum speech", round(sum(len(c) for c in clips)/SR,2))
