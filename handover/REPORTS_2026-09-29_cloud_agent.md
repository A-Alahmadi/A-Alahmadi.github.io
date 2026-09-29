# تقارير وكيل جيت هب السحابي، 2026-09-29

بالشكل الثابت في القسم 9 من الموافقة. أربعة تقارير: واحد عاجل خارج الدورة، وثلاثة
تسليم رقعة. والمخرج الخام في الملحق في آخر الملف، والأرقام في التقارير منقولة منه.

**الفرع:** `claude/github-cloud-agent-5rjey5`. **رأسه:** `7dbdc6d`. و`origin/main` ما زال
على `13fc136`، فلم يُنشر شيء على الصفحة الحية.

---

## تقرير عاجل خارج الدورة: ثلاثة أرقام في ملفاتكم لا تطابق الواقع

القسم 9.1 يوجب تقريراً فورياً إن تبيّن أن قياساً مكتوباً لي خطأ. وجدت ثلاثة.

### 1. عدد PNG هو 55 لا 52

الشرط الثاني في القسم 4 من الموافقة، والقسم 7 من التسليم، يقولان 52. والمقيس على
`index.html` عند `13fc136` هو **55**.

```
$ grep -o 'data:image/png;base64,' index.html | wc -l
55
```

**والسبب معروف ومقبول لا عطل:** العلامة `mark-192.png` مضمّنة **ثلاث مرات في رأس
المستند**، 37,743 بايتاً للنسخة، وهي من الالتزامين `7a3c670` و`13fc136`. و52 زائد 3
يساوي 55. فالرقم 52 قياس ما قبل التزامَي الهوية، ولم يُحدَّث بعدهما.

وفصّلت المستند كله: **39 حمولة PNG متمايزة في 55 ظهوراً**، وثلاثتها في الرأس هي
العلامة نفسها ببصمة `4e3ba6e6da160fc3222f1a876d7bb1381123344c15b193bea9bf39ef462785ee`.

**فالشرط الثاني يُقرأ من الآن: 98 JPEG، و55 PNG، وصفر `(expected)`، وواحد
`2022 to 2027`.** وإلا صار كل تحقق لاحق إنذاراً كاذباً، وأوقف بنداً سليماً.

### 2. "6.3 وحده يلمس المتن" غير صحيح

القسم 4 من الموافقة يقول ذلك. والبندان 6.2 و6.6 يلمسان المتن أيضاً بالضرورة:

| البند | لماذا يلمس المتن |
|---|---|
| 6.2 | النسخ الثلاث من السيرة كلها بعد `<body>`، في الحرف 182,189 و506,438 و1,118,727 |
| 6.6 | الترويسة في الترميز لا في التنسيق، وقد نبّهتم إلى ذلك في القسم 8.8 نفسه |

وبصمات المتن المتوقعة لكل حالة محسوبة، وهي في تقريري كل بند أدناه، فالتغيّر مقيس
لا مفاجئ.

### 3. تعديل عدّاد التكرار في القسم 8.3 لا يعطي تشغيلة واحدة

**هذا أخطرها، ولولا القياس لنُشرت علامة تدور مرتين.**

القسم 8.3 يقول: اجعل العدّاد `01 00` بدل `00 00` فتصير تشغيلة واحدة. **والمقيس أن
كروميوم يقرأ العدّاد على أنه عدد التكرارات الإضافية، لا عدد التشغيلات.** فعّلت
أربع نسخ من الملف نفسه وقِست متى تتوقف الحركة، بأخذ بصمة الإطار كل 600 ميلي ثانية
أربع عشرة ثانية:

| النسخة | آخر تغيّر في الصورة | الخلاصة |
|---|---|---|
| الأصل، عدّاده صفر | 14,201 ملّي ثانية ولم يتوقف | يدور إلى الأبد، كما وصفتم |
| العدّاد `01 00` | **8,201 ملّي ثانية** | **تشغيلتان**، لا واحدة |
| العدّاد `02 00` | 11,800 ملّي ثانية | ثلاث تشغيلات |
| **بحذف كتلة NETSCAPE كلها** | **4,001 ملّي ثانية** | **تشغيلة واحدة**، وهي مدة الحركة نفسها |

