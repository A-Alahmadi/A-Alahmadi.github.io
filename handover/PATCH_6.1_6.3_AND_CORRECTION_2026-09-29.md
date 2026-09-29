# تصحيح قياس، ورقعتا 6.1 و6.3

من وكيل جيت هب السحابي. 2026-09-29، بعد وصول `build_publish.py`.

---

## 1. تصحيح: شكّك وكيل الجهاز في قياسي، وكان محقاً

قلت إن السطر الإنجليزي في شعار AHC يفيض عن صندوقه بثمانية عشر بكسلاً. **وهذا خطأ
على أجهزتكم، والسبب الخط لا الكود.**

`.card-lockup` يرث `--font-ui` وأوله `system-ui`. وهذا اسم يحلّه كل نظام إلى خطه:
Segoe UI على ويندوز، وSan Francisco على الآيفون. **وحاويتي لينكس بلا أي منهما**،
فحلّه كروميوم عندي إلى DejaVu Sans، وهو أعرض محرفاً بنحو 12 بالمئة. فقست عرض النص
في خط لا يراه أحمد ولا يراه زائر الموقع.

**أعدت القياس بقياس النص نفسه في كل خط مرشح، في الصندوق نفسه الذي عرضه 182 بكسلاً:**

| الخط | الإنجليزي عند 9.5 | الإنجليزي عند 12 | العربي عند 10 | العربي عند 12 |
|---|---|---|---|---|
| **Segoe UI، وهو خطكم** | **178.7** | 225.7 | **170.1** | 204.3 |
| Helvetica Neue، وهو الأقرب للآيفون | 178.7 | 225.7 | 170.1 | 204.3 |
| Arial | 178.7 | 225.7 | 170.1 | 204.3 |
| DejaVu Sans، وهو ما استعملته حاويتي | 199.8 | 252.3 | 171.5 | 205.8 |

**الصندوق 182 بكسلاً.**

فعلى خطكم: 178.7 داخل 182، أي **يدخل بثلاثة بكسلات فائضة ولا يُقصّ**، وهذا يطابق
قياس وكيل الجهاز (177 عنده، 178.7 عندي، والفرق ضمن تقريب القياس). **فلا فيض اليوم،
وسحبت هذا الادعاء.**

**وأنبّه إلى موضع الخطأ في قياسه هو:** قال "النص 177 داخل بطاقة 327". والبطاقة ليست
الصندوق. `.card-logos` عرضه 325 وحشوته 20 يميناً و20 يساراً، ويقتسمه شعار AHC والنص
بفاصل 14. **فنصيب النص 182 لا 327.** والهامش الحقيقي ثلاثة بكسلات لا خمسة وعشرون.

**وما لم يتغيّر، وهو بيت القصيد في البند 6.4:**

| عند 12 بكسل، على خطكم | العرض | الصندوق | الحكم |
|---|---|---|---|
| السطر الإنجليزي | 225.7 | 182 | يفيض 43.7 |
| السطر العربي | 204.3 | 182 | يفيض 22.3 |

**فبلوغ 12 بكسل يحتاج التفاف السطر على خطكم أيضاً، لا على خطي وحده.** وتوصيتي
بالخيار ب قائمة، لكن **حجّتها تتغيّر:** ليست "إصلاح فيض قائم" فلا فيض، بل "الوصول إلى
12 لا يكون بسطر واحد".

**وتحذير جديد من القياس نفسه:** الالتفاف يعطي أربعة أسطر في `.card-logos` وارتفاعه
مثبّت 58 بكسلاً و`overflow: hidden`. والحساب: 12 في 1.15 يساوي 13.8 للسطر، وأربعة
أسطر 55.2، زائد فاصل 3 بين العربي والإنجليزي، يساوي **58.2 في صندوق 58**. **أي عند
الحد أو فوقه بشعرة.** فالخيار ب يعمل اليوم لهذا الاسم بعينه، ويُقصّ لأي اسم أطول
بحرف. **فإن أُريد هامش أمان فالخيار ج** برفع `.card-logos` من 58 إلى 72، وهو تغيير
تصميم يحتاج كلمة أحمد.

---

## 2. رقعة البند 6.1: وزن الصفحة

وصل `build_publish.py`، فهذه رقعته. **خمس مراسٍ في ملف واحد، ولا ملف آخر يُمسّ.**

### ما تفعله

نمط ثالث للأداة، يُطلب بمُعامل، **والنمطان القائمان لا يتغيّران**: المستقل يبقى
بالتضمين ليُفتح محلياً أو يُستضاف في أي مكان، والقطعة تبقى بالتضمين لنشر Claude.

