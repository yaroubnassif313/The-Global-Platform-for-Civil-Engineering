# -*- coding: utf-8 -*-
import streamlit as st
import os

def show_sidebar(get_auth_db_func):
    """
    عرض وتفعيل السايد بار الحديدي والدائم بالتوازي مع المحرك الرئيسي.
    يحتوي على الهيكل الإداري للكلية، الدعم الفني المباشر، وبوابة الدخول للمشرفين.
    """
    with st.sidebar:
        # --- 1. شعار الكلية الصغير والمتناسق في أعلى السايد بار ---
        col_img1, col_img2, col_img3 = st.columns([1, 1.5, 1])
        with col_img2:
            if os.path.exists("civil_logo.jpg"):
                st.image("civil_logo.jpg", width=95) # أبعاد هندسية متناسقة للظهور بجمالية فائقة على الموبايل والكمبيوتر
            else:
                st.markdown("<p style='text-align: center; font-size: 30px; margin:0;'>🏗️</p>", unsafe_allow_html=True)
        
        # --- 2. الهيكل الإداري والقيادي المعتمد للكلية ---
        st.markdown("""
            <div style='text-align: center; margin-top: 5px; margin-bottom: 15px;'>
                <h4 style='margin: 0; color: #1F4068; font-weight: bold; font-size: 18px;'>إدارة كلية الهندسة المدنية</h4>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div style='text-align: right; background-color: rgba(31, 64, 104, 0.04); padding: 12px; border-radius: 10px; border-right: 4px solid #1F4068;'>
                <p style='margin: 0 0 6px 0; font-size: 14px;'>🎓 <b>عميد الكلية:</b> الدكتور محسن أحمد</p>
                <p style='margin: 0 0 6px 0; font-size: 14px;'>🏛️ <b>النائب الإداري:</b> الدكتور عصام غزولين</p>
                <p style='margin: 0; font-size: 14px;'>🔬 <b>النائب العلمي:</b> الدكتور شريف الحايك</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        
        # --- 3. بوابة إشراف المنصة (إصلاح منطق المعاملات وزوال الخطأ الفوري) ---
        if st.button("⚙️ بوابة إشراف المنصة", type="secondary", use_container_width=True):
            st.session_state.is_admin_login = True
            st.session_state.admin_auth = False # تصفير أمان الأدمن لطلب الباسورد حماية للقواعد
            st.rerun()
            
        st.divider()
        
        # --- 4. قسم الدعم الفني والاتصال الفوري المباشر ---
        st.markdown("""
            <div style='text-align: right;'>
                <h5 style='color: #1F4068; font-weight: bold; margin-bottom: 5px;'>📞 الدعم الفني للمنصة</h5>
                <p style='color: #555; font-size: 13px; line-height: 1.4;'>إن واجهتك أي مشكلة برمجية أو تقنية في تفعيل حسابك، يمكنك التواصل مع مطور المنصة مباشرة:</p>
            </div>
            """, unsafe_allow_html=True)
            
        # زر الواتساب التفاعلي المباشر مع رقمك المهندس يعرب
        st.write("💬 **رقم الواتساب المعتمد:**")
        st.code("0992325041")
        st.link_button(
            "الانتقال الفوري إلى واتساب 🚀", 
            "https://wa.me", 
            use_container_width=True
        )
        
        st.write("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        
        # زر التليجرام التفاعلي المباشر مع حسابك
        st.write("✈️ **معرف تليجرام المعتمد:**")
        st.code("@AMS0012")
        st.link_button(
            "الانتقال الفوري إلى تليجرام 🚀", 
            "https://t.me", 
            use_container_width=True
        )
        
        st.divider()
        
        # --- 5. توثيق الحقوق والفخر في ذيل السايد بار المعتمد لعام 2026 ---
        st.markdown("""
            <div style='text-align: center; color: #888; font-size: 12px; font-weight: bold;'>
                تم التصميم بكل موثوقية وفخر © 2026
            </div>
            """, unsafe_allow_html=True)