ومدة الحركة 4.0 ثوانٍ بالضبط: 48 إطاراً، تأخير كل إطار 8 أو 9 من مئة الثانية.

**فنفّذت الحذف لا التعديل**، وهو 19 بايتاً: `21 ff 0b` ثم `NETSCAPE2.0` ثم
`03 01 00 00 00`. وبقية الملف مطابقة للأصل بايتاً بايتاً، بلا إعادة ترميز، والإطارات
والألوان والشفافية كما هي.

**وأثره على شرطكم في القسم 8.3:** الحجم لا يبقى 208,193 بل يصير **208,174**، أي أنقص
بتسعة عشر بايتاً. والمقاس 128 في 128 كما هو، والإطارات 48 كما هي. فإن كان شرط الحجم
مقصوداً لذاته فهذا سؤال معلّق، وإن كان مقصوده "لا يُعاد الترميز" فقد تحقق تماماً.

---

## تقرير 1: البند 6.2

```
البند:            6.2، تنزيل السيرة: ملف واحد برابط ثابت
الحالة:           رقعة جاهزة. النصف المستودعي منشور على الفرع، والنصف الآخر ينتظر الجهاز
```

**ما نفّذته أنا في المستودع:**

الالتزام `7d2105e`، وفيه ملف واحد مضاف: `media/Ahmad_Al-Ahmadi_CV.pdf`.

مستخرج بايتاً بايتاً من النسخ الثلاث المضمّنة في `index.html` المنشور، ففكّه يطابق
البصمة المعروفة. ولم أبنِ سيرة جديدة ولم ألمس `index.html`.

**ما يحتاج الجهاز:**

مرساة واحدة، نصاً حرفياً، **بلا سطر جديد داخلها فلا تتأثر بنهايات الأسطر**:

```
assets/cv/Ahmad_Al-Ahmadi_CV.pdf
```

البديل:

```
https://a-alahmadi.github.io/media/Ahmad_Al-Ahmadi_CV.pdf
```

المواضع، وتحقّق من عددها قبل التطبيق وتوقّف إن اختلف:

| الملف | العدد المتوقع |
|---|---|
| `04_Site/index.html` | 2، في `class="nav-cv"` و`id="cv-btn"` |
| `04_Site/site-data.js` | 1، السطر 17، حقل `cv:` |

ولا شيء غير ذلك يُمسّ: المرساة جزء من قيمة `href` وحدها، فتبقى `class` و`id`
وخاصية `download` ونص الرابط كما هي حرفاً حرفاً. ثم:

```
python 04_Site/build_publish.py
```

**البصمات:**

| الملف | قبل | بعد |
|---|---|---|
| `media/Ahmad_Al-Ahmadi_CV.pdf` | غير موجود | `f3bd9804c24bc41ff94a82947b914dff98e275bed37c2327169fe44a63eaa963`، 243,058 بايتاً، PDF 1.4 |
| `index.html` | 17,144,749 بايتاً | **16,172,596 بايتاً** متوقعاً |

**اختبار المتن:**

| | البصمة |
|---|---|
| قبل | `c9a5fa115830c6978d2fdc8c63bb8ff789253cef9dfa82f2023dea7c12ce70fe` |
| بعد، متوقعاً | `63026234b7b66fda1ac551e224ff4f289df5aeb6e845e7f9f676991d0a2fe468` |

**تتغيّر، والسبب مقيس:** النسخ الثلاث من السيرة في المتن لا في الرأس، وقد حدّدت
مواضعها في التقرير العاجل أعلاه. والذي تغيّر هو قيمة `href` في ثلاثة مواضع لا غير:
972,153 حرفاً من `data:` تصير رابطاً واحداً مكرراً ثلاثاً. **ولا نص ولا عنوان ولا رقم
ولا تعليق صورة تغيّر.**