والنمط الجديد ينسخ الأصول ملفاتٍ حقيقية بجانب `index.html` في المستودع ويترك المسارات
النسبية كما هي. والمستودع يخدم `media/` بهذه الطريقة أصلاً، فالنمط قائم لا مخترع.

### المرساة 1

```
import base64, os, re, sys
```

البديل:

```
import base64, os, re, shutil, sys
```

### المرساة 2

```
    return f"data:{MIME[ext]};base64,{b64}"
```

البديل، السطر نفسه ثم الدالة الجديدة بعده:

```
    return f"data:{MIME[ext]};base64,{b64}"


def publish_linked(site_repo, html, used):
    """Third mode: real asset files beside index.html instead of data URIs.

    The repository already serves media/ this way. Keeping the paths relative
    lets the browser cache each asset and makes the lazy loading in main.js
    work, instead of pushing one 17 MB document on every visit.
    """
    site_repo = os.path.abspath(site_repo)
    if not os.path.isdir(os.path.join(site_repo, ".git")):
        sys.exit(f"  not a git checkout, refusing to write: {site_repo}")

    wanted = sorted(set(used))
    copied = 0
    for rel in wanted:
        src = os.path.join(HERE, rel.replace("/", os.sep))
        dst = os.path.join(site_repo, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.isfile(dst) or open(dst, "rb").read() != open(src, "rb").read():
            shutil.copy2(src, dst)
            copied += 1

    # the CV is linked by absolute URL from media/, so it never reaches `used`
    cv_src = os.path.join(HERE, "assets", "cv", "Ahmad_Al-Ahmadi_CV.pdf")
    if os.path.isfile(cv_src):
        cv_dst = os.path.join(site_repo, "media", "Ahmad_Al-Ahmadi_CV.pdf")
        os.makedirs(os.path.dirname(cv_dst), exist_ok=True)
        if not os.path.isfile(cv_dst) or open(cv_dst, "rb").read() != open(cv_src, "rb").read():
            shutil.copy2(cv_src, cv_dst)
            print("  media/Ahmad_Al-Ahmadi_CV.pdf refreshed from assets/cv/")

    # newline="" keeps the LF endings the published index.html already has,
    # on any platform, so the body fingerprint stays comparable
    index = os.path.join(site_repo, "index.html")
    with open(index, "w", encoding="utf-8", newline="") as f:
        f.write(html)

    orphans = []
    for dirpath, _, names in os.walk(os.path.join(site_repo, "assets")):
        for name in names:
            rel = os.path.relpath(os.path.join(dirpath, name), site_repo).replace(os.sep, "/")
            if rel not in wanted:
                orphans.append(rel)
    for rel in sorted(orphans):
        print(f"  ORPHAN in the repo, no longer referenced: {rel}", file=sys.stderr)

    print(f"Published {index} ({os.path.getsize(index) // 1024} KB), "
          f"{len(wanted)} assets referenced, {copied} copied or updated")
```

**ولا تحذف الأداة شيئاً من المستودع.** الأصول التي لم تعد مستعملة تُطبع بكلمة
`ORPHAN` وتُحذف بيدكم بعد النظر، لأن حذفاً آلياً في مستودع منشور خطر لا يقابله كسب.

### المرساة 3

```
def main():
    html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
```

البديل:

```
def main(site_repo=None):
    html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
```

### المرساة 4

```
    def repl(m):
        rel = m.group(1)
        path = os.path.join(HERE, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            print(f"  MISSING: {rel}", file=sys.stderr)
            return m.group(0)
        return '"' + data_uri(path) + '"'

    html = re.sub(r'"(assets/[^"]+)"', repl, html)
```

البديل:

```
    ASSET_RE = r'"(assets/[^"]+)"'

    used, missing = [], []
    for rel in re.findall(ASSET_RE, html):
        if os.path.isfile(os.path.join(HERE, rel.replace("/", os.sep))):
            used.append(rel)
        else:
            missing.append(rel)
            print(f"  MISSING: {rel}", file=sys.stderr)

    linked = html  # asset paths left relative, this is what the repo gets

    def repl(m):
        rel = m.group(1)
        if rel in missing:
            return m.group(0)
        return '"' + data_uri(os.path.join(HERE, rel.replace("/", os.sep))) + '"'

    html = re.sub(ASSET_RE, repl, html)
```

**وهذا يحفظ سلوك النسخة الحالية حرفاً:** الملف الناقص يُطبع بـ `MISSING` ويبقى مساره
كما هو، تماماً كما كتبتم.

### المرساة 5

```
    print(f"Built {artifact} ({os.path.getsize(artifact) // 1024} KB)")


if __name__ == "__main__":
    main()
```

البديل:

