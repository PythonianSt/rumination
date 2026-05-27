import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

st.set_page_config(page_title="Thai Rumination Helper", page_icon="🧠", layout="centered")

st.title("🧠 ตัวช่วยแปลงความคิดวนซ้ำ")
st.caption("Rumination → Healthy Reflection โดยใช้ GPT")

st.warning(
    "เครื่องมือนี้ไม่ใช่การวินิจฉัยหรือการรักษาโรค "
    "หากมีความคิดทำร้ายตนเองหรือไม่ปลอดภัย โปรดติดต่อคนใกล้ชิด แพทย์ หรือสายด่วนฉุกเฉินทันที"
)

thought = st.text_area(
    "เขียนความคิดที่วนซ้ำอยู่ในใจ",
    height=180,
    placeholder="เช่น เขาไม่ตอบไลน์ แปลว่าเขาคงไม่ชอบเราแน่ ๆ..."
)

context = st.text_input(
    "บริบทสั้น ๆ ถ้ามี",
    placeholder="เช่น เรื่องเรียน งาน ความสัมพันธ์ สุขภาพ"
)

style = st.selectbox(
    "รูปแบบคำแนะนำ",
    [
        "อ่อนโยนและให้กำลังใจ",
        "สั้น กระชับ ใช้ได้ทันที",
        "เหมือนโค้ชถามกลับ",
        "เหมือนพยาบาล/แพทย์ให้คำปรึกษา"
    ]
)

def analyze_rumination(thought, context, style):
    prompt = f"""
คุณคือผู้ช่วยภาษาไทยด้านสุขภาวะจิตใจ
เป้าหมาย: ช่วยแยก "ความคิดวนซ้ำ/rumination" ออกจาก "healthy reflection"
ห้ามวินิจฉัยโรค ห้ามกล่าวเกินจริง ห้ามแทนที่แพทย์/นักจิตวิทยา

ข้อมูลจากผู้ใช้:
ความคิด: {thought}
บริบท: {context}
รูปแบบ: {style}

กรุณาตอบเป็นภาษาไทยในรูปแบบนี้:

1) ความคิดนี้เป็น rumination ตรงไหน
- ระบุ pattern เช่น คิดวน, โทษตัวเอง, อ่านใจคนอื่น, คาดการณ์ร้าย, all-or-none thinking

2) อารมณ์และความต้องการที่ซ่อนอยู่
- เช่น กลัวถูกปฏิเสธ ต้องการความมั่นใจ ต้องการความปลอดภัย

3) แปลงเป็น healthy reflection
ให้เขียนใหม่ 3 ประโยค:
- ประโยคที่เมตตาต่อตนเอง
- ประโยคที่อยู่กับข้อเท็จจริง
- ประโยคที่นำไปสู่การกระทำ

4) คำถามสะท้อนคิด 3 ข้อ
- ถามแบบไม่ตัดสิน

5) Action เล็ก ๆ ภายใน 10 นาที
- ทำได้จริง ปลอดภัย ไม่ซับซ้อน

6) ถ้ามีสัญญาณอันตราย
- ให้แนะนำพบผู้เชี่ยวชาญหรือขอความช่วยเหลือทันที
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
    )
    return response.output_text

if st.button("🔄 แปลงเป็น Healthy Reflection"):
    if not thought.strip():
        st.error("กรุณาเขียนความคิดที่วนซ้ำก่อน")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("ไม่พบ OPENAI_API_KEY ในไฟล์ .env")
    else:
        with st.spinner("กำลังช่วยแปลงความคิด..."):
            try:
                result = analyze_rumination(thought, context, style)
                st.subheader("ผลลัพธ์")
                st.markdown(result)

                st.download_button(
                    "📄 ดาวน์โหลดผลลัพธ์เป็นไฟล์ .txt",
                    data=result,
                    file_name="thai_rumination_reflection.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

st.divider()

st.subheader("ตัวอย่างการเปลี่ยนมุมคิด")
st.markdown("""
**Rumination:**  
“ฉันทำพลาดอีกแล้ว ฉันคงไม่เหมาะกับงานนี้”

**Healthy reflection:**  
“วันนี้ฉันทำบางอย่างพลาด แต่ฉันยังเรียนรู้ได้  
ข้อเท็จจริงคือมีจุดหนึ่งที่ต้องปรับ  
สิ่งที่ทำต่อได้คือถาม feedback และแก้ทีละขั้น”
""")