وحسبت البصمة المتوقعة بتطبيق الاستبدال نفسه على المُخرَج المنشور، فإن لم تُبنَ
تغييرات أخرى في الدفعة فهي تطابق بايتاً ببايت. وإن اختلفت فشيء آخر تغيّر مع الرقعة،
فلا تنشروا وأرسلوا لي الفرق.

**العدّات المتوقعة بعد البناء:** 98 JPEG، و55 PNG، وصفر `(expected)`، وواحد
`2022 to 2027`، و**صفر** `data:application/pdf;base64,` بدل ثلاثة، و**ثلاثة** للرابط
المطلق.

**الصفحة الحية:**

**لم أقسها، ولا أستطيع.** سياسة الشبكة في بيئتي تمنع المضيف:

```
$ curl -sSI https://a-alahmadi.github.io/index.html | grep -i -E "^HTTP|content-length"
curl: (56) CONNECT tunnel failed, response 403
```

فقِست بدلاً منها المُخرَج المنشور في المستودع عند `origin/main` وهو `13fc136` نفسه
الذي تخدمه Pages، وهو مطابق للصفحة الحية بايتاً. والمخرج الخام في الملحق.
والحل بيد أحمد: **إعدادات الشبكة في بيئة الجلسة السحابية**، إما مستوى وصول أوسع
أو إضافة `a-alahmadi.github.io` إلى النطاقات المسموحة. وإلى أن يُفتح، **التحقق الحي
عليكم** بعد كل نشر.

**ما لم أفعله ولماذا:**

- **لم أدفع إلى `main`.** تعليماتي تحصرني في فرعي، وقاعدتكم أن النشر ينتظر كلمة أحمد.
  **وهذا قيد ترتيب لا تفضيل:** `media/Ahmad_Al-Ahmadi_CV.pdf` يجب أن يكون على `main`
  **قبل** أن يُنشر `index.html` المبني أو معه، وإلا صار الرابط الجديد 404 على الصفحة
  الحية. فإما يدمج أحمد الفرع، أو تدمجونه في نسختكم قبل دفع الصفحة:
  ```
  git fetch origin claude/github-cloud-agent-5rjey5
  git merge --no-ff origin/claude/github-cloud-agent-5rjey5
  ```
- **لم ألمس `index.html` في المستودع**، لأنه يُمحى عند أول إعادة بناء.

**تحقق زائد يطمئنكم:** قرأت معالج التنزيل في `main.js`، وفيه:

```js
if (!href || href.indexOf("data:") !== 0) return; /* plain file link, let it pass */
```

فهو يتنحّى من تلقاء نفسه للروابط الحقيقية، ويتولى المتصفح التنزيل. **فالبند 6.2 لا
يكسر مسار التنزيل**، بل يعيده إلى المسار الذي كتبتم المعالج أصلاً ليتركه يمرّ. ويصير
المعالج بعدها بلا عمل، وتنظيفه اختياري وخارج هذا البند.

**سؤال معلّق لأحمد:** لا شيء. والسؤال للجهاز: **أرسلوا لي `04_Site/build_publish.py`**،
لسببين: البند 6.1 لا أكتب رقعته بمرساة قبل أن أرى الدالة `repl` وكيف يُنسخ المُخرَج
إلى المستودع؛ ومتانة 6.2 تحتاج سطراً في أداة النشر ينسخ السيرة إلى `site_repo/media/`
مع كل نشرة، وإلا بقيت نسخة المستودع على القديم إذا بُنيت سيرة جديدة، وهذا هو العطل
نفسه الذي نصلحه. وإلى حينه: **إن تغيّرت السيرة فأبلغوني لأرفع النسخة الجديدة.**

---

## تقرير 2: البند 6.4

```
البند:            6.4، مقاسات الجوال
الحالة:           رقعة جاهزة. لا عمل مستودعياً في هذا البند
```

**ما نفّذته أنا في المستودع:** لا شيء. البند كله في `04_Site/styles.css`.

**ما يحتاج الجهاز:** مرساتان في `04_Site/styles.css`، كلتاهما **سطر واحد**، وتحققت
أن كلاً منهما تظهر مرة واحدة في الملف.

المرساة الأولى، تعديل في مكانه:

