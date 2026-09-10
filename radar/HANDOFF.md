# رادار شقق العليا: ملف التسليم لجلسة جديدة

آخر تحديث: 2026-09-10. الحالة: الملف منشور ومكتمل بنسخة 6، وبقيت ثلاث مهام تحتاج شبكة مفتوحة وشريكاً مسجل الدخول.

## 1. الهدف
أحمد يبحث عن استديو أو غرفة وصالة، إيجار شهري للعزاب، ضمن 10 إلى 15 دقيقة بالسيارة من برج المملكة، طريق الملك فهد، الرياض (24.7114, 46.6745).
الأحياء: العليا، السليمانية، الورود، المروج، الملك فهد، المحمدية، الرحمانية، المعذر الشمالي، النخيل، التعاون، المصيف، الوزارات.
المنصات: حراج، عقار، بيوت، Property Finder، Airbnb، مبيت.
القواعد: صفر تلفيق، أي حقل غائب يُكتب "غير مذكور"، بدون شرطات طويلة ولا إيموجي، حذف المنتهي والسنوي فقط، تعليم "عوائل فقط".

## 2. المخرج
- الرابط الثابت (يُحدَّث بتمرير url عند النشر): https://claude.ai/code/artifact/295bf060-95e0-4dca-926e-b952cd0b56c9
- النسخة 6: 397 إعلاناً مفتوحاً، 41 محذوفاً من قائمة الـ47 السابقة بأسبابها في جدول داخل الصفحة.
- التوزيع: Airbnb 135، عقار 92، بيوت 81، مبيت 68، حراج 21. بسعر ظاهر 392. بصورة مصغرة مضمنة 382.
- البنية: بطاقات الأحياء (12 حياً مرتبة بالمسافة) ثم تبويب النوع ثم تبويب المنصة، مع تجميع البطاقات تحت عناوين، وفلاتر: الحد الأعلى، الفرش، الترتيب، بسعر ظاهر، استبعاد عوائل فقط (مفعّل افتراضياً)، الجديد فقط، الموثوق فقط.
- سطر "التحقق" على كل بطاقة يذكر كيف ثبت أن الإعلان قائم.
- معايير "الموثوق": Airbnb تقييم 4.8 مع 10 مراجعات فأكثر، مبيت 4.5 مع 5 مراجعات، بيوت رقم ظاهر ونشر خلال 120 يوماً، حراج رخصة إعلان أو رقم ظاهر مع ظهور في البحث الحي، عقار معلن مسمى وسعر شهري صريح بلا عقد سنوي مقسط. النتيجة 189 من 397.

## 3. المهام المتبقية بالترتيب
1. فتح الشبكة: claude.ai/code ثم Environments ثم تعديل البيئة، Network access إلى Full أو Allowlist بالنطاقات: haraj.com.sa, sa.aqar.fm, www.bayut.sa, www.propertyfinder.sa, ar.airbnb.com, mabet.com.sa, app.mabet.com.sa, images.aqar.fm, images.bayut.sa, a0.muscache.com, img4cdn.haraj.com.sa, mabet.b-cdn.net. ثم جلسة جديدة.
2. ربط الشريك: Codex مثبّت بالأمر npm i -g @openai/codex (0.154.0). في السحابة يلزم متغير بيئة OPENAI_API_KEY في إعدادات البيئة ثم: printenv OPENAI_API_KEY | codex login --with-api-key. ثم: bash bridge/scripts/bridge.sh selftest. لا يُكتب المفتاح في الدردشة أو الملفات أبداً.
3. إعادة التحقق بعد فتح الشبكة:
   - حراج: تشغيل radar/scripts/pw_hverify.js على إعلانات حراج الـ21 (المتصفح الحقيقي) وحذف ما يظهر فيه "الإعلان غير موجود" أو ما يغيب عن نتائج البحث الحية. ملاحظة مؤكدة: حراج يخدم صفحة الإعلان المحذوف من الذاكرة المؤقتة لكنه يستبعده من البحث، لذا البحث الحي هو المرجع لا الصفحة.
   - Property Finder: صفحات الأحياء بفلتر fu=1 أعطت سنوياً فقط، وفلتر الفترة (filter[price_type]=m) لا ينعكس على الرابط. المطلوب فتح /en/search?c=2&l=8238&rp=m&fu=1 في المتصفح الحقيقي والتقاط JSON، أو تغيير الفلتر من الواجهة. معرّف حي العليا في PF هو 8238.
   - بيوت: إعادة فتح الـ81 عبر WebFetch لالتقاط ما تحول إلى "لم يعد متاحاً".
   - تمرير عينة عشوائية من 20 إعلاناً للشريك للتحقق المستقل وتسجيل رده في .bridge/transcript.md.

