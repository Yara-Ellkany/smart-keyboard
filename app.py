# -*- coding: utf-8 -*-
"""
اللوحة الذكية للأطفال - Smart Keyboard for Kids
=================================================
تطبيق تعليمي بسيط بيعلم الأطفال إزاي "التصحيح الإملائي الذكي" بيشتغل،
عن طريق فكرة اسمها "المسافة التحريرية" (Edit Distance).

الفكرة ببساطة:
    - عندنا "قاموس" فيه كلمات صح (عربي + إنجليزي).
    - لما الطفل يكتب كلمة مش موجودة في القاموس، البرنامج بيدور على
      أقرب كلمة صح ليها عن طريق حساب عدد "الخطوات" اللي محتاجينها
      عشان نحول الكلمة الغلط للكلمة الصح (حذف حرف / إضافة حرف / تبديل حرف).
    - كل ده متكتوب من الصفر تحت عشان الطفل (أو المعلم) يقدر يفهم
      إزاي الخوارزمية شغالة، مش بس يستخدمها كصندوق أسود.

طريقة التشغيل:
    1) pip install -r requirements.txt
    2) streamlit run smart_keyboard.py
"""

import os
import string
import streamlit as st

# =============================================================
# 1) إعداد الصفحة والتنسيق العام (CSS بسيط لجعل الواجهة مبهجة للأطفال)
# =============================================================
st.set_page_config(
    page_title="اللوحة الذكية للأطفال",
    page_icon="⌨️",
    layout="centered",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 19px;
    }
    .stButton>button {
        border-radius: 14px;
        font-weight: bold;
        padding: 0.4rem 1rem;
    }
    .word-ok {
        background-color: #d4f7dc;
        color: #1a7a34;
        padding: 4px 10px;
        border-radius: 10px;
        margin: 3px;
        display: inline-block;
        font-weight: bold;
    }
    .word-bad {
        background-color: #fbdada;
        color: #b3261e;
        padding: 4px 10px;
        border-radius: 10px;
        margin: 3px;
        display: inline-block;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⌨️ اللوحة الذكية للأطفال")
st.caption("اكتب جملتك، وهنساعدك تصحّح الكلمات الغلط بالعربي والإنجليزي مع بعض! 🌟")


# =============================================================
# 2) قاموس الكلمات (Dictionary) - عربي وإنجليزي
#    ممكن تضيف كلمات جديدة من الشريط الجانبي وهتتحفظ في ملف نصي.
# =============================================================
DEFAULT_ARABIC_WORDS = [
    "اسم", "بيت", "مدرسة", "كتاب", "قلم", "ولد", "بنت", "أم", "أب", "أخ",
    "أخت", "جد", "جدة", "معلم", "معلمة", "صديق", "صديقة", "شمس", "قمر",
    "نجمة", "سماء", "بحر", "نهر", "جبل", "شجرة", "وردة", "حديقة", "حيوان",
    "قطة", "كلب", "أسد", "فيل", "أرنب", "عصفور", "سمكة", "فراشة", "لون",
    "أحمر", "أزرق", "أخضر", "أصفر", "أبيض", "أسود", "بنفسجي", "برتقالي",
    "رقم", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة",
    "ثمانية", "تسعة", "عشرة", "يوم", "ليل", "صباح", "مساء", "اليوم", "غدا",
    "أمس", "أسبوع", "شهر", "سنة", "فصل", "صيف", "شتاء", "ربيع", "خريف",
    "طعام", "ماء", "خبز", "لبن", "فاكهة", "تفاح", "موز", "برتقال", "عنب",
    "خضار", "لعبة", "كرة", "دراجة", "سيارة", "طائرة", "قطار", "سفينة",
    "مدينة", "قرية", "شارع", "باب", "نافذة", "طاولة", "كرسي", "سرير",
    "غرفة", "مطبخ", "حمام", "ملعب", "فرح", "حب", "سعادة", "حزن", "غضب",
    "خوف", "جميل", "كبير", "صغير", "طويل", "قصير", "سريع", "بطيء", "قوي",
    "ضعيف", "ذكي", "لطيف", "جيد", "سيء", "جديد", "قديم", "نظيف", "وسخ",
    "مفتوح", "مغلق", "يأكل", "يشرب", "يلعب", "يقرأ", "يكتب", "ينام",
    "يذهب", "يأتي", "يجري", "يمشي", "يطير", "يسبح", "يغني", "يرسم",
    "يضحك", "يبكي", "السلام", "عليكم", "شكرا", "آسف", "نعم", "لا", "هذا",
    "هذه", "أنا", "أنت", "هو", "هي", "نحن", "هم", "في", "من", "إلى",
    "على", "مع", "عند",
]

DEFAULT_ENGLISH_WORDS = [
    "the", "and", "is", "a", "to", "in", "of", "it", "you", "that", "he",
    "was", "for", "on", "are", "as", "with", "his", "they", "at", "be",
    "this", "have", "from", "or", "one", "had", "by", "word", "but",
    "not", "what", "all", "were", "we", "when", "your", "can", "said",
    "there", "use", "an", "each", "which", "she", "do", "how", "their",
    "if", "will", "up", "other", "about", "out", "many", "then", "them",
    "these", "so", "some", "her", "would", "make", "like", "him", "into",
    "time", "has", "look", "two", "more", "write", "go", "see", "number",
    "no", "way", "could", "people", "my", "than", "first", "water",
    "been", "call", "who", "its", "now", "find", "long", "down", "day",
    "did", "get", "come", "made", "may", "part", "cat", "dog", "sun",
    "moon", "star", "sky", "sea", "tree", "flower", "animal", "school",
    "book", "pencil", "friend", "family", "mother", "father", "brother",
    "sister", "happy", "sad", "big", "small", "red", "blue", "green",
    "yellow", "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "apple", "banana", "orange", "grape", "milk",
    "bread", "house", "car", "train", "plane", "boat", "city", "village",
    "street", "door", "window", "table", "chair", "bed", "room",
    "kitchen", "garden", "play", "read", "write", "sleep", "run", "walk",
    "fly", "swim", "sing", "draw", "laugh", "cry", "hello", "thank",
    "sorry", "yes", "no", "please",
]

CUSTOM_AR_FILE = "custom_words_ar.txt"
CUSTOM_EN_FILE = "custom_words_en.txt"


def load_custom_words(filepath):
    """يقرأ الكلمات الإضافية اللي المستخدم ضافها قبل كده من ملف نصي."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []


def save_custom_word(filepath, word):
    """يضيف كلمة جديدة للملف النصي عشان تفضل محفوظة بين مرات التشغيل."""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(word.strip() + "\n")


# تحميل القواميس مرة واحدة في بداية الجلسة
if "ar_words" not in st.session_state:
    st.session_state.ar_words = list(
        dict.fromkeys(DEFAULT_ARABIC_WORDS + load_custom_words(CUSTOM_AR_FILE))
    )
if "en_words" not in st.session_state:
    st.session_state.en_words = list(
        dict.fromkeys(DEFAULT_ENGLISH_WORDS + load_custom_words(CUSTOM_EN_FILE))
    )


# =============================================================
# 3) أدوات مساعدة: تطبيع الكلمات (تجاهل التشكيل) وفصل علامات الترقيم
# =============================================================
ARABIC_DIACRITICS = "\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670"
PUNCT_CHARS = string.punctuation + "،؛؟"


def is_arabic_word(word):
    """بيحدد لو الكلمة عربي عن طريق شوفان أي حرف عربي جواها."""
    return any("\u0600" <= ch <= "\u06ff" for ch in word)


def normalize_word(word):
    """
    بيوحّد شكل الكلمة عشان المقارنة تبقى عادلة:
    - يشيل التشكيل من العربي (الفتحة، الضمة، الكسرة...)
    - يوحّد أشكال الألف والياء المختلفة
    - يحول الإنجليزي لحروف صغيرة (lower case)
    """
    w = word
    for d in ARABIC_DIACRITICS:
        w = w.replace(d, "")
    w = w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    w = w.replace("ى", "ي")
    return w.lower()


def split_punctuation(token):
    """بيفصل علامات الترقيم من أول وآخر الكلمة عشان نصحح 'جوهر' الكلمة بس."""
    leading, trailing = "", ""
    core = token
    while core and core[0] in PUNCT_CHARS:
        leading += core[0]
        core = core[1:]
    while core and core[-1] in PUNCT_CHARS:
        trailing = core[-1] + trailing
        core = core[:-1]
    return leading, core, trailing


# =============================================================
# 4) قلب الموضوع: خوارزمية "المسافة التحريرية" (Edit Distance)
#    مكتوبة من الصفر عشان الطفل/المعلم يقدر يشوف إزاي بتفكر خطوة خطوة.
# =============================================================
def edit_distance(word_a, word_b):
    """
    بتحسب أقل عدد "خطوات" (حذف حرف / إضافة حرف / تبديل حرف) عشان
    نحوّل word_a لـ word_b. كل ما الرقم أصغر، كل ما الكلمتين أقرب لبعض.
    """
    n, m = len(word_a), len(word_b)
    # جدول ديناميكي: dp[i][j] = المسافة بين أول i حرف من word_a وأول j حرف من word_b
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i  # تحويل كلمة طولها i لكلمة فاضية = حذف كل الحروف
    for j in range(m + 1):
        dp[0][j] = j  # تحويل كلمة فاضية لكلمة طولها j = إضافة كل الحروف

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if word_a[i - 1] == word_b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # حذف حرف
                dp[i][j - 1] + 1,       # إضافة حرف
                dp[i - 1][j - 1] + cost,  # تبديل حرف (أو نفس الحرف لو cost=0)
            )
    return dp[n][m]


def get_suggestions(word, dictionary, max_distance=2, top_n=3):
    """بيرجع أقرب top_n كلمات صح من القاموس لكلمة معينة."""
    norm_word = normalize_word(word)
    scored = []
    for dict_word in dictionary:
        dist = edit_distance(norm_word, normalize_word(dict_word))
        if dist <= max_distance:
            scored.append((dict_word, dist))
    scored.sort(key=lambda pair: pair[1])
    return [w for w, _ in scored[:top_n]]


def is_correct(word):
    """بيتحقق هل الكلمة موجودة في القاموس المناسب (عربي أو إنجليزي)."""
    if is_arabic_word(word):
        dictionary = st.session_state.ar_words
    else:
        dictionary = st.session_state.en_words
    norm_word = normalize_word(word)
    return any(normalize_word(w) == norm_word for w in dictionary)


def suggestions_for(word):
    dictionary = st.session_state.ar_words if is_arabic_word(word) else st.session_state.en_words
    return get_suggestions(word, dictionary)


# =============================================================
# 5) الشريط الجانبي: شرح مبسط للخوارزمية + إضافة كلمات جديدة للقاموس
# =============================================================
with st.sidebar:
    st.header("🤔 إزاي اللوحة الذكية بتفكر؟")
    st.write(
        "لما تكتب كلمة، اللوحة بتقارنها بكل الكلمات الصح المحفوظة عندها.\n\n"
        "لو الكلمة مش موجودة، بتحسب 'عدد الخطوات' اللي محتاجينها عشان "
        "نحوّل كلمتك لأقرب كلمة صح (زي: تغيير حرف واحد بس).\n\n"
        "مثال: كلمة **'مدرسه'** قريبة من **'مدرسة'** بخطوة واحدة بس، "
        "فهتظهرلك كاقتراح!"
    )

    st.divider()
    st.header("➕ ضيف كلمة جديدة للقاموس")
    new_word = st.text_input("اكتب الكلمة (عربي أو إنجليزي)")
    if st.button("إضافة الكلمة"):
        if new_word.strip():
            if is_arabic_word(new_word):
                st.session_state.ar_words.append(new_word.strip())
                save_custom_word(CUSTOM_AR_FILE, new_word.strip())
            else:
                st.session_state.en_words.append(new_word.strip())
                save_custom_word(CUSTOM_EN_FILE, new_word.strip())
            st.success(f"تمام! ضفنا كلمة '{new_word.strip()}' 🎉")
        else:
            st.warning("لازم تكتب كلمة الأول!")


# =============================================================
# 6) الجملة الحالية + أمثلة سريعة للتجربة
# =============================================================
if "sentence" not in st.session_state:
    st.session_state.sentence = "انا بحب العب في الحديقه with my friend"

st.write("جرّب مثال سريع:")
example_cols = st.columns(3)
examples = [
    "هاذا بيتي وهاذي مدرستي",
    "my dog can rn and jmp",
    "الشمس جميله والسماء زرقاء",
]
for col, example in zip(example_cols, examples):
    if col.button(example, use_container_width=True):
        st.session_state.sentence = example

st.text_area("اكتب جملتك هنا ✍️ (عربي وإنجليزي مع بعض مسموح!)", key="sentence", height=100)


# =============================================================
# 7) تحليل الجملة وعرض النتيجة + اقتراحات قابلة للنقر
# =============================================================
tokens = st.session_state.sentence.split()

if tokens:
    st.subheader("النتيجة:")

    correct_count = 0
    checked_count = 0

    for i, token in enumerate(tokens):
        leading, core, trailing = split_punctuation(token)

        if not core:
            continue

        checked_count += 1

        if is_correct(core):
            correct_count += 1
            st.markdown(
                f'<span class="word-ok">✅ {leading}{core}{trailing}</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span class="word-bad">❌ {leading}{core}{trailing}</span>',
                unsafe_allow_html=True,
            )
            suggestions = suggestions_for(core)

            if suggestions:
                st.caption("يمكن تقصد:")
                sugg_cols = st.columns(len(suggestions))

                def make_replacer(index, replacement, lead, trail, all_tokens):
                    def _replace():
                        new_tokens = all_tokens.copy()
                        new_tokens[index] = lead + replacement + trail
                        st.session_state.sentence = " ".join(new_tokens)
                    return _replace

                for col, suggestion in zip(sugg_cols, suggestions):
                    col.button(
                        suggestion,
                        key=f"sugg_{i}_{suggestion}",
                        on_click=make_replacer(i, suggestion, leading, trailing, tokens),
                    )
            else:
                st.caption("مفيش اقتراح قريب... جرب كلمة تانية 🤷")

    st.divider()
    if checked_count > 0:
        st.metric("عدد الكلمات الصح ⭐", f"{correct_count} / {checked_count}")
        if correct_count == checked_count:
            st.balloons()
            st.success("رائع! كل الكلمات صح! 🎉")
else:
    st.info("ابدأ اكتب جملة عشان اللوحة الذكية تساعدك! 😊")
