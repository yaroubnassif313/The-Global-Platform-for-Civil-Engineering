# -*- coding: utf-8 -*-
import streamlit as st
import random

# 🌟 1. الواجهة الترحيبية الأولى للمنصة (Welcome Page)
def show_welcome_page(draw_header, draw_footer):
    draw_header() # استدعاء التوب بار الموحد بالصور في البداية
    
    # الـ Middle Bar الترحيبي
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1F4068;'>مرحباً بك في منصة كلية الهندسة المدنية الكبرى</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>المكتبة الرقمية والمنصة الأكاديمية الشاملة لطلاب جامعة اللاذقية</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("تسجيل الدخول إلى المنصة 🔑", type="primary", use_container_width=True):
        st.session_state.step = 'login'
        st.rerun()
        
    draw_footer() # استدعاء البوتوم بار المشترك في النهاية


# 🌟 2. واجهة تسجيل الدخول للطلاب (Login Page)
def show_login_page(get_db_func, hash_func, draw_header, draw_footer):
    draw_header()
    
    st.subheader("🔑 تسجيل الدخول للمنصة")
    u_email = st.text_input("البريد الإلكتروني المعتمد (Gmail):")
    u_password = st.text_input("كلمة المرور:", type="password")
    
    if st.button("دخول آمن", type="primary"):
        if u_email and u_password:
            db = get_db_func()
            # فحص ومطابقة بيانات الطالب المشفرة بـ SHA-256 لحماية الخصوصية
            user = db.execute("SELECT * FROM access_gate WHERE email=? AND password=?", (u_email, hash_func(u_password))).fetchone()
            db.close()
            if user:
                if user['is_verified'] == 1:
                    st.session_state.user_data = user
                    st.session_state.step = 'dashboard'
                    st.rerun()
                else:
                    st.warning("⚠️ هذا الحساب معلق، يرجى إعادة تفعيله عبر خيار تسجيل طالب جديد بالأسفل.")
            else:
                st.error("❌ عذراً، البريد الإلكتروني أو كلمة المرور غير صحيحة.")
        else:
            st.warning("⚠️ يرجى إدخال البريد الإلكتروني وكلمة المرور.")
                
    st.divider()
    if st.button("طالب جديد؟ تفعيل وتوثيق الحساب بالرقم الوطني 📝", use_container_width=True):
        st.session_state.step = 'signup'
        st.rerun()
    if st.button("رجوع للخلف", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()
        
    draw_footer()


# 🌟 3. واجهة التسجيل المتقدم بالتحقق الثلاثي الصارم مع رسالة الـ OTP المحدثة (Sign Up Page)
def show_signup_page(get_db_func, hash_func, draw_header, draw_footer):
    import smtplib
    from email.mime.text import MIMEText
    
    draw_header()
    st.subheader("📝 تفعيل حساب طالب جديد")
    st.caption("أمن المنصة: يتم تدقيق هويتك الثلاثية الحالية فوراً مع سجلات الكلية الرسمية.")
    
    s_name = st.text_input("الاسم الكامل (كما هو مسجل بالكلية):")
    s_serial = st.text_input("الرقم الجامعي (Serial Number):")
    s_national = st.text_input("الرقم الوطني المكون من 11 رقماً:")
    s_email = st.text_input("بريدك الإلكتروني الشخصي الحقيقي (Gmail):")
    s_pass = st.text_input("اختر كلمة مرور جديدة للمنصة:", type="password")
    s_confirm = st.text_input("تأكيد كلمة المرور الجديدة:", type="password")
    
    if st.button("التحقق والمصادقة الأمنية 🚀", type="primary", use_container_width=True):
        if not (s_name and s_serial and s_national and s_email and s_pass and s_confirm):
            st.error("⚠️ يرجى ملء كافة الحقول والخانات المطلوبة أعلاه.")
        elif s_pass != s_confirm:
            st.error("❌ عذراً، كلمات المرور المكتوبة غير متطابقة!")
        elif not s_email.endswith("@gmail.com"):
            st.error("❌ يرجى استخدام بريد إلكتروني حقيقي ونشط ينتهي بامتداد @gmail.com.")
        else:
            db = get_db_func()
            # الفحص الثلاثي الحقيقي الحاسم مباشرة من جدولك المعتمد access_gate
            record = db.execute("SELECT * FROM access_gate WHERE serial_number=? AND full_name=? AND national_id=?", (s_serial, s_name, s_national)).fetchone()
            db.close()
            
            if record:
                otp = str(random.randint(100000, 999999))
                st.session_state.otp_code = otp
                st.session_state.signup_data = {
                    'serial': s_serial, 'email': s_email, 'password': hash_func(s_pass)
                }
                
                st.success("✅ تم التحقق من هويتك بنجاح في سجلات الكلية الكبرى!")
                
                # 📨 صياغة رسالة الإيميل الرسمية والمعدلة بناءً على رغبتك هندسة
                email_body = f"مرحباً بك يا مهندس {s_name}\n\nكود تفعيل منصة كلية الهندسة المدنية هو: {otp}"
                
                msg = MIMEText(email_body, 'plain', 'utf-8')
                msg['Subject'] = "كود تفعيل حساب المنصة الكبرى"
                msg['From'] = "facultyofcivilengineering1@gmail.com"  # الإيميل الرسمي الجديد للكلية
                msg['To'] = s_email
                
                with st.spinner("جاري إرسال رمز الأمان إلى بريدك الحقيقي..."):
                    try:
                        # الاتصال بسيرفر جوجل باستخدام بيانات الاعتماد الجديدة الخاصة بك
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                            server.login("facultyofcivilengineering1@gmail.com", "ilbm mour ukcv lshr")
                            server.sendmail("facultyofcivilengineering1@gmail.com", s_email, msg.as_string())
                        st.info(f"📨 تم إرسال الرمز بنجاح من حساب الكلية الرسمي إلى: {s_email}")
                    except Exception:
                        st.warning("⚠️ تعذر الإرسال الآلي سحابياً حالياً بسبب قيود جوجل السحابية لحماية الحساب الجديد.")
                        st.info(f"⚙️ وضع المطور السحابي الاحتياطي: رمز التفعيل المولد هو: {otp}")
                    
                st.session_state.step = 'verify_otp'
                st.rerun()
            else:
                st.error("❌ عذراً، البيانات الثلاثية المدخلة غير مطابقة لسجلات الكلية الرسمية. راجع المسؤول لإضافتك.")
                    
    if st.button("رجوع لصفحة الدخول", use_container_width=True):
        st.session_state.step = 'login'
        st.rerun()
        
    draw_footer()


# 🌟 4. واجهة تأكيد وإدخال رمز الأمان (OTP Page)
def show_otp_page(get_db_func, draw_header, draw_footer):
    draw_header()
    st.header("🔢 نافذة تفعيل رمز الأمان")
    st.write(f"الرجاء إدخال الرمز المخصص لتفعيل الحساب: **{st.session_state.signup_data['email']}**")
    
    if 'otp_code' in st.session_state and st.session_state.otp_code:
        st.caption(f"(تنبيه وضع المطور السحابي: الرمز النشط حالياً هو {st.session_state.otp_code})")
        
    input_otp = st.text_input("أدخل رمز التفعيل المكون من 6 أرقام:", max_chars=6)
    
    if st.button("تأكيد التفعيل وفتح الحساب رسميًا ✅", type="primary", use_container_width=True):
        if input_otp == st.session_state.otp_code:
            db = get_db_func()
            # حفظ الحساب وتفعيله ليصبح معتمداً في قاعدة البيانات
            db.execute('''
                UPDATE access_gate 
                SET email=?, password=?, is_verified=1 
                WHERE serial_number=?
            ''', (st.session_state.signup_data['email'], st.session_state.signup_data['password'], st.session_state.signup_data['serial']))
            db.commit()
            db.close()
            
            st.success("🎉 تم تفعيل وتوثيق حسابك بنجاح في المنصة الكبرى!")
            st.session_state.step = 'login'
            st.rerun()
        else:
            st.error("❌ الرمز المدخل غير صحيح، يرجى المحاولة مرة أخرى.")
            
    if st.button("إلغاء والعودة للبداية", use_container_width=True):
        st.session_state.step = 'welcome'
        st.rerun()
        
    draw_footer()