## 4. الطرق التقنية المثبتة (كلها اشتغلت في 2026-09-09 و2026-09-10 بسياسة Full)
- المتصفح عبر بروكسي الجلسة: Playwright مع Chromium من /opt/pw-browsers/chromium ولا يعمل إلا بالأعلام: --disable-features=PostQuantumKyber,UseMLKEM,EncryptedClientHello --disable-quic --ssl-version-max=tls1.2 مع proxy:{server:process.env.HTTPS_PROXY}. بدونها ERR_CONNECTION_RESET.
- بيوت: تحدي أمان يعطي 503 لـcurl وللمتصفح، لكن WebFetch يفتح الصفحة ويعيد الحقول بما فيها بانر "This property is no longer available". صفحات البحث الشهرية: /en/monthly-rental/apartments/riyadh/north-riyadh/<slug>/ والأسماء: al-olaya, al-sulimaniyah, al-wurud, al-muruj, king-fahd, al-mohammadiyah, al-mathar-al-shamali, al-nakhil, al-taawun, al-masif، والوزارات تحت central-riyadh/al-wizarat. الرحمانية لا نتائج.
- حراج: صفحة الإعلان SSR فيها الحقول بصيغة مسطحة (title, bodyTEXT, postDate, updateDate, geoNeighborhood, thumbURL) ويستخرجها haraj_parse.py وhparse2.py. البحث يُقرأ من DOM بالمتصفح (pw_haraj_search.js) لأن GraphQL لا يستجيب لاستعلام مباشر. الصور: https://img4cdn.haraj.com.sa/userfiles30/<تاريخ النشر>/<thumbURL> للصيغة -GO__ فقط، والصيغة القديمة (UUID) محذوفة.
- عقار: صفحات الأحياء SSR بحمولة RSC فيها الكائنات كاملة (السعر، content، lat/lng، mainImage، rent_period). فلاتر تعمل: beds=eq,1 وfurnished=eq,1. فلتر rent_period لا يعمل، فالتحديد الشهري يتم من نص الإعلان (aqar_scan.py). الصور: https://images.aqar.fm/webp/300x0/props/<mainImage>.
- Property Finder: __NEXT_DATA__ يحوي searchResult.listings مع price.period وlisted_date والهاتف. pf_scan.py.
- Airbnb: فتح صفحة البحث بالمتصفح مع check_in/check_out لشهر كامل وcurrency=SAR ثم التقاط استجابة StaysSearch؛ air_parse.py يقرأ demandStayListing (id بترميز base64) والسعر الشهري بعد الخصم والإحداثيات والصورة. الصور: نفس الرابط مع ?im_w=320.
- مبيت: API مباشر بـcurl: app.mabet.com.sa/api/v2/units?city=1&check_in&check_out&page (37 صفحة) ثم /api/v2/units/<id> للتفاصيل والإحداثيات، و/api/v2.1/units/<id>/availability?from&to لتسعير 30 ليلة (full_payment شامل الرسوم).
- الدمج والصور والبناء: merge.py ثم images.py (Pillow، تصغير 320 بكسل، data URI) ثم build_html.py ينتج radar.html (نحو 6.2 ميغابايت، الحد 16).

## 5. ملفات هذا المجلد
scripts/ فيه كل السكربتات أعلاه مع old.json (قائمة الـ47 الأصلية) وremoved.json (أسباب الحذف). بيانات الإعلانات والصور ليست هنا عمداً لأن المستودع عام؛ هي داخل الملف المنشور نفسه.