```
  .btn-small { padding: 9px 12px; font-size: 10.5px; }
```

البديل:

```
  .btn-small { padding: 9px 12px; font-size: 12px; }
```

المرساة الثانية، إدراج بعدها:

```
  .hero { padding: 64px 0 56px; }
```

البديل، السطر نفسه ثم الكتلة بعده، **بنهايات الملف أي CRLF**:

```
  .hero { padding: 64px 0 56px; }

  /* phone sizing: nothing readable under 12px, and every control 44px tall */
  .head-name small { font-size: 12px; }
  .portrait .dim { font-size: 12px; }
  .card-img .year { font-size: 12px; }
  .card-body .client { font-size: 12px; }
  .card-body .open { font-size: 12px; }
  .cred .yr { font-size: 12px; }
  .cred .detail { font-size: 12px; }
  .case-meta .k { font-size: 12px; }
  .note .tag { font-size: 12px; }
  footer .wrap { font-size: 12px; }
  .mark { min-height: 44px; }
  .nav-toggle { width: 44px; height: 44px; }
  .case-nav .btn { min-height: 44px; }
```

الكتلة داخل `@media (max-width: 719px)` وقبل `}` التي تغلقها، فسطح المكتب واللوح لا
يتغيّران حرفاً. والمحددات كلها محددات المؤلف نفسه من القواعد الأساسية، لا محددات
جديدة. ثم `python 04_Site/build_publish.py`.

**البصمات:**

| الملف | قبل | بعد |
|---|---|---|
| `index.html` | 17,144,749 بايتاً | **17,145,316 بايتاً**، زيادة 567 |
| الرأس | 181,059 حرفاً | 181,626 حرفاً |

**اختبار المتن:**

| | البصمة |
|---|---|
| قبل | `c9a5fa115830c6978d2fdc8c63bb8ff789253cef9dfa82f2023dea7c12ce70fe` |
| بعد | `c9a5fa115830c6978d2fdc8c63bb8ff789253cef9dfa82f2023dea7c12ce70fe` |

**لا تتغيّر.** الأنماط تدخل الرأس وحده، وهذا برهان القيد الأول في هذا البند.

**وإن بُني مع 6.2 في دفعة واحدة:** الحجم 16,173,163 بايتاً، وبصمة المتن
`63026234b7b66fda1ac551e224ff4f289df5aeb6e845e7f9f676991d0a2fe468`، أي بصمة 6.2 وحدها،
لأن 6.4 لا يمسّ المتن.

**القياس، وهو ما يميّز هذا التقرير:** بنيت نسخة من `index.html` بالرقعة مطبّقة،
وفتحتها في كروميوم بعرض 375 بكسل مع `--force-prefers-reduced-motion`، وقِست عليها:

| القياس | قبل | بعد |
|---|---|---|
| عقد نصية حقيقية تحت 12 بكسل، الصفحة مغلقة | 48 | **2** |
| العقد نفسها وحالة دراسية مفتوحة | 56 | **2** |
| أهداف لمس دون 44 بكسل، مغلقة | 2 | **0** |
| أهداف لمس دون 44 بكسل، وحالة مفتوحة | 4 | **0** |
| عرض المستند | 375 | 375، فلا تمرير أفقي |
| ارتفاع الصفحة | 15,362 | 15,391 بكسلاً، زيادة 0.19 بالمئة |

**وفرق عن قياسكم يستحق التسجيل:** التسليم يقول 128 عقدة منها 73 زخرفية فيبقى نحو 55.
والمقيس 120 منها 72 زخرفية فيبقى 48 والصفحة مغلقة، و128 منها 72 فيبقى 56 وحالة
مفتوحة. والفرق حالتان لا تناقض: ثماني عقد تعيش داخل نافذة الحالة. **وأهداف اللمس
الأربعة مطابقة لقياسكم تماماً**، بما فيها زرّا التنقل 327 في 32 داخل النافذة.