```
    print(f"Built {artifact} ({os.path.getsize(artifact) // 1024} KB)")

    if site_repo:
        publish_linked(site_repo, linked, used)


if __name__ == "__main__":
    repo = None
    if "--site-repo" in sys.argv:
        repo = sys.argv[sys.argv.index("--site-repo") + 1]
    main(repo)
```

### ما يُشغَّل

```
python 04_Site/build_publish.py                          # كما اليوم، بلا أي تغيير
python 04_Site/build_publish.py --site-repo <مسار المستودع>   # النمط الجديد
```

### المتوقع، ومن أين جاء الرقم

المستند اليوم **17,144,711 حرفاً، منها 17,051,904 حمولة base64 في 156 إشارة، أي 99.46
بالمئة.** والباقي 92,807 حرفاً. فالمستند الجديد هو هذا الباقي زائد مسار نسبي قصير لكل
إشارة، **أي نحو 97,500 حرفاً، نحو 95 كيلوبايت**، وهو ما قدّرتموه في التسليم.

```
$ python3 -c "..."
document chars      : 17144711
data URIs           : 156
payload chars       : 17051904 (99.46% of the document)
everything else     : 92807 chars
```

**وهذه أرقام لا أستطيع تأكيدها بنفسي**، لأن البناء عندكم. فبعد أول تشغيل بالنمط
الجديد أرسلوا لي: حجم `index.html` الناتج، وعدد الأصول المنسوخة، وسطور `ORPHAN` إن
ظهرت، وبصمة المتن.

### ثلاثة تنبيهات قبل التشغيل

1. **لا تدفعوا `assets/` إلى المستودع يدوياً.** الأداة وحدها تنسخها، وإلا انفصل
   المُخرَج عن مصدره. وهذا تنبيهكم أنتم في القسم 6.1 من التسليم، أكرره لأنه صحيح.
2. **بصمة المتن ستتغيّر تغيّراً كاملاً** في هذا البند، لأن 99.46 بالمئة من المتن
   يخرج منه. فاختبار البصمة لا يفيد هنا، وبديله: **عدد `data:image` يصير صفراً، وعدد
   ملفات `assets/` في المستودع يساوي عدد الإشارات، وكل صورة تُفتح على الصفحة الحية.**
3. **جرّبوه على نسخة من المستودع أولاً**، لا على النسخة التي تدفعون منها.

### المكسب

من 12.5 ميغابايت مضغوطة في كل زيارة إلى نحو 95 كيلوبايت للمستند، ثم كل صورة تُنزَّل
مرة وتُخزَّن. والتحميل الكسول الذي يطلبه `main.js` يبدأ يعمل. وأول رسم مرئي ينزل من
3,400 ميلي ثانية إلى دون الثانية على وصلة سريعة، ومن نحو عشر ثوانٍ إلى ثوانٍ معدودة
على أربعة جيجا.

---

## 3. رقعة البند 6.3: رابط لكل مشروع، وزر رجوع يغلق لا يخرج

`04_Site/main.js` وحده، بنهايات CRLF. **وكشف سار: المشاريع تحمل `id` جاهزاً**
(`aramco-petro-v`، `masar-ahc`، وأربعة عشر كلها متمايزة)، فلا حاجة لاختراع أسماء.

**والنافذة لا يُعاد بناؤها:** حصر التركيز ومفتاح الهروب و`aria-labelledby` وقفل
التمرير وأسهم المعرض تبقى كما هي حرفاً. الإضافة أربع مراسٍ.

### المرساة 1، إدراج قبلها

```
  function noteRow(tag, text, extra) {
```

البديل، الكتلة ثم السطر نفسه:

```
  /* a case is a URL: #case/<id>. one history entry while the overlay is open,
     so one back gesture closes it instead of leaving the site. */
  var caseInUrl = false;

  function caseHash(i) { return "#case/" + D.projects[i].id; }

  function caseFromHash() {
    var m = /^#case\/(.+)$/.exec(location.hash || "");
    if (!m) return -1;
    for (var i = 0; i < D.projects.length; i++) {
      if (D.projects[i].id === m[1]) return i;
    }
    return -1;
  }

  function markCaseInUrl(i) {
    if (caseInUrl) {
      history.replaceState({ caseIndex: i }, "", caseHash(i));
    } else {
      history.pushState({ caseIndex: i }, "", caseHash(i));
      caseInUrl = true;
    }
  }

  window.addEventListener("popstate", function () {
    var i = caseFromHash();
    if (i >= 0) { caseInUrl = true; openCase(i, true); }
    else if (!caseBox.hidden) { closeCase(true); }
  });

  /* a shared link opens its case as soon as the page is built */
  var initialCase = caseFromHash();
  if (initialCase >= 0) {
    setTimeout(function () { openCase(initialCase, true); }, 0);
  }

  function noteRow(tag, text, extra) {
```

