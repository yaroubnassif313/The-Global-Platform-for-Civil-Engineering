# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import hashlib
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =====================================================================
# 1. الإعدادات الهندسية الكبرى والتحصين البصري المانع للترجمة قسراً
# =====================================================================
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
    
    /* تصميم البطاقات التفاعلية ذات الحواف الدائرية الكحلي الملكي للمنصة الكبرى */
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

# =====================================================================
# 2. روابط الاتصال بقواعد البيانات الخمس المستقلة وتشفير الأمان
# =====================================================================
def get_visitor_db(): return sqlite3.connect("Azaz_Visitor.db")
def get_civil_files_db(): return sqlite3.connect("Civil_General_Files.db")
def get_survey_files_db(): return sqlite3.connect("Survey_Geomatics_Files.db")
def get_auth_db(): return sqlite3.connect("Core_Auth_Registry.db")
def get_ai_db(): return sqlite3.connect("AI_Core_Brain.db")

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# =====================================================================
# 3. إدارة وحفظ متغيرات الجلسة الحديدية والمقاومة للتحديث (Refresh)
# =====================================================================
session_keys = {
    'step': 'welcome', 'lang': 'العربية', 'user_data': None,
    'admin_auth': False, 'selected_dept': None, 'otp_code': None, 'signup_data': None
}
for key, default_val in session_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_val

# =====================================================================
# 4. الأشرطة العالمية الموحدة (التوب بار والبوتوم بار الثابت)
# =====================================================================
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

# =====================================================================
# 5. نظام إرسال رسائل الـ OTP الفخمة عبر الجيميل الرسمي للمطور
# =====================================================================
def send_otp_email(student_email, student_name, otp_code):
    sender_email = "yaroubnassif313@gmail.com"
    sender_password = "uhcr jtwb exbc qkwd" 
    
    msg = MIMEMultipart()
    msg['From'] = f"المنصة الكبرى | كلية الهندسة المدنية <{sender_email}>"
    msg['To'] = student_email
    msg['Subject'] = f"🔒 رمز التحقق الرقمي الخاص بك: {otp_code}"
    
    body = f"""
    <html>
    <body style="direction: rtl; text-align: right; font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 6px solid #1F4068;">
            <h2 style="color: #1F4068; text-align: center;">🏛️ جامعة اللاذقية - كلية الهندسة المدنية</h2>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p style="font-size: 16px; color: #333;">مرحباً بالزميل المهندس: <b>{student_name}</b></p>
            <p style="font-size: 15px; color: #555; line-height: 1.6;">لقد قمت بطلب تفعيل حسابك على المنصة الكبرى الأكاديمية. يرجى استخدام رمز الأمان المؤقت التالي لإتمام عملية التحقق الرقمي الحيوية بنجاح:</p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #E94560; background-color: #fff0f2; padding: 10px 30px; border-radius: 10px; border: 2px dashed #E94560; letter-spacing: 5px;">{otp_code}</span>
            </div>
            <p style="font-size: 13px; color: #888;">⚠️ هذا الرمز صالح للاستخدام مرة واحدة فقط، يرجى عدم مشاركته مع أي شخص حفاظاً على سرية بياناتك الأكاديمية.</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin-top: 30px;">
            <p style="text-align: center; font-size: 12px; color: #aaa; font-weight: bold;">تم التطوير بكل فخر وموثوقية © 2026</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    try:
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, student_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False

# =====================================================================
# 6. الموجه والمحرك التفاعلي المركزي للميدل بار (Middle Bar Router)
# =====================================================================

# ⚙️ فرز الأمان السري والكامل: إذا نجح دخول الدكتور كأدمن تفتح له لوحة التحكم الموحدة فوراً
if st.session_state.admin_auth:
    draw_global_header()
    st.markdown("<h2 style='text-align: center; color: #E94560;'>🛠️ بوابة إشراف المنصة الموحدة</h2>", unsafe_allow_html=True)
    st.info("مرحباً بك يا دكتور في لوحة التحكم المطلقة. سيتم تفعيل أزرار التغذية والرفع الموازي لقواعد البيانات الخمسة خطوة بخطوة...")
    
    if st.button("🚪 خروج من بوابة الإشراف", type="primary"):
        st.session_state.admin_auth = False
        st.rerun()
    draw_global_footer()

else:
    # 🏙️ تدفق واجهات الطلاب والزوار العادية بسلاسة تامة
    if st.session_state.step == 'welcome':
        draw_global_header()
        
        # 📞 زر الدعم التقني الأنيق في الزاوية العلوية اليمنى للميدل بار تحت التوب بار مباشرة
        col_sup1, col_sup2 = st.columns(2)
        with col_sup2:
            if st.button("📞 الدعم التقني", key="corner_support_btn", type="secondary"):
                st.toast("💬 واتساب: 0992325041 | ✈️ تليجرام: @AMS0012", icon="ℹ️")
                st.info("💡 للتواصل السريع الفوري مع المهندس المطور: [اضغط للواتساب](https://wa.me) أو [اضغط للتليجرام](https://t.me)")
        
        # شريط الطاقم القيادي الفخم والشفاف للكلية
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
