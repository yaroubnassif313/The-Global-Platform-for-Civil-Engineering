# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import hashlib
import os

DB_NAME = "Engineering_Library.db"

# --- 1. الإعدادات الهندسية والهوية البصرية الشاملة للمنصة ---
st.set_page_config(
    page_title="المنصة الكبرى | كلية الهندسة المدنية", 
    layout="centered", 
    initial_sidebar_state="expanded" # يظهر مفتوحاً في البداية ويمكن للطالب إغلاقه وفتحه بالسهم العلوي متى شاء
)

# تنسيق المظهر الاحترافي والتكيف التلقائي (Responsive UI) لجميع الأجهزة
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 4.5em;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        transition: 0.3s;
        margin-bottom: 8px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        background-color: #E94560;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الاتصال الموحد وقوانين الأمان المشتركة ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 3. تهيئة وإدارة متغيرات الجلسة الثابتة للمنصة ---
keys = ['step', 'user_data', 'is_admin_login', 'admin_auth', 'page', 'otp_code', 'signup_data']
for key in keys:
    if key not in st.session_state:
        if key == 'step':
            st.session_state[key] = 'welcome'
        elif key in ['is_admin_login', 'admin_auth', 'page', 'otp_code', 'signup_data']:
            st.session_state[key] = False
        else:
            st.session_state[key] = None

# --- 4. دالات التوب بار والبوتوم بار الثابتة والمشتركة عبر المنصة ---
def draw_global_header():
    """رسم التوب بار المتناظر مع الشعارات الرسمية المتكيفة مع الهاتف والكمبيوتر"""
    col_right, col_center, col_left = st.columns(3)
    
    with col_right:
        if os.path.exists("latakia_logo.jpg"):
            st.image("latakia_logo.jpg", use_container_width=True)
        else:
            st.markdown("<p style='text-align: right; font-size: 40px; margin:0;'>🏛️</p>", unsafe_allow_html=True)
        
    with col_center:
        st.markdown("""
            <div style='text-align: center; line-height: 1.3;'>
                <h6 style='margin: 0; color: #666; font-size: 12px;'>وزارة التعليم العالي</h6>
                <h5 style='margin: 3px 0; font-weight: bold; color: #333;'>جامعة اللاذقية</h5>
                <h3 style='margin: 0; color: #1F4068; font-weight: bold; font-size: 18px;'>كلية الهندسة المدنية</h3>
            </div>
            """, unsafe_allow_html=True)
        
    with col_left:
        if os.path.exists("civil_logo.jpg"):
            st.image("civil_logo.jpg", use_container_width=True)
        else:
            st.markdown("<p style='text-align: left; font-size: 40px; margin:0;'>🏗️</p>", unsafe_allow_html=True)
        
    st.divider()

def draw_global_footer():
    """البوتوم بار الثابت لتوثيق حقوقك كمصمم للمنصة الكبرى عبر جميع الصفحات"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #888; font-size: 14px; font-weight: bold;'>
            صمم بواسطة زميلكم المهندس يعرب ناصيف © 2026
        </div>
        """, unsafe_allow_html=True)

# --- 5. استدعاء الملفات الفرعية الموازية بنظام الحماية السحابية ---
try: import sidebar
except ImportError: sidebar = None

try: import auth
except ImportError: auth = None

try: import admin_panel
except ImportError: admin_panel = None

try: import student_dashboard
except ImportError: student_dashboard = None

# --- 6. تشغيل السايد بار الموازي (يعمل بثبات ويمرر الدالة دون شروط صارمة) ---
if sidebar:
    sidebar.show_sidebar(get_db)
else:
    st.sidebar.info("⚙️ نظام السايد بار قيد الرفع والتحديث السحابي...")

# --- 7. المحرك والموجه الرئيسي لإدارة تنقل واجهات الطلاب والمسؤول ---
if st.session_state.is_admin_login:
    if admin_panel:
        admin_panel.show_admin_panel(get_db, draw_global_header, draw_global_footer)
    else:
        draw_global_header()
        st.warning("⚙️ لوحة تحكم المسؤول قيد الرفع الموازي حالياً...")
        if st.button("رجوع للموقع"):
            st.session_state.is_admin_login = False
            st.rerun()
        draw_global_footer()
else:
    # تدفق واجهات الطلاب بناءً على المراحل المتتالية الثابتة
    if st.session_state.step == 'welcome':
        if auth:
            auth.show_welcome_page(draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #1F4068;'>مرحباً بك في منصة كلية الهندسة المدنية الكبرى</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #666;'>المكتبة الرقمية والمنصة الأكاديمية الشاملة لطلاب جامعة اللاذقية</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("تسجيل الدخول إلى المنصة 🔑", type="primary", use_container_width=True):
                st.session_state.step = 'login'
                st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'login':
        if auth:
            auth.show_login_page(get_db, hash_password, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🔑 واجهة تسجيل الدخول قيد الرفع والتحديث...")
            if st.button("⬅️ عودة للخلف"):
                st.session_state.step = 'welcome'
                st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'signup':
        if auth:
            auth.show_signup_page(get_db, hash_password, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("📝 واجهة التفعيل بالرقم الوطني قيد الرفع...")
            if st.button("⬅️ عودة للخلف"):
                st.session_state.step = 'login'
                st.rerun()
            draw_global_footer()

    elif st.session_state.step == 'verify_otp':
        if auth:
            auth.show_otp_page(get_db, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.subheader("🔢 واجهة تأكيد رمز الأمان قيد الرفع...")
            draw_global_footer()

    elif st.session_state.step == 'dashboard':
        if student_dashboard:
            student_dashboard.show_dashboard(get_db, draw_global_header, draw_global_footer)
        else:
            draw_global_header()
            st.title("👷‍♂️ لوحة الخدمات الطلابية:")
            st.button("📢 الأخبار العامة للكلية")
            st.button("📌 الأخبار الخاصة بكل سنة")
            st.button("📚 المحاضرات الخاصة بكل سنة")
            st.button("📄 النوط والدورات الخاصة بكل سنة")
            st.button("🧮 الحاسبات العلمية الهندسية")
            st.button("🤖 قسم المساعدة بالذكاء الصناعي")
            
            st.divider()
            if st.button("🚪 تسجيل الخروج"):
                st.session_state.step = 'welcome'
                st.rerun()
            draw_global_footer()
