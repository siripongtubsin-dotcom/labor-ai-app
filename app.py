import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI ผู้ช่วยพนักงานตรวจแรงงาน", layout="centered")

st.title("⚖️ AI ผู้ช่วยพนักงานตรวจแรงงาน")
st.subheader("อัปโหลดแบบฟอร์ม คร.๗ เพื่อดึงข้อมูลอัตโนมัติ")

# ใส่ช่องให้กรอก API Key ชั่วคราว (เพื่อความง่ายในการติดตั้ง)
api_key = st.text_input("ใส่ Google Gemini API Key ของคุณ:", type="password")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ภาพฟอร์ม คร.๗ (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="ไฟล์ที่อัปโหลด", use_container_width=True)
    
    if st.button("วิเคราะห์ข้อมูล"):
        with st.spinner("AI กำลังอ่านเอกสารและวิเคราะห์รูปคดี..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = """
                นี่คือเอกสารคำร้อง คร.๗ ให้คุณทำหน้าที่เป็นผู้ช่วยพนักงานตรวจแรงงาน 
                ช่วยดึงข้อมูลต่อไปนี้ออกมาให้ชัดเจน:
                1. ชื่อลูกจ้าง (ผู้ร้อง)
                2. ชื่อนายจ้าง (ผู้ถูกร้อง)
                3. ประเด็นที่ร้องเรียน (เช่น ค้างจ่ายค่าจ้าง, เลิกจ้างไม่เป็นธรรม)
                4. ข้อเสนอแนะเบื้องต้นตามกฎหมายแรงงานสำหรับกรณีนี้
                """
                response = model.generate_content([prompt, image])
                st.success("วิเคราะห์เสร็จสิ้น!")
                st.write(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
