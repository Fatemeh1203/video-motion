# پرامپت‌های ویدیو (فاطمه شمس)

سه پرامپت آماده برای سه کار متفاوت. هر بار فقط بخش «تنظیمات» را پر کن. قوانین ثابت
(مراحل کار، چک‌لیست بررسی، رنگ و فونت برند) داخل اسکیل‌ها ذخیره شده‌اند، پس لازم نیست
هر بار تکرارشان کنی.

| کار | کجا | اسکیل |
|---|---|---|
| ساخت یک شات تصویری با هوش مصنوعی (فیلم واقعی‌نما) | Veo، Sora، Kling، Runway، Higgsfield | — |
| ساخت ویدیو موشن از صفر (متن، گرافیک، صدا) | Claude Code | `/video-studio` |
| ادیت ویدیویی که خودم ضبط کرده‌ام | Claude Code | `/video-edit` |

---

## ۱. پرامپت تولید ویدیو (Text-to-Video)

مدل‌های تولید ویدیو با انگلیسی خیلی بهتر کار می‌کنند. **هرگز متن فارسی از آن‌ها نخواه**؛
حروف فارسی را خراب می‌سازند. متن و لوگو را بعداً در موشن اضافه کن. هر پرامپت فقط **یک شات**
باشد (۵ تا ۱۰ ثانیه). برای چند شات پشت‌سرهم، شخصیت و نور و رنگ را در همهٔ پرامپت‌ها کلمه‌به‌کلمه
تکرار کن تا یکدست بمانند. اگر ابزار «تصویر مرجع» می‌گیرد، یک عکس از سوژه بده.

### قالب

```
[SHOT] shot type, lens, depth of field.
[SUBJECT] who/what, appearance, ONE clear action.
[SETTING] place, time of day, key props.
[LIGHT] light sources, direction, quality.
[CAMERA] one movement, speed, height.
[LOOK] color palette, mood, texture, style reference.
[TECH] duration, aspect ratio, fps.
No on-screen text, no logos, no subtitles, no watermark.
```

### نمونهٔ آماده (رنگ‌های سایتم)

```
Cinematic medium close-up, 35mm lens, shallow depth of field.
A young woman sits at a wooden desk and leans toward her laptop, curious; small
holographic icons of AI tools rise from the keyboard and slowly orbit her.
A quiet home studio at night, a plant and a notebook beside the laptop.
Soft cyan key light from the screen, violet rim light from behind, light volumetric haze.
Slow dolly-in at eye level, subtle parallax, no cuts.
Deep navy and violet palette with teal and lavender accents, floating dust particles,
calm, focused and hopeful mood, photoreal, natural skin texture, film grain.
8 seconds, 16:9, 24 fps.
No on-screen text, no logos, no subtitles, no watermark.
```

### پرامپت منفی (اگر ابزار این بخش را دارد)

```
text, letters, watermark, logo, blurry, low resolution, warped face, distorted hands,
extra fingers, flicker, jitter, morphing objects, oversaturated, cartoonish
```

### چند ایدهٔ شات برای کامیونیتی (فقط [SUBJECT] را عوض کن)

- `A teacher at a whiteboard turns around smiling as glowing diagrams of a physics simulation appear in the air beside her.`
- `Hands holding a phone; a Telegram-style chat lights up with new messages, the glow reflecting on the fingers.` (بدون نوشتن نام برند)
- `A stack of glowing paper handouts floats up from a desk and arranges itself into a neat fan.`
- `Six tall glowing portals in a dark landscape, the camera glides slowly toward the middle one.`

---

## ۲. پرامپت ویدیو موشن (Claude Code، اسکیل `/video-studio`)