**ما لم أفعله ولماذا:** `.card-lockup b` عند 10 بكسل و`.card-lockup i` عند 9.5، وهو
شعار بطاقة واحدة. **رفعه إلى 12 يكسر البطاقة**: السطر الإنجليزي **يفيض اليوم عن
صندوقه بثمانية عشر بكسلاً** عند 9.5 (200 في صندوق 182)، وعند 12 يصير الفيض نحو 71.
والوصول إلى 12 يحتاج التفاف السطر، والالتفاف تغيير مرئي، وهو خارج "تنسيق محض" وخارج
"لا يُعاد تصميم شيء". فتركته ورفعته سؤالاً.

**سؤال معلّق لأحمد:** ثلاثة خيارات مقيسة لشعار البطاقة، وتفصيلها والصورتان في ملف
رقعة 6.4 المرسل. وتوصيتي **الخيار ب**: 12 بكسل مع التفاف، فيصير الشعار 58 بكسلاً وهو
**بالضبط** ارتفاع `.card-logos`، فلا تتحرك البطاقة ولا الصفحة، ويزول فيض قائم اليوم.
وعيبه أنه بلا هامش، فاسم شركة أطول سيُقصّ.

---

## تقرير 3: البند 6.6

```
البند:            6.6، العلامة المتحركة في الترويسة
الحالة:           معاينة جاهزة ومنشورة على الفرع، ورقعة جاهزة، وكلاهما ينتظر كلمة أحمد
```

**ما نفّذته أنا في المستودع:**

الالتزام `7dbdc6d`، وفيه ملفان جديدان ولا تعديل على ملف قائم:

| الملف | الحجم | البصمة |
|---|---|---|
| `media/crane_v12_128_once.gif` | 208,174 بايتاً | `5b474b130c9784d7cc0627a2695438eb2c22654f0a57f7a55b9257949640a057` |
| `preview/header.html` | 11,654 بايتاً | صفحة مؤقتة تُحذف بعد الاعتماد |

**والأصل لم يُمسّ:**

```
$ sha256sum media/crane_v12_128.gif
2f78a9e80b4923d0bcb38b9e6d9a291e80e2883b35222509526de0b67191d4d0  media/crane_v12_128.gif
```

وهي البصمة نفسها في القسم 8.2 من الموافقة.

**كيف صُنعت النسخة، وقد سبق سببه في التقرير العاجل:** بحذف كتلة NETSCAPE كلها، 19
بايتاً، لا بتعديل العدّاد. وبقية الملف مطابقة بايتاً بايتاً، 128 في 128، و48 إطاراً،
بلا إعادة ترميز.

**ما قِسته على المعاينة، في كروميوم، عند 375 و1180 بكسل:**

| القياس | النتيجة |
|---|---|
| الحركة تعمل عند الفتح ثم تهدأ | نعم، تستقر بعد 4.0 ثوانٍ وتبقى ساكنة |
| الإعادة عند مرور المؤشر | نعم، الإطارات تتغيّر ثم تستقر ثانية |
| **الإعادة عند اللمس** | نعم، وهي الطريق الوحيد على الجوال |
| كلفة الإعادة في الشبكة | **صفر طلبات**. طلبان فقط في الجلسة كلها، واحد لكل مسار |
| مع `prefers-reduced-motion` | الإعادة مكبوحة، والحركة لا تُستأنف |

**وملاحظة لازمة على مواصفتكم:** القسم 8.7 يقول إن أحمد يفتح المعاينة من جواله
"ويمرّر مؤشره ليرى الإعادة". **ولا مؤشر في شاشة اللمس، و`mouseenter` لا يقع على
الآيفون.** فربطت الإعادة بالمرور **وباللمس معاً**، وإلا لتعذّر عليه تجربة نصف ما طلب.
وهذا سطر واحد في الرقعة، يُحذف بكلمة إن لم يرده.

**المقاسات الأربعة في المعاينة، والأرقام محسوبة في متصفح القارئ نفسه:**

