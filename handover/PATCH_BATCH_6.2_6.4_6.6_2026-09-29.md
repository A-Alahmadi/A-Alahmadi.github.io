# الدفعة الواحدة: البنود 6.2 و6.5أ و6.4 و6.6

من وكيل جيت هب السحابي. 2026-09-29. **يحلّ محل رقعتَي 6.2 و6.4 المرسلتين قبله**،
لأن قرارَي أحمد دخلا فيهما، ولأن بصمة الدفعة محسوبة مجتمعة لا مفرّقة.

ثلاثة ملفات مصدر تُمسّ: `04_Site/index.html` و`04_Site/styles.css` و`04_Site/main.js`.
والبناء مرة واحدة، والنشر التزام واحد.

---

## 0. ما نُشر على `main` قبل هذه الرقعة

بطلب أحمد أن يرى العلامة على الموقع لا في فيديو.

```
$ git log --oneline -1
29472b2 Preview: publish the header mark preview page and its assets

$ git diff --stat 13fc136 HEAD
 media/Ahmad_Al-Ahmadi_CV.pdf | Bin 0 -> 243058 bytes
 media/crane_v12_128_once.gif | Bin 0 -> 208174 bytes
 preview/header.html          | 264 +++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 264 insertions(+)

$ git diff --stat 13fc136 HEAD -- index.html
(لا مخرج: الملف مطابق بايتاً بايتاً)
```

**و`index.html` لم يُمسّ**، كما اشترطتم. والرابط لأحمد:
`https://a-alahmadi.github.io/preview/header.html`

**والعلامة المتحركة لزمت `main` معها** لأن صفحة المعاينة تحمّلها، وهي ملف جديد لا
يشير إليه شيء في الصفحة الحية. **وملف السيرة كذلك** ذهب معها، وهو ملف يتيم حتى تُطبَّق
رقعة 6.2، **وهذا في صالح الترتيب**: كنت نبّهت أن الملف يجب أن يسبق `index.html` المبني
وإلا صار الرابط الجديد 404، وقد سبقه الآن.

**وصفحة المعاينة تُحذف** في التزام مستقل فور اعتماد المقاس، وهي أول ما أحذفه.

---

## 1. البند 6.2 مع 6.5أ: `04_Site/index.html` و`04_Site/site-data.js`

### المرساة 1، مسار السيرة

سطر واحد بلا سطر جديد داخله، فلا تتأثر بنهايات الأسطر:

```
assets/cv/Ahmad_Al-Ahmadi_CV.pdf
```

البديل:

```
https://a-alahmadi.github.io/media/Ahmad_Al-Ahmadi_CV.pdf
```

| الملف | العدد المتوقع | الموضع |
|---|---|---|
| `04_Site/index.html` | 2 | `class="nav-cv"` و`id="cv-btn"`، في `href` وحدها |
| `04_Site/site-data.js` | 1 | السطر 17، حقل `cv:` |

**توقّفوا ولا تطبّقوا إن اختلف العدد.**

### المرساة 2، اسم التنزيل، وهو البند 6.5أ

في `04_Site/index.html` وحده، ويظهر مرة واحدة:

```
download="Ahmad_Al-Ahmadi_CV.pdf"
```

البديل:

```
download="Ahmad_Al-Ahmadi_Project_and_Operations_Manager_CV.pdf"
```

فيصير الرابطان على اسم واحد، وهو الطويل، ولا يعود الاسم المحفوظ تابعاً للزر المضغوط.

**ولا تمسّوا** `a.getAttribute("download") || "Ahmad_Al-Ahmadi_CV.pdf"` في `main.js`:
هو احتياط لرابط بلا خاصية `download`، ويصير بلا عمل بعد 6.2 لأن المعالج يتنحّى
للروابط الحقيقية. تنظيفه خارج هذه البنود.

---

## 2. البند 6.4: `04_Site/styles.css`، بنهايات CRLF

ثلاث مراسٍ، كلها داخل `@media (max-width: 719px)`، وتحققت أن كلاً منها تظهر مرة واحدة.

### المرساة 1

```
  .btn-small { padding: 9px 12px; font-size: 10.5px; }
```

البديل:

```
  .btn-small { padding: 9px 12px; font-size: 12px; }
```

### المرساة 2، شعار البطاقة، وهو الخيار ب الذي اعتمده أحمد

```
  /* a narrow card leaves the lockup about seven pixels short, so the two lines
     and the gap give that back rather than letting the name clip */
  .card-logos { gap: 12px; }
  .card-lockup b { font-size: 10px; }
  .card-lockup i { font-size: 9.5px; }
```

البديل:

