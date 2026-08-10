# -*- coding: utf-8 -*-
import streamlit as st

def show_sidebar(get_db_func=None):
    """
    عرض وتفعيل السايد بار الذكي بالتوازي مع المحرك الرئيسي.
    يظهر فقط عندما يكون الطالب في الصفحة الترحيبية الأولى (welcome).
    """
    # تبسيط الشرط لضمان الظهور الفوري في الصفحة الأولى
    if st.session_state.step == 'welcome':
        with st.sidebar:
            st.title("🏛️ بوابة التحكم")
            st.caption("المنصة الكبرى لجامعة اللاذقية")
            st.divider()
            
            # 🔐 زر تسجيل الدخول كمشرف
            if st.button("⚙️ تسجيل الدخول كمشرف", type="secondary", use_container_width=True):
                st.session_state.is_admin_login = True
                st.rerun()
            
            st.divider()
            st.subheader("📞 قسم الدعم الفني")
            st.write("يمكنك التواصل مع مطور المنصة مباشرة عبر الأزرار أدناه:")
            
            # 🟢 زر الواتساب الذكي المباشر مع رقمك
            st.write("💬 **رقم الواتساب المعتمد:**")
            st.code("0992325041")
            st.link_button(
                "الانتقال الفوري إلى واتساب 🚀", 
                "https://wa.me", 
                use_container_width=True
            )
            
            st.write("---")
            
            # 💬 زر التليجرام الذكي المباشر مع حسابك
            st.write("✈️ **معرف تليجرام المعتمد:**")
            st.code("@AMS0012")
            st.link_button(
                "الانتقال الفوري إلى تليجرام 🚀", 
                "https://t.me", 
                use_container_width=True
            )
            
            st.divider()
            st.caption("تم التطوير بكل فخر وموثوقية © 2026 👷‍♂️")
