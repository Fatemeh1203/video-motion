# یک هفته در کامیونیتی (ریلز ۹:۱۶، ۶۶ ثانیه)

انیمیشن معرفی کامیونیتی هوش مصنوعی با صدای دلارا. متن گوینده: `SCRIPT.md`.

- خروجی: `renders/community-week.mp4`
- ساختار: یک فایل `index.html`؛ نوار هفت روز هفته بالای تصویر می‌ماند و هر روز یک کارت دارد.
- بررسی: `npm run check` و `npx hyperframes snapshot --at 9.5,18.5,31`

## صدا و موزیک

```bash
python3 scripts/mix_narration.py voice/lines.tsv voice assets/audio/narration.wav 66
ffmpeg -y -i assets/audio/narration.wav -b:a 192k assets/audio/narration.mp3
python3 scripts/make-bgm.py bgm-raw.wav 66
ffmpeg -y -i bgm-raw.wav -i assets/audio/narration.mp3 -filter_complex "[0:a]volume=0.55[m];[1:a]asplit[k][x];[m][k]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=500[d];[x]anullsink;[d]afade=t=in:d=1.5,afade=t=out:st=63:d=3[o]" -map "[o]" -b:a 192k assets/audio/bgm.mp3
```
