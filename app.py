# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import hashlib
import os

# --- 1. الإعدادات الهندسية الكبرى وحصانة المظهر واللغة ---
st.set_page_config(
    page_title="المنصة الكبرى | Faculty of Civil Engineering",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🛡️ وسم السحر البرمجي المانع لتخريب الترجمة التلقائية + التنسيق البصري الفخم والبطاقات التفاعلية
st.markdown("""
    <html lang="ar" translate="no">
    <head>
        <meta name="google" content="notranslate">
    </head>
    </html>
    <style>
    /* منع الترجمة على كامل عناصر المنصة */
    * {
        translate: no !important;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* تصميم البطاقات التفاعلية الأنيقة باللون الكحلي الملكي للمنصة الكبرى */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 4.5em;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
        transition: all 0.3s ease-in-out;
        margin-bottom: 10px;
        background-color: #1F4068;
        color: white;
        border: none;
    }
    /* تأثير الحركة الناعمة للأعلى عند تمرير الماوس أو اللمس بالأصبع (Hover Effect) */
    .stButton>button:hover {
        transform: translateY(-4px);
        background-color: #E94560;
        color: white;
        box-shadow: 0px 8px 20px rgba(233, 69, 96, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الروابط الخماسية المستقلة للاتصال بقواعد البيانات ---
def get_visitor_db():
    return sqlite3.connect("Azaz_Visitor.db")

def get_civil_files_db():
    return sqlite3.connect("Civil_General_Files.db")

def get_survey_files_db():
    return sqlite3.connect("Survey_Geomatics_Files.db")

def get_auth_db():
    return sqlite3.connect("Core_Auth_Registry.db")

def get_ai_db():
    return sqlite3.connect("AI_Core_Brain.db")

# دالة تشفير كلمات المرور لحماية هويات وحسابات الطلاب والدكاترة
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 3. الحماية الحديدية وتثبيت متغيرات الجلسة (Anti-Refresh System) ---
session_keys = {
    'step': 'welcome',         # المرحلة الحالية للمستخدم
    'lang': 'العربية',          # اللغة الافتراضية للمنصة
    'user_data': None,          # بيانات الطالب بعد تسجيل الدخول
    'is_admin_login': False,    # مؤشر محاولة دخول مشرف
    'admin_auth': False,        # تأكيد نجاح دخول الدكتور
    'selected_dept': None,      # القسم المختار (مدني عام / مساحة)
    'otp_code': None,           # رمز الأمان المؤقت
    'signup_data': None         # بيانات التسجيل المؤقتة للطالب الجديد
}

for key, default_val in session_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_val

# --- 4. الأشرطة العالمية الموحدة (Global Frame) ---
def draw_global_header():
    """رسم التوب بار المتناظر مع الشعارات الرسمية المتكيفة مع الهاتف والكمبيوتر"""
    col_right, col_center, col_left = st.columns(3)
    
    with col_right:
        if os.path.exists("latakia_logo.jpg"):
            st.image("latakia_logo.jpg", use_container_width=True)
        else:
            st.markdown("<p style='text-align: right; font-size: 40px; margin:0;'>🏛️</p>", unsafe_allow_html=True)
        
    with col_center:
        if st.session_state.lang == 'العربية':
            st.markdown("""
                <div style='text-align: center; line-height: 1.3;'>
                    <h6 style='margin: 0; color: #666; font-size: 12px;'>وزارة التعليم العالي</h6>
                    <h5 style='margin: 3px 0; font-weight: bold; color: #333;'>جامعة اللاذقية</h5>
                    <h3 style='margin: 0; color: #1F4068; font-weight: bold; font-size: 18px;'>كلية الهندسة المدنية</h3>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='text-align: center; line-height: 1.3;'>
                    <h6 style='margin: 0; color: #666; font-size: 11px;'>Ministry of Higher Education</h6>
                    <h5 style='margin: 3px 0; font-weight: bold; color: #333;'>University of Latakia</h5>
                    <h3 style='margin: 0; color: #1F4068; font-weight: bold; font-size: 16px;'>Faculty of Civil Engineering</h3>
                </div>
                """, unsafe_allow_html=True)
        
    with col_left:
        if os.path.exists("civil_logo.jpg"):
            st.image("civil_logo.jpg", use_container_width=True)
        else:
            st.markdown("<p style='text-align: left; font-size: 40px; margin:0;'>🏗️</p>", unsafe_allow_html=True)
        
    st.divider()

def draw_global_footer():
    """البوتوم بار الثابت لتوثيق حقوق التصميم عبر جميع الواجهات بلغة الطالب المختارة"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    if st.session_state.lang == 'العربية':
        st.markdown("""
            <div style='text-align: center; color: #888; font-size: 14px; font-weight: bold;'>
                صمم بواسطة زميلكم المهندس يعرب ناصيف © 2026
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align: center; color: #888; font-size: 14px; font-weight: bold;'>
                Designed by your colleague, Eng. Yaroub Nassif © 2026
            </div>
            """, unsafe_allow_html=True)

# --- 5. استدعاء واستيراد الملفات الفرعية بنظام التوازي الذكي ---
try: import sidebar
except ImportError: sidebar = None

try: import gateway
except ImportError: gateway = None

try: import auth
except ImportError: auth = None

try: import admin_panel
except ImportError: admin_panel = None

try: import student_dashboard
except ImportError: student_dashboard = None

# --- 6. تشغيل السايد بار الحديدي والدائم في قمة الكود ---
if sidebar:
    sidebar.show_sidebar(get_auth_db)

# --- 7. الموجه والمحرك المركزي الحركي للميدل بار (Middle Bar Router) ---
# الفرز الأول: التحويل التلقائي لبوابة إشراف المنصة إذا ضغط الدكتور على زر الإشراف في السايد بار
if st.session_state.is_admin_login:
    if admin_panel:
        admin_panel.show_admin_panel(get_auth_db, get_visitor_db, get_civil_files_db, get_survey_files_db, get_ai_db, draw_global_header, draw_global_footer)
    else:
        draw_global_header()
        st.warning("⚙️ بوابة إشراف المنصة قيد الرفع الموازي حالياً...")
        if st.button("رجوع للخلف"):
            st.session_state.is_admin_login = False
            st.rerun()
        draw_global_footer()
else:
    # الفرز الثاني: تدفق واجهات الطلاب والزوار بناءً على المراحل المتتالية
    if st.session_state.step == 'welcome':
        if gateway:
            gateway.show_welcome_gateway(get_visitor_db, get_ai_db, draw_global_header, draw_global_footer)
        else:
            # واجهة ترحيبية احتياطية أنيقة تعمل تلقائياً لحين رفع ملف gateway.py الفرعي
            draw_global_header()
            col_lang1, col_lang2 = st.columns([4, 1])
            with col_lang2:
                # مفتاح التبديل الفوري للغات في أعلى يمين الميدل بار
                st.session_state.lang = st.selectbox("🌐", ["العربية", "English"], index=0 if st.session_state.lang == "العربية" else 1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.lang == 'العربية':
                st.markdown("<h2 style='text-align: center; color: #1F4068;'>مرحباً بك في منصة كلية الهندسة المدنية الكبرى</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #666;'>المكتبة الرقمية والمنصة الأكاديمية الشاملة لطلاب جامعة اللاذقية</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("🚀 بوابة الهندسة المدنية الاستكشافية (زائر)", type="primary"):
                        st.session_state.step = 'visitor_portal'
                        st.rerun()
                with col_b2:
                    if st.button("🔑 تسجيل الدخول الآمن للطلاب", type="primary"):
                        st.session_state.step = 'login'
                        st.rerun()
            else:
                st.markdown("<h2 style='text-align: center; color: #1F4068;'>Welcome to the Grand Civil Engineering Platform</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #666;'>The digital library and comprehensive academic gateway for Latakia University students</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("🚀 Civil Engineering Explorer Gateway", type="primary"):
                        st.session_state.step = 'visitor_portal'
                        st.rerun()
                with col_b2:
                    if st.button("🔑 Student Secure Login", type="primary"):
                        st.session_state.step = 'login'
                        st.rerun()
                        
            draw_global_footer()

    elif st.session_state.step == 'visitor_portal':
        if gateway:
            gateway.show_visitor_portal(get_visitor_db, get_ai_db, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🌐 بوابة الهندسة المدنية الاستكشافية قيد التجميع الموازي...")
            if st.button("⬅️ العودة للرئيسية"):
                st.session_state.step = 'welcome'
                st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'login':
        if auth:
            auth.show_login_page(get_auth_db, hash_password, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🔑 واجهة تسجيل دخول الطلاب قيد التجهيز...")
            if st.button("⬅️ العودة للرئيسية"):
                st.session_state.step = 'welcome'
                st.rerun()
