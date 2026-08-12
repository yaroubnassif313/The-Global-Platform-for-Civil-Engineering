# -*- coding: utf-8 -*-
import streamlit as st

def show_sidebar(get_db_func=None):
    """
    عرض وتفعيل السايد بار الذكي بالتوازي مع المحرك الرئيسي.
    تم تثبيته ليعمل دائماً عند تحديث الموقع، وتم إصلاح المعاملات ليزول الخطأ تماماً.
    """
    # تم إلغاء شروط التقييد لضمان ظهور السايد بار دائماً وثباته عند كل تحديث (Refresh)
    with st.sidebar:
        st.title("🏛️ بوابة التحكم")
        st.caption("المنصة الكبرى لجامعة اللاذقية")
        st.divider()
        
        # 🔐 زر تسجيل الدخول كمشرف (تم إصلاح منطق الربط ليزول الخطأ الأحمر فوراً)
        if st.button("⚙️ تسجيل الدخول كمشرف", type="secondary", use_container_width=True):
            st.session_state.is_admin_login = True
            st.session_state.admin_auth = False # إعادة تهيئة الأمان لطلب الباسورد
            st.rerun()
        
        st.divider()
        st.subheader("📞 قسم الدعم الفني")
        st.write("يمكنك التواصل مع مطور المنصة مباشرة عبر الأزرار أدناه:")
        
        # 🟢 زر الواتساب الذكي المباشر مع رقمك المهندس يعرب
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