```
  /* the name is readable at 12px, which no longer fits on one line in the
     space the logo leaves, so both lines wrap instead of being shrunk to fit */
  .card-logos { gap: 12px; height: auto; min-height: 58px; }
  .card-lockup b, .card-lockup i { white-space: normal; }
  .card-lockup b { font-size: 12px; }
  .card-lockup i { font-size: 12px; }
```

**وسطر `height: auto; min-height: 58px` لازم، وهذه قصته.** طبّقت الخيار ب وحده وقِست
فوجدته **يُقصّ**: `.card-logos` ارتفاعه مثبّت 58 و`overflow: hidden`.

| العرض | ارتفاع الشعار بعد الالتفاف | القصّ بالخيار ب وحده |
|---|---|---|
| 320 بكسل | 72 (الإنجليزي ثلاثة أسطر) | **يُقصّ 8 بكسلات** |
| 375 بكسل | 58.2 | **يُقصّ بكسل واحد** |
| 414 بكسل | 44.4 | لا يُقصّ |

وبالسطر المضاف: **لا قصّ عند أي من الثلاثة**. والثمن أن شريط الشعار يطول في البطاقة
الواحدة التي فيها شعار: 15 بكسلاً عند 320، و1.2 عند 375، **وصفر عند 414 فما فوق**.
ولا بطاقة أخرى تتأثر، ولا يتغيّر شيء على سطح المكتب.

### المرساة 3، إدراج بعدها

```
  .hero { padding: 64px 0 56px; }
```

البديل، السطر نفسه ثم الكتلة بعده:

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

**والكتلة تُكتب بنهايات الملف، أي CRLF**، وتسبق `}` التي تغلق نقطة التوقف.

---

## 3. البند 6.6: المقاس ج الذي اعتمده أحمد

### `04_Site/index.html`، بنهايات LF

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

المسار مطلق عمداً فينجو من التضمين ويكلّف الصفحة صفر بايت. و`width` و`height` مكتوبتان
في الوسم عمداً أيضاً: الصندوق يبقى 24 في 24 حتى قبل أن تصل الصورة، فلا يقفز شيء.

### `04_Site/styles.css`، بنهايات CRLF

المرساة الأولى، سطر واحد فريد:

```
  padding: 5px 7px; line-height: 0;
```

البديل:

```
  padding: 5px 7px; line-height: 0; min-width: 50px;
```

المرساة الثانية، كتلة قواعد الرسم كلها:

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

المرساة الثالثة، سطر واحد فريد داخل كتلة تقليل الحركة، **يُحذف بلا بديل**:

```
  .mark svg path { stroke-dashoffset: 0 !important; transition: none; animation: none !important; }
```

**وبعد هذه الثلاث لا يبقى في التنسيق حرف يشير إلى العلامة المرسومة.** ويبقى في
`main.js` سطر `document.body.classList.add("marked")` بلا قاعدة تستعمله، وحذفه
اختياري وخارج هذه الرقعة، فاتركوه أو احذفوه كما ترون.

### `04_Site/main.js`، بنهايات CRLF

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

**والإعادة مربوطة بالمرور وباللمس معاً**، لأن `mouseenter` لا يقع على الآيفون.
وحذفُ اللمس سطر واحد إن لم يُرد.

---

## 4. ما يُشغَّل، ثم ما يجب أن يخرج

```
python 04_Site/build_publish.py
```

**بنيت المستند المتوقع بتطبيق هذه الرقع الثلاث نفسها على `index.html` المنشور،
وقِست الملف الناتج. فهذه ليست تقديرات:**

| القياس | الآن | بعد الدفعة |
|---|---|---|
| حجم `index.html` | 17,144,749 بايتاً | **16,172,974 بايتاً** |
| **بصمة المتن** | `c9a5fa11...ce70fe` | **`35a44581b08e54a64414d8d92f2c701d7b66588905067e49de8080ff7f75448d`** |
| `data:image/jpeg;base64,` | 98 | 98 |
| `data:image/png;base64,` | 55 | 55 |
| `data:application/pdf;base64,` | 3 | **0** |
| `(expected)` | 0 | 0 |
| `2022 to 2027` | 1 | 1 |
| رابط السيرة المطلق | 0 | **3** |
| `crane_v12_128_once.gif` | 0 | **2**، واحد في الوسم وواحد في `main.js` |
| `<svg viewBox="0 0 44 30"` | 1 | **0** |
| `slash-redraw` | 2 | **0** |

**بصمة المتن تتغيّر، وهذه أسبابها الثلاثة مجتمعة ولا رابع لها:** النسخ الثلاث من
السيرة تخرج من المتن، ومحتوى زر العلامة يتبدّل، وكتلة معالج العلامة في `main.js`
المضمّن تتبدّل. **ولا حرف واحد من نص الصفحة يتغيّر:** لا عنوان، ولا بند مشروع، ولا
تعليق صورة، ولا رقم.