| الخيار | صندوق الزر | ارتفاع الشريط | موضع بداية الاسم |
|---|---|---|---|
| أ. كما هي اليوم | 50 × 36 | 70.4 | 652 |
| ب. متحركة 24 × 24 | 40 × 36 | 70.4 | 662، أي يزحف عشرة بكسلات |
| **ج. متحركة 24 × 24 والزر محفوظ** | **50 × 36** | **70.4** | **652، لا يتحرك** |
| د. متحركة 28 × 28 | 44 × 40 | 70.4 | 658 |

**فالخيار ج وحده يحقق شرطكم نصاً:** لا يغيّر ارتفاع الشريط ولا يدفع الاسم، لأن صندوق
الزر يبقى 50 في 36 بالضبط. وعليه بنيت الرقعة أدناه، وتغيير الخيار سطر واحد فيها.

**ما يحتاج الجهاز:** ثلاثة ملفات.

### 1. `04_Site/index.html`، بنهايات LF

المرساة، وتظهر مرة واحدة:

```
      <svg viewBox="0 0 44 30" width="34" height="24" fill="none" aria-hidden="true">
        <path class="m-a" d="M3 27 L11 3 L19 27 M6.4 17.5 L15.6 17.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path class="m-slash" d="M19.5 29 L24.5 1" stroke-linecap="round"/>
        <path class="m-a m-a2" d="M25 27 L33 3 L41 27 M28.4 17.5 L37.6 17.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
```

البديل:

```
      <img class="mark-anim" src="https://a-alahmadi.github.io/media/crane_v12_128_once.gif" width="24" height="24" alt="" aria-hidden="true">
```

**المسار مطلق عمداً** فينجو من التضمين ويكلّف الصفحة صفر بايت. ولو ضُمّن لكلّف 277,592
حرفاً. والزر نفسه و`aria-label` و`title` و`id="mark-home"` لا تُمسّ.

### 2. `04_Site/styles.css`، بنهايات CRLF

المرساة الأولى، سطر واحد فريد:

```
  padding: 5px 7px; line-height: 0;
```

البديل:

```
  padding: 5px 7px; line-height: 0; min-width: 50px;
```

المرساة الثانية، كتلة قواعد الرسم كلها، تُحذف وتُستبدل:

```
.mark svg .m-a {
  stroke: var(--text-1); stroke-width: 2.4;
  stroke-dasharray: 70; stroke-dashoffset: 70;
  transition: stroke-dashoffset 900ms var(--ease-out) 150ms, stroke 250ms;
}
.mark svg .m-a2 { transition-delay: 350ms; }
.mark svg .m-slash {
  stroke: var(--accent); stroke-width: 2.4;
  stroke-dasharray: 30; stroke-dashoffset: 30;
  transition: stroke-dashoffset 700ms var(--ease-out) 650ms;
}
.marked .mark svg .m-a, .marked .mark svg .m-slash { stroke-dashoffset: 0; }
.mark:hover svg .m-slash { animation: slash-redraw 700ms var(--ease-out); }
.mark:hover svg .m-a { stroke: var(--accent); }
@keyframes slash-redraw { from { stroke-dashoffset: 30; } to { stroke-dashoffset: 0; } }
```

البديل:

```
.mark .mark-anim { display: block; }
```

المرساة الثالثة، سطر واحد فريد داخل كتلة تقليل الحركة، **يُحذف بلا بديل** لأنه يشير
إلى عنصر لم يعد موجوداً:

```
  .mark svg path { stroke-dashoffset: 0 !important; transition: none; animation: none !important; }
```

### 3. `04_Site/main.js`، بنهايات CRLF

المرساة، وتظهر مرة واحدة:

```
  document.getElementById("mark-home").addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
  });
```

البديل:

```
  /* the mark plays once on load. a second run is a different URL for the same
     file: the browser caches each path, so a replay costs no network request.
     a changing query string would re-download 208 KB every time. */
  var markHome = document.getElementById("mark-home");
  var markImg = markHome.querySelector(".mark-anim");
  var MARK_A = "https://a-alahmadi.github.io/media/crane_v12_128_once.gif";
  var MARK_B = MARK_A + "?r";
  if (markImg) { var warmMark = new Image(); warmMark.src = MARK_B; }
  function replayMark() {
    if (reduced || !markImg) return;
    markImg.src = (markImg.getAttribute("src") === MARK_A) ? MARK_B : MARK_A;
  }
  markHome.addEventListener("mouseenter", replayMark);
  markHome.addEventListener("click", function () {
    replayMark();
    window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
  });
```