```
/video-studio
یک ویدیو موشن بساز.

## تنظیمات
- طول: [۳۰ ثانیه / ۶۰ ثانیه / حداکثر ۲ دقیقه]
- ابعاد: [۱۶:۹ برای یوتیوب و سایت / ۹:۱۶ برای ریلز و استوری]
- موضوع: [مثلاً شبیه‌ساز فیزیک کامیونیتی]
- مخاطب: [مثلاً معلم‌هایی که تازه با هوش مصنوعی آشنا شده‌اند]
- هدف: بیننده بعد از دیدن ویدیو باید [عضو کامیونیتی شود / سایت را باز کند / ...]
- پیام اصلی در یک جمله: [...]
- سبک بصری: [مینیمال و تمیز / سینمایی و تاریک با تم سایتم / پرانرژی و سریع]
- حس کلی: [آرام، قابل‌اعتماد، الهام‌بخش]
- تصویر واقعی: [ضبط از سایتم / عکس‌ها و ویدیوهای پوشهٔ ... / فقط گرافیک]
- گوینده: [صدای خودم (فایل را می‌فرستم) / بدون گوینده، فقط متن و موزیک]
- پایان: QR و لینک کامیونیتی
- آزادی خلاقانه: [فقط همین ساختار / آزاد، ولی شلوغ نکن]
- تأیید مرحله‌ای: [روشن: اول متن و استوری‌بورد را نشانم بده / خاموش]

## ساختار داستان
۱. قلاب (۰ تا ۳ ثانیه): [سؤال یا جملهٔ غافلگیرکننده]
۲. مشکل: [...]
۳. راه‌حل: [...]
۴. نمایش و اثبات: [...]
۵. دعوت به اقدام: [...]

## قوانین
- متن روی صفحه کوتاه باشد: هر صحنه حداکثر ۷ کلمه، ظاهرشدن کلمه‌به‌کلمه.
- هر صحنه فقط یک ایده داشته باشد. ترنزیشن‌ها نرم باشند و ریتم با موزیک هماهنگ باشد.
- قبل از تحویل، از لحظهٔ هر جمله فریم بگیر و خوانایی و هم‌زمانی را چک کن.
```

---

## ۳. پرامپت ادیت ویدیو (Claude Code، اسکیل `/video-edit`)

فایل ویدیو را بفرست، بعد:

```
/video-edit
این ویدیو را ادیت کن.

## تنظیمات
- فایل: [فایلی که فرستادم]
- نوع ویدیو: [آموزشی بلند / ریلز عمودی / معرفی محصول]
- خروجی: [MP4 آماده / پروژهٔ قابل ویرایش در Premiere]
- ابعاد: [۱۶:۹ / ۹:۱۶]
- سبک بصری: [مینیمال و خیلی تمیز با رنگ‌های سایتم]
- حس کلی: [قابل‌اعتماد، گرم، سریع]
- هدف: بیننده بعد از دیدنش باید بتواند [...]
- جای صورت من در کادر: [وسط / راست / چپ]
- پوشهٔ فایل‌های کمکی: [بی‌رول، لوگوها، موزیک، افکت صوتی؛ یا «نداریم»]
- لحظه‌های مشخص:
  - وقتی گفتم «[کلمه]» ← [چه چیزی، از کدام سمت، با چه حرکتی]
- آزادی خلاقانه: [فقط همین لحظه‌ها / آزاد، ولی شلوغ نکن]
- کلمات اضافهٔ من: خب، عه، اِم، یعنی، ببین
- زیرنویس: [فارسی کلمه‌به‌کلمه / ندارد]
- طول نهایی: [حداکثر ۶۰ ثانیه / هر چه شد]
- تأیید مرحله‌ای: [روشن: جدول برش و استوری‌بورد را قبل از ساخت نشانم بده / خاموش]
```

**اجرای کاملاً خودکار** (بعد از اینکه چند بار نتیجه را دیدی و راضی بودی؛ تأیید مرحله‌ای خاموش):

```
/goal با اسکیل video-edit ویدیوی [فایل] را طبق تنظیمات زیر ادیت کن و تا شرط پایان همان اسکیل برقرار نشده ادامه بده. [تنظیمات پرشده]
```

**یاد گرفتن سبک از یک ویدیوی دیگر:**

```
این ویدیو را ببین: [فایل]
تحلیل کن چرا سبک ادیتش خوب است: ریتم برش‌ها، نوع انیمیشن‌ها، تایپوگرافی، رنگ‌ها و صداگذاری.
بعد این تحلیل را به اسکیل video-edit اضافه کن تا ویدیوهای خودم را با همین سبک ادیت کنی.
```

**بهتر کردن اسکیل با بازخورد:** بعد از هر خروجی بگو «این قسمت خوب بود، این قسمت نه، اسکیل را
آپدیت کن». هر چیزی را که دو بار گفتی، به اسکیل اضافه می‌شود.
