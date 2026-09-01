import streamlit as st
import google.generativeai as genai
import tempfile
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 ผู้ช่วย AI วิเคราะห์ไฟล์ PDF")

# ดึง API Key
api_key = st.secrets.get("GOOGLE_API_KEY", "")

if not api_key:
    st.error("⚠️ ไม่พบ API Key กรุณาตั้งค่า GOOGLE_API_KEY ใน Streamlit Secrets")
else:
    # ตั้งค่า Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # ปุ่มอัปโหลดไฟล์
    uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ PDF เพื่อให้ AI วิเคราะห์", type=['pdf'])

    if uploaded_file is not None:
        st.success("✅ อัปโหลดไฟล์สำเร็จ!")
        
        # สร้างไฟล์ชั่วคราวเพื่อให้ Gemini อ่านได้โดยตรง
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name

        user_prompt = st.text_input("💬 พิมพ์คำสั่งให้ AI ทำอะไรกับไฟล์นี้ (เช่น สรุปเนื้อหาทั้งหมด):")
        
        if st.button("🚀 ส่งให้ AI ประมวลผล") and user_prompt:
            with st.spinner("AI กำลังอ่านและประมวลผล..."):
                try:
                    # อัปโหลดไฟล์เข้าสู่ระบบของ Gemini
                    gemini_file = genai.upload_file(path=temp_path, mime_type="application/pdf")
                    
                    # สั่งให้ AI ทำงานโดยส่งคำสั่งพร้อมกับไฟล์
                    response = model.generate_content([user_prompt, gemini_file])
                    
                    st.markdown("### 💡 ผลลัพธ์จาก AI:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
                finally:
                    # ลบไฟล์ชั่วคราวทิ้งเมื่อเสร็จสิ้น
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
