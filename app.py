# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import hashlib
import os

# --- 1. الإعدادات الهندسية الكبرى والتحصين البصري المانع للترجمة قسراً ---
st.set_page_config(
    page_title="المنصة الكبرى | Faculty of Civil Engineering",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <html lang="ar" translate="no">
    <head><meta name="google" content="notranslate"></head>
    </html>
    <style>
    * { translate: no !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
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
    .stButton>button:hover {
        transform: translateY(-4px);
        background-color: #E94560;
        color: white;
        box-shadow: 0px 8px 20px rgba(233, 69, 96, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. روابط الاتصال بقواعد البيانات الخمس المستقلة ---
def get_visitor_db(): return sqlite3.connect("Azaz_Visitor.db")
def get_civil_files_db(): return sqlite3.connect("Civil_General_Files.db")
def get_survey_files_db(): return sqlite3.connect("Survey_Geomatics_Files.db")
def get_auth_db(): return sqlite3.connect("Core_Auth_Registry.db")
def get_ai_db(): return sqlite3.connect("AI_Core_Brain.db")

# --- 3. إدارة وحفظ متغيرات الجلسة الثابتة عند التحديث ---
session_keys = {
    'step': 'welcome', 'lang': 'العربية', 'user_data': None,
    'admin_auth': False, 'selected_dept': None, 'otp_code': None, 'signup_data': None
}
for key, default_val in session_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_val

# --- 4. الأشرطة العالمية الموحدة (التوب بار والبوتوم بار الثابت) ---
def draw_global_header():
    col_right, col_center, col_left = st.columns(3)
    with col_right:
        if os.path.exists("latakia_logo.jpg"): st.image("latakia_logo.jpg", use_container_width=True)
        else: st.markdown("<p style='text-align: right; font-size: 40px; margin:0;'>🏛️</p>", unsafe_allow_html=True)
    with col_center:
        if st.session_state.lang == 'العربية':
            st.markdown("<div style='text-align: center; line-height: 1.3;'><h6 style='margin: 0; color: #666; font-size: 12px;'>وزارة التعليم العالي</h6><h5 style='margin: 3px 0; font-weight: bold; color: #333;'>جامعة اللاذقية</h5><h3 style='margin: 0; color: #1F4068; font-weight: bold; font-size: 18px;'>كلية الهندسة المدنية</h3></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; line-height: 1.3;'><h6 style='margin: 0; color: #666; font-size: 11px;'>Ministry of Higher Education</h6><h5 style='margin: 3px 0; font-weight: bold; color: #333;'>University of Latakia</h5><h3 style='margin: 0; color: #1F4068; font-weight: bold; font-size: 16px;'>Faculty of Civil Engineering</h3></div>", unsafe_allow_html=True)
    with col_left:
        if os.path.exists("civil_logo.jpg"): st.image("civil_logo.jpg", use_container_width=True)
        else: st.markdown("<p style='text-align: left; font-size: 40px; margin:0;'>🏗️</p>", unsafe_allow_html=True)
    st.divider()

def draw_global_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    if st.session_state.lang == 'العربية':
        st.markdown("<div style='text-align: center; color: #888; font-size: 14px; font-weight: bold;'>صمم بواسطة زميلكم المهندس يعرب ناصيف © 2026</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; color: #888; font-size: 14px; font-weight: bold;'>Designed by your colleague, Eng. Yaroub Nassif © 2026</div>", unsafe_allow_html=True)

# --- 5. استدعاء واستيراد الملفات الفرعية بنظام التوازي ---
try: import gateway
except ImportError: gateway = None
try: import auth
except ImportError: auth = None
try: import admin_panel
except ImportError: admin_panel = None
try: import student_dashboard
except ImportError: student_dashboard = None

# --- 6. المحرك والموجه المركزي الحركي للميدل بار (Middle Bar Router) ---
if st.session_state.admin_auth:
    if admin_panel:
        admin_panel.show_admin_panel(get_auth_db, get_visitor_db, get_civil_files_db, get_survey_files_db, get_ai_db, draw_global_header, draw_global_footer)
    else:
        draw_global_header()
        st.warning("⚙️ نظام الإشراف قيد التحميل الموازي...")
        draw_global_footer()
else:
    if st.session_state.step == 'welcome':
        draw_global_header()
        
        # 📞 وضع حقل زر الدعم الفني في زاوية الميدل بار اليمينية العلوية تحت التوب بار مباشرة
        col_sup1, col_sup2 = st.columns([3, 1])
        with col_sup2:
            if st.button("📞 الدعم التقني", key="corner_support_btn", type="secondary"):
                st.toast("💬 واتساب: 0992325041 | ✈️ تليجرام: @AMS0012", icon="ℹ️")
                st.info("💡 للتواصل السريع الفوري مع المهندس المطور: [اضغط للواتساب](https://wa.me) أو [اضغط للتليجرام](https://t.me)")
        
        # شريط الطاقم القيادي للكلية المعتمد
        st.markdown("<div style='text-align: center; background-color: rgba(31, 64, 104, 0.03); padding: 10px; border-radius: 10px; font-size: 13px; color: #555;'>🎓 عميد الكلية: د. محسن أحمد | 🏛️ النائب الإداري: د. عصام غزولين | 🔬 النائب العلمي: د. شريف الحايك</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.lang == 'العربية':
            st.markdown("<h2 style='text-align: center; color: #1F4068;'>مرحباً بك في منصة كلية الهندسة المدنية الكبرى</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #666;'>المكتبة الرقمية والمنصة الأكاديمية الشاملة لطلاب جامعة اللاذقية</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🚀 بوابة الهندسة المدنية الاستكشافية (زائر)"):
                    st.session_state.step = 'visitor_portal'
                    st.rerun()
            with col_b2:
                if st.button("🔑 الدخول الآمن الموحد للمنصة"):
                    st.session_state.step = 'login'
                    st.rerun()
        else:
            st.markdown("<h2 style='text-align: center; color: #1F4068;'>Welcome to the Grand Civil Engineering Platform</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #666;'>Digital library and comprehensive academic gateway</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🚀 Civil Engineering Explorer Gateway"):
                    st.session_state.step = 'visitor_portal'
                    st.rerun()
            with col_b2:
                if st.button("🔑 Student Secure Login"):
                    st.session_state.step = 'login'
                    st.rerun()
        draw_global_footer()

    elif st.session_state.step == 'visitor_portal':
        if gateway: gateway.show_visitor_portal(get_visitor_db, get_ai_db, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🌐 البوابة الاستكشافية قيد التحميل الموازي...")
            if st.button("⬅️ العودة للرئيسية"): st.session_state.step = 'welcome'; st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'login':
        if auth: auth.show_login_page(get_auth_db, hash_password, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🔑 واجهة تسجيل الدخول الموحدة قيد التجهيز...")
            if st.button("⬅️ العودة للرئيسية"): st.session_state.step = 'welcome'; st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'signup':
        if auth: auth.show_signup_page(get_auth_db, hash_password, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("📝 واجهة التفعيل بالرقم الوطني قيد البناء...")
            if st.button("⬅️ عودة للخلف"): st.session_state.step = 'login'; st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'verify_otp':
        if auth: auth.show_otp_page(get_auth_db, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🔢 واجهة تأكيد الـ OTP قيد التفعيل...")
            draw_global_footer()

    elif st.session_state.step == 'dashboard':
        if student_dashboard: student_dashboard.show_student_dashboard(get_civil_files_db, get_survey_files_db, get_ai_db, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.title("👷‍♂️ لوحة الخدمات الطلابية الموحدة:")
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.step = 'welcome'; st.session_state.user_data = None; st.rerun()
            draw_global_footer()
