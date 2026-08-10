# -*- coding: utf-8 -*-
import streamlit as st

def show_admin_panel(get_db_func, draw_header, draw_footer):
    """
    لوحة التحكم والقيادة الكبرى المخصصة لرئيس المنصة، الدكاترة، والإداريين.
    يتم استدعاؤها بالتوازي من المحرك الرئيسي لتغذية جداول قاعدة البيانات السبعة.
    """
    # 🔐 1. مرحلة التحقق والمصادقة الرقمية للمشرفين من جدول قاعدة البيانات
    if not st.session_state.admin_auth:
        draw_header()
        st.title("🔐 بوابة التحقق الرقمي للمشرفين")
        st.caption("هذه اللوحة مخصصة لأعضاء الهيئة التدريسية وإدارة المنصة الكبرى")
        
        a_name = st.text_input("الاسم الكامل للمسؤول (كما هو بجدول الإدارة):")
        a_pass = st.text_input("كلمة مرور المشرف الخاصة بك:", type="password")
        
        col_adm_btn1, col_adm_btn2 = st.columns(2)
        with col_adm_btn1:
            if st.button("تأكيد الدخول الآمن 🛡️", type="primary", use_container_width=True):
                if a_name and a_pass:
                    db = get_db_func()
                    # الفحص الذكي: المطابقة الحية مع جدول admins لتأكيد دخول أي دكتور مضاف مستقبلاً
                    admin = db.execute("SELECT * FROM admins WHERE full_name=? AND admin_password=?", (a_name, a_pass)).fetchone()
                    db.close()
                    if admin:
                        st.session_state.admin_auth = True
                        st.rerun()
                    else: 
                        st.error("❌ عذراً، بيانات الإشراف المكتوبة غير مسجلة بنظام الكلية.")
                else:
                    st.warning("⚠️ الرجاء كتابة الاسم وكلمة المرور للمصادقة.")
        with col_adm_btn2:
            if st.button("إلغاء والعودة للموقع الطلاب الخارجي", use_container_width=True): 
                st.session_state.is_admin_login = False
                st.rerun()
        draw_footer()

    # 🏛️ 2. فتح لوحة الإدارة الشاملة بعد نجاح الأمان والمصادقة
    else:
        st.title("🛡️ مركز الإدارة والتشييد الرقمي للمنصة الكبرى")
        st.subheader(f"مرحباً بك يا مهندس: {st.session_state.get('user_data', {}).get('full_name', 'يعرب ناصيف')}")
        
        if st.button("⬅️ تسجيل خروج آمن من لوحة الإدارة والعودة للموقع", type="primary", use_container_width=True):
            st.session_state.admin_auth = False
            st.session_state.is_admin_login = False
            st.rerun()
            
        st.divider()
        
        # تقسيم لوحة التحكم إلى 4 ألسنة تبويب احترافية (Tabs) لتغذية قاعدة البيانات بالتوازي
        adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs([
            "👥 إدارة سجلات الطلاب", 
            "📚 أرشيف المحاضرات والنوط", 
            "📢 لوحة الأخبار والعلامات الدراسية", 
            "📊 رفع وتعديل الجداول والنتائج"
        ])
        
        # 👥 اللسان الأول: إضافة سجلات الطلاب المعتمدين بالرقم الوطني
        with adm_tab1:
            st.subheader("👥 إضافة طالب رسمي إلى سجلات الوزارة/الكلية")
            st.write("البيانات المدخلة هنا ستكون المرجع الأساسي الذي يتحقق منه النظام عند تسجيل الطلاب.")
            
            n_name = st.text_input("الاسم الثلاثي الكامل للطالب الجديد:")
            n_serial = st.text_input("الرقم الجامعي المعتمد (Serial Number):")
            n_national = st.text_input("الرقم الوطني الرسمي (المكون من 11 رقماً):")
            
            if st.button("حفظ الطالب بالسجلات الرسمية الكبرى 💾", use_container_width=True):
                if n_name and n_serial and n_national:
                    db = get_db_func()
                    try:
                        db.execute('''
                            INSERT INTO access_gate (full_name, serial_number, national_id, password, is_verified) 
                            VALUES (?, ?, ?, '0000', 0)
                        ''', (n_name, n_serial, n_national))
                        db.commit()
                        st.success(f"✅ تم تسجيل المهندس(ة) {n_name} بنجاح في سجلات الكلية المعتمدة.")
                    except sqlite3.IntegrityError:
                        st.warning("⚠️ تنبيه أمني: هذا الرقم الجامعي أو الرقم الوطني مسجل مسبقاً في النظام!")
                    finally:
                        db.close()
                else:
                    st.error("❌ يرجى ملء كافة الخانات الثلاثية (الاسم، الرقم الجامعي، الرقم الوطني).")

        # 📚 اللسان الثاني: رفع المحاضرات ومطابقتها ديناميكياً مع الـ 66 مادة
        with adm_tab2:
            st.subheader("📚 إدراج محاضرة أو مقرر دراسي جديد بالأرشيف")
            years_list = ["السنة الأولى", "السنة الثانية", "السنة الثالثة", "السنة الرابعة", "السنة الخامسة"]
            sel_y = st.selectbox("اختر السنة الدراسية المستهدفة بمادة الأرشيف:", years_list)
            
            db = get_db_func()
            # جلب المواد الـ 66 الخاصة بالسنة المختارة تلقائيًا وديناميكيًا من جدول subjects
            subs = db.execute("SELECT DISTINCT subject_name FROM subjects WHERE academic_year=?", (sel_y,)).fetchall()
            db.close()
            
            if subs:
                sel_sub = st.selectbox("اختر المادة الهندسية المعتمدة:", [s['subject_name'] for s in subs])
                lec_t = st.text_input("عنوان أو رقم المحاضرة (مثال: مقرر مقاومة المواد - القسم الأول):")
                
                st.info("💡 المنصة تدعم كافة الروابط: ملفات المخططات (DWG الأوتوكاد)، حسابات الساب والإيتيبس، ملفات الإكسل، ونوط الوورد والبوربوينت.")
                lec_u = st.text_input("ضع رابط الملف السحابي المباشر (Google Drive / Telegram Link):")
                
                if st.button("إرسال ونشر المحاضرة رسميًا في الأرشيف 🚀", use_container_width=True):
                    if lec_t and lec_u:
                        db = get_db_func()
                        db.execute('''
                            INSERT INTO university_archive (academic_year, subject_name, lecture_title, file_url) 
                            VALUES (?, ?, ?, ?)
                        ''', (sel_y, sel_sub, lec_t, lec_u))
                        db.commit()
                        db.close()
                        st.success(f"✅ تم نشر مادة المقررات '{lec_t}' وإدراجها بالأرشيف بنجاح.")
                    else:
                        st.error("❌ يرجى تعبئة عنوان ورابط المقرر الدراسي أولاً.")
            else:
                st.warning("⚠️ لم يتم العثور على مواد مدرجة في جدول قاعدة البيانات لهذه السنة.")

        # 📢 اللسان الثالث: نشر الإعلانات والأخبار والعلامات الدراسية
        with adm_tab3:
            st.subheader("📢 نشر إعلان، خبر جامعي، أو كشوف العلامات الدراسية")
            st.write("هنا يمكنك نشر البيانات والنصوص والملفات. سيتم دمج نتائج المواد الفرعية وكشوف الدرجات بداخل هذا القسم بناءً على السنة الدراسية.")
            
            n_title = st.text_input("عنوان الإعلان أو كشف الدرجات الرئيسي:")
            n_text = st.text_area("تفاصيل ونص الإعلان أو الملاحظات الهندسية للطلاب:")
            n_target = st.selectbox("السنة المستهدفة بهذا الخبر/العلامات:", ["العام"] + years_list)
            
            st.info("🔗 توافق كامل: يمكنك إرفاق صور القرارات، جداول إكسل للدرجات، أو ملفات PDF متوافقة 100% لتفتح فوراً داخل محركات أجهزة الأندرويد والآيفون.")
            n_url = st.text_input("رابط الملف المرفق بالإعلان (اختياري - ضع رابط الملف أو الصورة إن وجد):")
            
            if st.button("نشر الإعلان وعرضه على لوحة الطلاب فوراً 📢", use_container_width=True):
                if n_title and n_text:
                    db = get_db_func()
                    # تم دمج وحفظ رابط الملف المرفق ميديا وتخصيص نوعها لخدمة مشروعك هندسة
                    db.execute('''
                        INSERT INTO college_news (news_title, news_text, media_url, media_type, target_year) 
                        VALUES (?, ?, ?, 'file', ?)
                    ''', (n_title, n_text, n_url if n_url else '', n_target))
                    db.commit()
                    db.close()
                    st.success("📢 تم إدراج ونشر الإعلان بنجاح وجاهز الآن للعرض الفوري للطلاب.")
                else:
                    st.error("❌ يرجى ملء عنوان ونص الإعلان كحد أدنى للنشر.")

        # 📊 اللسان الرابع: رفع النتائج الامتحانية الرسمية للامتحانات العامة
        with adm_tab4:
            st.subheader("📊 لوحة إعلان النتائج الامتحانية والدرجات الرسمية للكلية")
            r_year = st.selectbox("السنة الدراسية للنتيجة العامة المعلنة:", years_list)
            r_title = st.text_input("عنوان النتيجة الامتحانية الكبرى (مثال: نتيحة خرسانة مسلح 1 - الدورة الفصلية الأولى):")
            
            st.caption("🔒 حماية أمنية: يفضل رفع ملفات النتائج بصيغة PDF؛ حيث تم تصميم روابطها لتفتح تلقائيًا وبسلاسة تامة داخل متصفحات الموبايل (أندرويد وآيفون) والكمبيوتر بدون مشاكل.")
            r_url = st.text_input("رابط ملف النتيجة PDF المرفوع على سيرفر الكلية أو الدرايف:")
            
            if st.button("اعتماد ونشر النتيجة الامتحانية للعموم 📊", use_container_width=True):
                if r_title and r_url:
                    db = get_db_func()
                    db.execute('''
                        INSERT INTO exam_results (academic_year, result_title, pdf_url) 
                        VALUES (?, ?, ?)
                    ''', (r_year, r_title, r_url))
                    db.commit()
                    db.close()
                    st.success(f"📊 تم إدراج النتيجة الامتحانية الرسمية لمادة '{r_title}' بنجاح وبدء بثها على لوحات الطلاب.")
                else:
                    st.error("❌ يرجى إدخال عنوان المقرر الدراسي ورابط الـ PDF الصحيح لنشر النتيجة.")
