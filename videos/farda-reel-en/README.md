# Farda Academy Reel (English)

English version of `../farda-reel`: same 38.6 s cut, 1080×1920, left-to-right layout, same music (vidIQ track)
and sound design. No narration; on-screen text only. Final file: `renders/farda-reel-en.mp4`.
Caption for the post: `CAPTION.txt` (ig-caption: READY).

Hook: «Farda Academy's new accountant» + sticker «Doesn't even take a salary» (hookscore 59, OK).

| Time | On-screen card |
|---|---|
| 0:00 | Farda Academy's new accountant |
| 0:03 | Teacher pay, still on a calculator? |
| 0:05 | Receipts, invoices, Excel... everywhere |
| 0:06 | Payments: just one form |
| 0:09 | Manager approves in Telegram |
| 0:11 | Teacher's 70% share, automatic |
| 0:13 | Expenses + invoice photo |
| 0:15 | Investor capital, kept separate |
| 0:17 | Class schedule & groups |
| 0:19 | Class held or cancelled? |
| 0:21 | All in Google Sheets (17 sheets) |
| 0:23 | Month end: just one button |
| 0:25 | Payroll report, in Gmail |
| 0:28 | Pay teachers: one tick |
| 0:30 | Quarterly reports, automatic |
| 0:32 | Want one like this? · Just send us a DM |
| 0:35 | Farda Science Academy: logo, aifardainstitute.ir, Instagram and Telegram @amozeshgah_farda, «Want a similar project? DM us» |

Sample data (Sara Mohammadi, C001, M001, 70%) comes from the Farda-Institute README. Sheet tab names are
English translations for the viewer; the real workbook's tabs are in Persian.

## Rebuild

```bash
npx hyperframes check
npx hyperframes render -o renders/raw.mp4 --quality delivery
```
