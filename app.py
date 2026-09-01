import streamlit as st
import google.generativeai as genai
import PyPDF2

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

    # ปุ่มอัปโหลดไฟล์ เปลี่ยนเป็นรองรับ PDF
    uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ PDF เพื่อให้ AI วิเคราะห์", type=['pdf'])

    if uploaded_file is not None:
        st.success("✅ อัปโหลดไฟล์สำเร็จ!")
        
        # แกะข้อความจากไฟล์ PDF
        file_content = ""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    file_content += text + "\n"
            
            with st.expander("ดูเนื้อหาที่แกะได้จาก PDF"):
                st.text(file_content[:1000] + "...\n(แสดงเพียงส่วนแรก)")
                
        except Exception as e:
            st.error(f"ไม่สามารถอ่านไฟล์ PDF ได้: {e}")
        
        # ถ้ามีเนื้อหา ค่อยให้ AI ทำงาน
        if file_content.strip():
            user_prompt = st.text_input("💬 พิมพ์คำสั่งให้ AI ทำอะไรกับไฟล์นี้ (เช่น สรุปเนื้อหา):")
            
            if st.button("🚀 ส่งให้ AI ประมวลผล") and user_prompt:
                with st.spinner("AI กำลังคิด..."):
                    try:
                        full_prompt = f"{user_prompt}\n\nเนื้อหาข้อมูล:\n{file_content}"
                        response = model.generate_content(full_prompt)
                        
                        st.markdown("### 💡 ผลลัพธ์จาก AI:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("⚠️ ไม่พบข้อความในไฟล์ PDF นี้ (อาจเป็นไฟล์ที่สแกนเป็นรูปภาพ)")
