import streamlit as st
import google.generativeai as genai
import tempfile
import os

# 1. ใส่ API Key ของคุณตรงนี้ (เอาอันที่สร้างใหม่มาใส่นะครับ)
genai.configure(api_key="ใส่_API_KEY_ของคุณที่นี่")

st.title("ระบบสรุปเอกสารอัตโนมัติ 📄")
st.write("เพียงอัปโหลดไฟล์ ระบบจะสรุปเนื้อหาให้ทันที")

# 2. สร้างช่องให้อัปโหลดไฟล์ (รองรับ PDF และ TXT)
uploaded_file = st.file_uploader("ลากไฟล์มาวาง หรือกดเพื่อเลือกไฟล์", type=['pdf', 'txt'])

if uploaded_file is not None:
    with st.spinner("🤖 ระบบกำลังอ่านและสรุปข้อมูล โปรดรอสักครู่..."):
        # 3. บันทึกไฟล์ที่อัปโหลดลงเครื่องชั่วคราว เพื่อส่งให้ Gemini
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        try:
            # 4. อัปโหลดไฟล์ไปที่ Gemini และตั้งค่าคำสั่ง (Prompt) ที่ฝังไว้
            gemini_file = genai.upload_file(tmp_path)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # **นี่คือคำสั่งที่เราซ่อนไว้ ผู้ใช้ไม่ต้องพิมพ์เอง**
            hidden_prompt = "สรุปใจความสำคัญของเอกสารนี้ให้เข้าใจง่าย สั้นกระชับ และจัดรูปแบบเป็นหัวข้อให้อ่านง่ายที่สุด"
            
            response = model.generate_content([gemini_file, hidden_prompt])
            
            # 5. แสดงผลลัพธ์
            st.success("✅ สรุปเสร็จสิ้น!")
            st.write("### 📝 สรุปเนื้อหา:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
        finally:
            # ลบไฟล์ชั่วคราวทิ้ง
            os.remove(tmp_path)