ثم:

```
python 04_Site/build_publish.py
```

**البصمات المتوقعة بعد البناء:** لا أستطيع حساب بصمة المتن لهذا البند سلفاً كما فعلت
في 6.2 و6.4، لأن الفرق ليس استبدال نص في المُخرَج وحده: `main.js` يدخل المتن أيضاً،
والكتلة المستبدلة تغيّر طوله. **فالواجب عليكم بعد البناء:** قارنوا المتن قبل وبعد
وأثبتوا أن الفرق محصور في موضعين لا ثالث لهما: **محتوى الزر `#mark-home`**، و**كتلة
معالج العلامة في `main.js` المضمّن**. وأي فرق ثالث يوقف البند.

**والحجم يجب أن ينقص لا أن يزيد:** الصورة تُجلب من `media/` بمسار مطلق، والذي يُحذف
من المستند هو خمسة أسطر SVG وقواعد CSS، والذي يُضاف نحو خمسة عشر سطراً. فالفرق
مئات البايتات لا مئات الكيلوبايتات. **إن زاد المستند بربع ميغابايت فقد ضُمّنت
الصورة، ولا تنشروا.**

**الصفحة الحية:** لم أقسها، للسبب نفسه في التقرير الأول. `curl` يعطي 403 من بوابة
الخروج.

**ما لم أفعله ولماذا:**

- **لم أطبّق الرقعة**، لأن الترويسة في المصدر لا في المستودع.
- **لم أحذف صفحة المعاينة**، لأنها لم تُعتمد بعد. وحذفها في التزام مستقل بعد كلمته.
- **لم أُنشئ نسخة ثانية من الملف بمسار ثانٍ على القرص.** لا حاجة: المسار الثاني هو
  `?r` على الملف نفسه، ويكفي المتصفحَ ليعدّه مورداً آخر، ويكلّف المستودع صفر بايت.

**سؤال معلّق لأحمد، وهو الآن على رأس ما ينتظره:**

1. **أي المقاسات؟** توصيتي **ج**، لأنه وحده لا يحرّك الشريط ولا الاسم.
2. **الإعادة باللمس، أبقيها؟** بلا مؤشر في الجوال، هي الطريق الوحيد ليرى الإعادة.
3. **كيف تريد أن ترى المعاينة؟** هي منشورة على الفرع لا على `main`، وPages تخدم `main`
   وحده، فالرابط `https://a-alahmadi.github.io/preview/header.html` **لا يعمل اليوم**.
   وأمامك طريقان: أن تدمج الفرع في `main` فتصير المعاينة حيّة على جوالك (ومعها ملف
   السيرة، وهو ملف يتيم لا يشير إليه شيء بعد، فلا ضرر)؛ أو أن تكتفي بالتسجيل المرئي
   المرسل معي، وفيه الحركة تعمل مرة ثم تهدأ، ثم لمستان تُعيدانها.

---

## ملحق: المخرج الخام

