# Held site copy

## methodology-email-sms-section.html

Removed from the live methodology page on 15 Nov 2026, to be restored on 23 Nov 2026 when the Email/SMS category launches.

To restore: paste the HTML block (the `div.box#emailsms` and its contents) back into `build.py` in the `methodology.html` `page()` call, after the search and recommendation apps box and before the "Spotted an error?" paragraph. Then rebuild and deploy.

Do not publish this section before 23 Nov.

## Under-$50 essay header (held)

Brent's images already exist in /workspace/stillprice-essays/headers/:

- essays-ai-support-under-50-a-month-1456x816.png
- essays-ai-support-under-50-a-month-og-1200x630.png

They are not in assets/essays/ and are not live, because the title on the artwork includes "$50" and the title might change when Ali approves the correction draft.

One-line switch after Ali approves, if the title stays "AI support under $50 a month?":

1. Copy those two pngs into assets/essays/
2. On the ai-support-under-50-a-month essay in data/essays.json, add the same keys as the search essay:

   "hero": "essays-ai-support-under-50-a-month-1456x816.png",
   "og": "essays-ai-support-under-50-a-month-og-1200x630.png"

3. Rebuild and deploy.
