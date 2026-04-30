# Discourse Knowledge Base Analysis

## Method

I used the IITM Discourse JSON API through an authenticated browser session, because the course categories are login-restricted. The workflow was:

1. Read category metadata from `/site.json` to map category names to slugs and IDs.
2. Search solved topics with `/search.json?q=category:<slug> status:solved ...` and paginate until no more results.
3. Fetch each topic with `/t/<topic_id>.json`; for long topics, fetch missing post IDs through `/t/<topic_id>/posts.json?post_ids[]=...`.
4. Compute reusable per-topic fields: original poster, topic creation date, tags, accepted answer post ID, reply count, latest reply post ID, post authors, and like counts.
5. Filter exactly by the prompt's category, title, author, date range, and cutoff timestamp.

Important correction from the first failed submission: the portal requires keys named `task1` through `task50`. Numeric keys like `"9"` are not accepted and cause a 0/50 validation result.

## Submission Payload

```json
{
  "task1": "721351",
  "task2": "8-677523",
  "task3": "257",
  "task4": "9-664628",
  "task5": "730270",
  "task6": "706319",
  "task7": "3-759112",
  "task8": "730409",
  "task9": "3-730377",
  "task10": "5-627022",
  "task11": "694815",
  "task12": "599945",
  "task13": "182",
  "task14": "3-598613",
  "task15": "81",
  "task16": "24f3000936",
  "task17": "3-649398",
  "task18": "3-684375",
  "task19": "110",
  "task20": "91",
  "task21": "132",
  "task22": "6-658119",
  "task23": "646566",
  "task24": "4-722076",
  "task25": "581608",
  "task26": "6-755560",
  "task27": "4-659810",
  "task28": "23f1001171",
  "task29": "629844",
  "task30": "835",
  "task31": "9-617918",
  "task32": "24-702516",
  "task33": "5-628852",
  "task34": "112",
  "task35": "592990",
  "task36": "729566",
  "task37": "3-587148",
  "task38": "5-677017",
  "task39": "600820",
  "task40": "33",
  "task41": "Gurkirat",
  "task42": "24F2001956",
  "task43": "8-614488",
  "task44": "749847",
  "task45": "615398",
  "task46": "584354",
  "task47": "16-613676",
  "task48": "663262",
  "task49": "UNRESOLVED_MAD2_ACCESS_REQUIRED",
  "task50": "21"
}
```

## Access Note

Task 49 asks for a Modern Application Development II topic. The authenticated Discourse session used here does not expose a Modern Application Development II category in `/site.json`, searches for the exact title/author/date returned no topic, and a direct scan of nearby topic IDs from 2025-11-21 did not expose the matching topic. This one needs data from a peer account that has MAD2 access.