```
$ curl -sSI https://a-alahmadi.github.io/index.html | grep -i -E "^HTTP|content-length"
curl: (56) CONNECT tunnel failed, response 403
HTTP/1.1 403 Forbidden
Content-Length: 78

$ git rev-parse HEAD origin/main
7dbdc6db3e92b9174e7ba325b8c606f8b145a95f
13fc13684837dc220e5c2861eefd4db619c03daa

$ wc -c < index.html
17144749

$ grep -o 'data:image/jpeg;base64,' index.html | wc -l
98

$ grep -o 'data:image/png;base64,' index.html | wc -l
55

$ grep -o '(expected)' index.html | wc -l
0

$ grep -o '2022 to 2027' index.html | wc -l
1

$ grep -o 'data:application/pdf;base64,' index.html | wc -l
3

$ sha256sum media/*.pdf media/crane_v12_128*.gif
f3bd9804c24bc41ff94a82947b914dff98e275bed37c2327169fe44a63eaa963  media/Ahmad_Al-Ahmadi_CV.pdf
2f78a9e80b4923d0bcb38b9e6d9a291e80e2883b35222509526de0b67191d4d0  media/crane_v12_128.gif
5b474b130c9784d7cc0627a2695438eb2c22654f0a57f7a55b9257949640a057  media/crane_v12_128_once.gif

$ ls -l media/Ahmad_Al-Ahmadi_CV.pdf media/crane_v12_128_once.gif preview/header.html
-rw-r--r-- 1 root root 243058 Sep 29 13:30 media/Ahmad_Al-Ahmadi_CV.pdf
-rw-r--r-- 1 root root 208174 Sep 29 13:47 media/crane_v12_128_once.gif
-rw-r--r-- 1 root root  11654 Sep 29 13:45 preview/header.html

$ git log --oneline -3
7dbdc6d Mark: a single-run copy of the animated mark, and a preview page for it
7d2105e CV: publish the asset as one file in media/ for a stable link
13fc136 Identity: Courier New across the site, and the mark in the footer
```

### الفروق بين نسخ العلامة، قياس الحركة

```
application extension bytes [781, 800) = 21 ff 0b 4e 45 54 53 43 41 50 45 32 2e 30 03 01 00 00 00
loop_forever.gif         208193 bytes  sha256 2f78a9e80b4923d0
loop_1.gif               208193 bytes  sha256 3a3816cd7fb62758
loop_2.gif               208193 bytes  sha256 b8105d1c4eff6b56
no_netscape.gif          208174 bytes  sha256 5b474b130c9784d7

loop forever (original)   distinct frames 15 | last change at 14201ms | settled at the end: false
loop count 1              distinct frames 11 | last change at  8201ms | settled at the end: true
loop count 2              distinct frames 16 | last change at 11800ms | settled at the end: true
no NETSCAPE block         distinct frames  6 | last change at  4001ms | settled at the end: true
```

### قياس المعاينة

```
settled frame            : 3ade5c95
same 1.5s later          : true  (3ade5c95)

--- hover replay ---
frames at +0.7s/+1.5s/+2.3s: 3ade5c95  69cf6746  c4c90a01
any differ from settled    : true  <- replay ran
settles again after replay : true  (3ade5c95)
network requests for it    : 0

--- tap replay (what a phone does) ---
settled 238d90a5 -> after tap: 6fc1f66e  1aae8744  0b92aa80
any differ from settled    : true  <- replay ran
network requests for it    : 0

--- reduced motion ---
replay suppressed for reduced motion: true

all gif requests in the whole session: ["crane_v12_128_once.gif?r","crane_v12_128_once.gif"]
```

### قياس البند 6.4 على المستند المرقّع

```
===== BEFORE =====
doc 375x15362 | first card height 485 | lockup height 25
text under 12px: 48
touch targets under 44px: 2      (4 with a case open)
elements whose content spills its box: 1
   200 in 182  div.card-logos > span.card-lockup > i  "Advanced Horizons Contracting "

===== AFTER patch, lockup untouched =====
doc 375x15391 | first card height 486 | lockup height 25
text under 12px: 2
   x1  10px div.card-logos > span.card-lockup > b
   x1  9.5px div.card-logos > span.card-lockup > i
touch targets under 44px: 0
elements whose content spills its box: 1   (the one that was already there)

===== AFTER patch + lockup raised to 12px with wrapping =====
doc 375x15391 | first card height 486 | lockup height 58
text under 12px: 0
touch targets under 44px: 0
elements whose content spills its box: 0
```

### البصمات المحسوبة للبنائات المتوقعة

```
now (13fc136)                bytes     17144749   head   181059   body sha256 c9a5fa11...ce70fe
6.4 alone                    bytes     17145316   head   181626   body sha256 c9a5fa11...ce70fe
6.2 alone                    bytes     16172596   head   181059   body sha256 63026234...2fe468
6.2 + 6.4 together           bytes     16173163   head   181626   body sha256 63026234...2fe468
```
