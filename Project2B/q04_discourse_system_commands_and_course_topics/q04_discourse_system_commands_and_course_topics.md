# Discourse Knowledge Base Analysis

## Method

I used the IITM Discourse JSON data dump shared for Project 2B Q4, plus the authenticated IITM Discourse JSON API for the earlier exact-topic checks. The final correction pass used the Drive JSON files because they include course categories that my account could not directly access, especially Modern Application Development II.

The workflow was:

1. Download the public Drive folder JSON files for all 14 Discourse categories.
2. Load each subject JSON as a list of full topic objects.
3. For exact-topic tasks, match on category, normalized title, original poster, and topic creation date.
4. For accepted-answer tasks, map `accepted_answer.post_number` back to the corresponding post ID.
5. For reply-count compound tasks, count non-original posts and select the latest reply post ID before `2026-12-31T23:59:59Z`.
6. For aggregate tasks, filter solved topics by topic creation date and tags, or count posts/replies/likes by post creation date as required.

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
  "task30": "849",
  "task31": "9-617918",
  "task32": "24-702516",
  "task33": "5-628852",
  "task34": "113",
  "task35": "592990",
  "task36": "729566",
  "task37": "3-587148",
  "task38": "5-677017",
  "task39": "600820",
  "task40": "35",
  "task41": "Gurkirat",
  "task42": "Preethy",
  "task43": "8-614488",
  "task44": "749847",
  "task45": "615398",
  "task46": "584354",
  "task47": "16-613676",
  "task48": "663262",
  "task49": "701557",
  "task50": "22"
}
```

## Correction Note

The earlier 42/50 submission still depended on API search pagination and did not have Modern Application Development II access. Recomputing from the Drive JSON dump changed six answers:

- `task30`: `835` -> `849`
- `task34`: `112` -> `113`
- `task40`: `33` -> `35`
- `task42`: `24F2001956` -> `Preethy`
- `task49`: `UNRESOLVED_MAD2_ACCESS_REQUIRED` -> `701557`
- `task50`: `21` -> `22`