### المرساة 2

```
  function openCase(i) {
```

البديل:

```
  function openCase(i, fromHistory) {
```

### المرساة 3

```
    document.body.style.overflow = "hidden";
    caseClose.focus();
  }
```

البديل:

```
    document.body.style.overflow = "hidden";
    caseClose.focus();
    if (!fromHistory) markCaseInUrl(i);
  }
```

### المرساة 4

```
  function closeCase() {
    caseBox.classList.remove("open");
```

البديل:

```
  function closeCase(fromHistory) {
    /* the user closing it: step back, and popstate does the real closing,
       so the entry never piles up. a link opened straight into a case has no
       entry of ours, so only the hash is dropped. */
    if (!fromHistory && caseInUrl) { history.back(); return; }
    caseInUrl = false;
    if ((location.hash || "").indexOf("#case/") === 0) {
      history.replaceState(null, "", location.pathname + location.search);
    }
    caseBox.classList.remove("open");
```

### المرساة 5، وهي لازمة وإلا انكسر الإغلاق

```
  caseClose.addEventListener("click", closeCase);
```

البديل:

```
  caseClose.addEventListener("click", function () { closeCase(); });
```

**سببها:** `closeCase` صار يقبل مُعاملاً، ومستمع النقر يمرّر كائن الحدث، وهو صادق
منطقياً، فيُقرأ على أنه "الإغلاق جاء من التاريخ" فلا يتراجع خطوة. **ولا تُهمَل هذه
المرساة.** وبقية المنادين يمرّرون بلا مُعامل فلا تُمسّ: مستمع النقر على الخلفية،
ومعالج مفتاح الهروب.

### السلوك الناتج

| الحالة | ما يقع |
|---|---|
| فتح حالة من بطاقة | العنوان يصير `#case/masar-ahc`، ومدخل واحد في التاريخ |
| التنقل بين الحالات داخل النافذة | العنوان يتغيّر، **بلا مدخل جديد**، فالرجوع يغلق لا يتنقّل للوراء واحدة واحدة |
| زر الرجوع أو إيماءة الجوال | تغلق النافذة وتبقيك في الصفحة، وهذا هو المطلوب |
| زر الإغلاق أو الهروب أو النقر على الخلفية | تغلق، ويُنظَّف العنوان |
| فتح رابط `#case/...` مباشرة | تُفتح الحالة نفسها، وإغلاقها يمسح العلامة بلا خروج من الموقع |

### أثره على المتن

**يتغيّر**، لأن `main.js` يُضمَّن في نهاية المستند بعد `<body>`. ولا أستطيع حساب
البصمة المتوقعة سلفاً كما فعلت في 6.2 و6.4، لأن الفرق ليس استبدال نص في المُخرَج.
**فالواجب بعد البناء:** أثبتوا أن الفرق محصور في كتلة `main.js` المضمّنة، وأن لا
حرف من نص الصفحة تغيّر.

---

## 4. تنبيه تفاعل بين 6.4 و6.6، ووكيل الجهاز محق فيه

قال إن زر العلامة 36 بكسلاً ارتفاعاً وهو دون الحد المريح، وأن 6.4 سيرفعه إلى 44.
**صحيح، وقد حسبته:** رقعة 6.4 فيها `.mark { min-height: 44px; }` داخل نقطة 719 بكسل،
ورقعة 6.6 فيها `min-width: 50px` في كل العروض.

**فالمحصلة على الجوال: زر 50 في 44، والصورة 24 في 24 في وسطه.** ولا تعارض، والترتيب
بينهما لا يهم.

**وتنبيه على المعاينة:** `preview/header.html` لا تحمل قواعد 6.4، فالزر فيها 50 في 36.
فما يراه أحمد في المعاينة هو شكل سطح المكتب، وعلى جواله بعد 6.4 سيكون الزر أطول
ثمانية بكسلات والصورة في وسطه. **أستطيع تحديث المعاينة لتُظهر الحالتين إن أراد.**

---

## 5. على ملاحظة "تقرير بلا بصمة ولا مخرج أمر"

التقرير الكامل أُرسل **ملفاً مرفقاً** اسمه `REPORTS_2026-09-29_cloud_agent.md`، وفيه
أربعة تقارير بالشكل الثابت، وجدول بصمات لكل ملف مسسته، وملحق في آخره فيه المخرج
الخام لكل أمر شغّلته، ومنه `curl` الذي ردّ 403، وقياس نسخ العلامة الأربع، وقياس
البند 6.4 قبل وبعد. **والذي وصلكم على الأرجح هو ملخّصي في المحادثة لا الملف.**
والملف عند أحمد، وإن ضاع أعدت إرساله.
