import streamlit as st
import google.generativeai as genai
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 ผู้ช่วย AI พร้อมระบบอัปโหลดไฟล์")

# ตั้งค่า API Key (ดึงจาก Streamlit Secrets หรือใส่ตรงนี้ชั่วคราวได้)
# แนะนำให้ตั้งค่า GOOGLE_API_KEY ในหน้าตั้งค่าของ Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.error("⚠️ ไม่พบ API Key กรุณาตั้งค่า GOOGLE_API_KEY ใน Streamlit Secrets")
else:
    # เริ่มต้นการเชื่อมต่อกับ Google Gemini
    genai.configure(api_key=api_key)
    
    # ใช้โมเดลเวอร์ชันที่อัปเดตล่าสุดเพื่อแก้ปัญหา 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # สร้างปุ่มอัปโหลดไฟล์
    uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ข้อความ (TXT) เพื่อให้ AI วิเคราะห์", type=['txt'])

    if uploaded_file is not None:
        st.success("✅ อัปโหลดไฟล์สำเร็จ!")
        
        # อ่านเนื้อหาจากไฟล์
        file_content = uploaded_file.getvalue().decode("utf-8")
        with st.expander("ดูเนื้อหาในไฟล์"):
            st.text(file_content)
        
        # ช่องรับคำสั่งจากผู้ใช้
        user_prompt = st.text_input("💬 พิมพ์คำสั่งให้ AI ทำอะไรกับไฟล์นี้ (เช่น สรุปเนื้อหา, หาจุดสำคัญ):")
        
        if st.button("🚀 ส่งให้ AI ประมวลผล") and user_prompt:
            with st.spinner("AI กำลังคิด..."):
                try:
                    # รวมคำสั่งและเนื้อหาไฟล์เข้าด้วยกัน
                    full_prompt = f"{user_prompt}\n\nเนื้อหาข้อมูล:\n{file_content}"
                    response = model.generate_content(full_prompt)
                    
                    # แสดงผลลัพธ์
                    st.markdown("### 💡 ผลลัพธ์จาก AI:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
