# -*- coding: utf-8 -*-
import streamlit as st
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- دالة إرسال رمز الأمان OTP عبر الجيميل الرسمي بنظام فخم ---
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

# --- 1. واجهة تسجيل الدخول الموحدة والمخفية بالأسماء المتطابقة ---
def show_login_page(get_auth_db, hash_func, draw_global_header, draw_global_footer):
    draw_global_header()
    st.markdown("<h3 style='text-align: center; color: #1F4068;'>🔑 بوابة الدخول الموحدة والآمنة</h3>", unsafe_allow_html=True)
    st.caption("الرجاء إدخال بياناتك الرسمية للعبور إلى لوحة خدمات الكلية")
    
    in_name = st.text_input("📝 الاسم الثلاثي الكامل:")
    in_pass = st.text_input("🔒 كلمة السر الخاصة بك:", type="password")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        if st.button("تأكيد الدخول الآمن 🛡️", type="primary", use_container_width=True):
            if in_name and in_pass:
                db = get_auth_db()
                admin = db.execute("SELECT * FROM admins_access WHERE full_name_triple=? AND admin_password=?", (in_name, in_pass)).fetchone()
                
                if admin:
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    hashed_p = hash_func(in_pass)
                    student = db.execute("SELECT * FROM students_access WHERE full_name=? AND password=? AND is_verified=1", (in_name, hashed_p)).fetchone()
                    db.close()
                    
                    if student:
                        st.session_state.user_data = dict(student)
                        st.session_state.step = 'dashboard'
                        st.rerun()
                    else:
                        st.error("❌ عذراً، البيانات المكتوبة غير مسجلة، أو أن الحساب لم يتم تفعيله بالرقم الوطني بعد.")
            else:
                st.warning("⚠️ يرجى كتابة الاسم الثلاثي وكلمة المرور أولاً.")
                
    with col_l2:
        if st.button("📝 تسجيل طالب جديد", use_container_width=True):
            st.session_state.step = 'signup'
            st.rerun()
            
    if st.button("⬅️ العودة للصفحة الرئيسية", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()
        
    draw_global_footer()

# --- 2. واجهة التفعيل بالرقم الوطني والتحقق الثلاثي الصارم بالأسماء المتطابقة ---
def show_signup_page(get_auth_db, hash_func, draw_global_header, draw_global_footer):
    draw_global_header()
    st.markdown("<h3 style='text-align: center; color: #1F4068;'>📝 تفعيل حساب طالب جديد</h3>", unsafe_allow_html=True)
    st.caption("نظام المطابقة الثلاثية الصارمة لمنع الحسابات الوهمية وحماية بيانات الطلاب")
    
    s_name = st.text_input("الاسم الثلاثي المعتمد في سجلات الكلية:")
    s_serial = st.text_input("الرقم الجامعي المعتمد (Serial Number):")
    s_national = st.text_input("الرقم الوطني الرسمي (المكون من 11 رقماً):")
    s_email = st.text_input("البريد الإلكتروني (الجيميل الرسمي لتلقي الـ OTP):")
    s_pass = st.text_input("اختر كلمة مرور قوية لحسابك:", type="password")
    
    if st.button("إرسال رمز التفعيل والأمان 🚀", type="primary", use_container_width=True):
        if s_name and s_serial and s_national and s_email and s_pass:
            generated_otp = str(random.randint(100000, 999999))
            st.session_state.otp_code = generated_otp
            
            st.session_state.signup_data = {
                'serial': s_serial, 'name': s_name, 'national': s_national,
                'email': s_email, 'password': hash_func(s_pass)
            }
            
            sent = send_otp_email(s_email, s_name, generated_otp)
            if sent:
                st.success("📩 تم إرسال رمز الأمان OTP بنجاح إلى بريد الجيميل الخاص بك. يرجى مراجعة صندوق الوارد والرسائل.")
            else:
                st.toast(f"🔒 رمز التحقق المؤقت الخاص بك هو: {generated_otp}", icon="ℹ️")
                st.info(f"💡 الرمز الاحتياطي السريع للتفعيل: {generated_otp}")
                
            st.session_state.step = 'verify_otp'
            st.rerun()
        else:
            st.error("❌ يرجى ملء كافة الخانات والبيانات الهندسية المطلوبة للتأكيد.")
            
    if st.button("⬅️ تراجع والعودة للدخول", use_container_width=True):
        st.session_state.step = 'login'
        st.rerun()
    draw_global_footer()

# --- 3. واجهة تأكيد رمز الأمان وإقفال الحساب بالأسماء المتطابقة ---
def show_otp_page(get_auth_db, draw_global_header, draw_global_footer):
    draw_global_header()
    st.markdown("<h3 style='text-align: center; color: #1F4068;'>🔢 تأكيد الرمز الرقمي الآمن</h3>", unsafe_allow_html=True)
    st.caption("أدخل الرمز المكون من 6 أرقام والموجود في رسالة الجيميل")
    
    user_otp = st.text_input("أدخل رمز الـ OTP هنا:", max_chars=6)
    
    if st.button("تأكيد واعتماد الحساب رسمياً 💾", type="primary", use_container_width=True):
        if user_otp and user_otp == st.session_state.otp_code:
            s_data = st.session_state.signup_data
            db = get_auth_db()
            try:
                db.execute('''
                    INSERT INTO students_access (serial_number, full_name, national_id, email, password, is_verified, department)
                    VALUES (?, ?, ?, ?, ?, 1, 'لم يحدد بعد')
                ''', (s_data['serial'], s_data['name'], s_data['national'], s_data['email'], s_data['password']))
                db.commit()
                st.success("🎉 مبارك يا زميل! تم تفعيل هويتك الرقمية بنجاح وجاري نقلك للوحة تسجيل الدخول.")
                st.session_state.step = 'login'
                st.session_state.otp_code = None
                st.session_state.signup_data = None
                st.rerun()
            except sqlite3.IntegrityError:
                st.warning("⚠️ تنبيه أمني: هذا الطالب أو الأرقام الثبوتية مسجلة بالفعل مسبقاً بالنظام!")
            finally:
                db.close()
        else:
            st.error("❌ عذراً، الرمز المدخل غير صحيح. يرجى مطابقة الأرقام الستة بدقة.")
            
    if st.button("⬅️ إعادة المحاولة", use_container_width=True):
        st.session_state.step = 'signup'
        st.rerun()
    draw_global_footer()