**وإن اختلف الحجم أو البصمة عن هذين الرقمين فشيء آخر تغيّر مع الرقع، فلا تنشروا
وأرسلوا لي الفرق.**

**وإن أردتم 6.4 وحده للمقارنة:** 17,145,412 بايتاً، وبصمة المتن `c9a5fa11...ce70fe`
كما هي بلا تغيير، لأن الأنماط تدخل الرأس وحده.

---

## 5. ما قِسته على المستند المرقّع، وبأي عرض

**وأجيب هنا سؤالكم عن العرض، وهو سؤال في محلّه.**

فتحت المستند المرقّع في كروميوم بـ `--force-prefers-reduced-motion`، عند ثلاثة عروض:

| القياس | 320 بكسل | 375 بكسل | 414 بكسل |
|---|---|---|---|
| نصوص حقيقية تحت 12 بكسل | **0** | **0** | **0** |
| أهداف لمس دون 44 بكسل | **0** | **0** | **0** |
| عرض المستند، أي تمرير أفقي | 320 | 375 | 414 |
| صندوق `#mark-home` | **50 × 44** | **50 × 44** | **50 × 44** |
| قصّ في شعار البطاقة | لا | لا | لا |

**و50 في 44 هو تحديداً ما نبّهتم إليه:** `min-width: 50px` من 6.6 مع `min-height: 44px`
من 6.4، فالزر يبلغ الحد المريح على الجوال والصورة 24 في 24 في وسطه. **والمعاينة
المنشورة لا تحمل قواعد 6.4**، فالزر فيها 50 في 36، وهو شكل سطح المكتب. **أستطيع تحديث
المعاينة لتعرض الحالتين إن أراد أحمد**، وهي كلمة منه.

---

## 6. تصحيح ادعائي عن شعار AHC، والجواب عن سؤال العرض

**قست عند 375 بكسل، وقياسي كان خاطئاً، والسبب الخط لا العرض.**

`.card-lockup` يرث `--font-ui` وأوله `system-ui`، وهو اسم يحلّه كل نظام إلى خطه:
Segoe UI عندكم، وSan Francisco على الآيفون. **وحاويتي لينكس بلا أي منهما**، فحلّه
كروميوم إلى DejaVu Sans، وهو أعرض بنحو 12 بالمئة. فقست عرض النص في خط لا يراه أحد.

أعدت القياس بقياس النص نفسه في كل خط مرشح، في الصندوق نفسه:

| الخط | الإنجليزي عند 9.5 | الإنجليزي عند 12 | العربي عند 10 | العربي عند 12 |
|---|---|---|---|---|
| **Segoe UI، خطكم** | **178.7** | 225.7 | 170.1 | 204.3 |
| Helvetica Neue، الأقرب للآيفون | 178.7 | 225.7 | 170.1 | 204.3 |
| DejaVu Sans، خط حاويتي | 199.8 | 252.3 | 171.5 | 205.8 |

**الصندوق 182 بكسلاً.** فعلى خطكم 178.7 يدخل بثلاثة بكسلات، **ولا فيض، وسحبت
الادعاء**. وقياسكم 177 وقياسي 178.7، والفرق تقريب.

**وأنبّه إلى موضع في قياسكم:** قلتم "177 داخل بطاقة 327". والبطاقة ليست الصندوق:
`.card-logos` عرضه 325 وحشوته 20 من كل جهة، ويقتسمه شعار AHC والنص بفاصل 14، **فنصيب
النص 182 لا 327**. فالهامش ثلاثة بكسلات لا خمسة وعشرون، وهو أضيق مما يبدو.

**وما لم يتغيّر:** عند 12 بكسل وعلى خطكم، الإنجليزي 225.7 والعربي 204.3 في صندوق 182،
فكلاهما يحتاج الالتفاف. **فالخيار ب صحيح، وحجّته "لا يُبلَغ 12 بسطر واحد" لا "إصلاح
فيض قائم".**

**والتزاماً بشرطكم من الآن: كل قياس أذكره سيحمل عرض النافذة والخط الذي حُلّ إليه
`system-ui`.**

---

## 7. الترتيب كما طلبتم

| الدفعة | ما فيها | لماذا |
|---|---|---|
| **الآن** | حذف `preview/` بعد كلمة أحمد | أول ما أحذفه |
| **1** | هذه الرقعة: 6.2 و6.5أ و6.4 و6.6 | بناء واحد ونشر واحد، والبصمة المتوقعة في القسم 4 |
| **2** | 6.3 وحده | يمسّ المتن وحده فيستحق مقارنة معزولة. رقعته مرسلة |
| **3** | 6.1 في جلسة مستقلة | رقعته مرسلة بعد قراءة `build_publish.py` |

و**6.5ب**، أي `LINK_USAGE.md`، ليس لي بنصكم، ولم أكتب فيه حرفاً.
