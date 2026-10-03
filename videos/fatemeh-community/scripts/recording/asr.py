import re, subprocess, wave, numpy as np, sherpa_onnx, json
M="/root/.cache/video-studio/asr/sherpa-onnx-whisper-small/small-"
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+"encoder.int8.onnx",decoder=M+"decoder.int8.onnx",tokens=M+"tokens.txt",language="fa",task="transcribe",num_threads=8)
out=subprocess.run(["ffmpeg","-i","raw.wav","-af","silencedetect=noise=-38dB:d=0.35","-f","null","-"],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; se=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
w=wave.open("r16.wav"); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768; sr=16000
segs=[]; cur=0.0
for s,e in zip(ss,se):
    if s-cur>0.15: segs.append((cur,s))
    cur=e
if len(a)/sr-cur>0.15: segs.append((cur,len(a)/sr))
res=[]
for s,e in segs:
    st=rec.create_stream(); st.accept_waveform(sr,a[int(max(0,s-0.1)*sr):int((e+0.1)*sr)]); rec.decode_stream(st)
    res.append((round(s,2),round(e,2),st.result.text.strip())); print(f"{s:7.2f} {e:7.2f}  {st.result.text.strip()}",flush=True)
json.dump(res,open("segs.json","w"),ensure_ascii=False)
