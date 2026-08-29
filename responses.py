import os
import re
import streamlit as st  # 📌 เพิ่มการเรียกใช้งาน streamlit
from google import genai
from google.genai import types

from knowledge_base_child_2 import LAW_CHILD_KNOWLEDGE
from knowledge_base_family_3 import LAW_DOMESTIC_VIOLENCE_KNOWLEDGE
from knowledge_base_elderly_4 import LAW_ELDERLY_KNOWLEDGE
from knowledge_base_welfare_5 import LAW_WELFARE_KNOWLEDGE
from knowledge_base_community_6 import LAW_COMMUNITY_KNOWLEDGE
from knowledge_base_disabled_7 import LAW_DISABLED_KNOWLEDGE 

# 📌 เปลี่ยนมาดึง API Key จาก Streamlit Secrets อย่างปลอดภัย
API_KEYS = [
    st.secrets["GEMINI_API_KEY_1"],
    st.secrets["GEMINI_API_KEY_2"]
]

# 📌 กำหนดข้อความความรู้พื้นฐาน (แทนส่วนของ knowledge_base 1 ที่ลบไป)
SYSTEM_KNOWLEDGE = """
ข้อมูลพื้นฐานสำนักงานพัฒนาสังคมและความมั่นคงของมนุษย์จังหวัดสกลนคร (พมจ.สกลนคร):
มีหน้าที่ในการขับเคลื่อนงานด้านสวัสดิการสังคม การคุ้มครองและพัฒนาคุณภาพชีวิตเด็ก เยาวชน สตรี ครอบครัว ผู้สูงอายุ คนพิการ และผู้ด้อยโอกาสในพื้นที่จังหวัดสกลนคร
"""

def get_ai_response(contents):
    if isinstance(contents, list):
        user_message = " ".join([str(item) for item in contents if isinstance(item, str)])
    elif isinstance(contents, dict):
        user_message = contents.get("prompt", "") or contents.get("content", "")
    else:
        user_message = str(contents)
        
    msg = user_message.lower().strip()

    # 📌 ระบบคัดเลือกคลังความรู้เฉพาะหมวดที่เกี่ยวข้อง เพื่อประหยัด Quota Tokens ไม่ให้เกินลิมิต
    selected_knowledge = SYSTEM_KNOWLEDGE
    
    if any(keyword in msg for keyword in ["เด็ก", "แรกเกิด", "เยาวชน", "คุ้มครองเด็ก"]):
        selected_knowledge += "\n" + LAW_CHILD_KNOWLEDGE
    if any(keyword in msg for keyword in ["ครอบครัว", "สตรี", "ความรุนแรง", "สามีภรรยา"]):
        selected_knowledge += "\n" + LAW_DOMESTIC_VIOLENCE_KNOWLEDGE
    if any(keyword in msg for keyword in ["ผู้สูงอายุ", "คนแก่", "เบี้ยยังชีพ"]):
        selected_knowledge += "\n" + LAW_ELDERLY_KNOWLEDGE
    if any(keyword in msg for keyword in ["สวัสดิการ", "สังคม", "สงเคราะห์"]):
        selected_knowledge += "\n" + LAW_WELFARE_KNOWLEDGE
    if any(keyword in msg for keyword in ["ชุมชน", "อพม", "สภาองค์กรชุมชน", "พสช", "codi"]):
        selected_knowledge += "\n" + LAW_COMMUNITY_KNOWLEDGE
    if any(keyword in msg for keyword in ["คนพิการ", "ความพิการ", "บัตรคนพิการ"]):
        selected_knowledge += "\n" + LAW_DISABLED_KNOWLEDGE
    
    # หากไม่ตรงหมวดไหนเลย หรือเป็นการทักทายทั่วไป ให้แนบความรู้หลักทั้งหมดแบบย่อส่วนผสมได้
    if len(selected_knowledge) < len(SYSTEM_KNOWLEDGE) + 100:
        selected_knowledge = f"""
        {SYSTEM_KNOWLEDGE}
        {LAW_CHILD_KNOWLEDGE[:1000]}
        {LAW_COMMUNITY_KNOWLEDGE[:1000]}
        {LAW_DISABLED_KNOWLEDGE[:1000]}
        """

    dynamic_system_instruction = f"""คุณคือ "AI ผู้ช่วยสิทธิสวัสดิการ พมจ.สกลนคร" สังกัดสำนักงานพัฒนาสังคมและความมั่นคงของมนุษย์จังหวัดสกลนคร

กฎการตอบคำถาม:
1. แทนตัวเองว่า "ผม" และใช้คำลงท้ายด้วย "ครับ" เท่านั้น ห้ามใช้คำว่า "ค่ะ", "คะ", "ดิฉัน", "ครับ/ค่ะ" เด็ดขาด
2. ตอบด้วยภาษาไทยที่สุภาพ อ่านง่าย กระชับ ตรงประเด็น
3. **เรื่องทั่วไป/ทักทาย/คิดเลข/คำนวณ:** ให้สนทนา ตอบคำถาม และคำนวณได้อย่างเป็นธรรมชาติ สุภาพ และเป็นมิตร ห้ามปฏิเสธการตอบ
4. **เรื่องสิทธิสวัสดิการ/กฎหมาย/พม.:** ให้ค้นหาข้อมูลที่เกี่ยวข้องจาก "คลังความรู้ที่กำหนดให้" ด้านล่างนี้ นำมาเรียบเรียงตอบผู้ใช้ทันทีอย่างครบถ้วน ห้ามตกหล่นข้อมูลสำคัญ
5. ปิดท้ายด้วยการถามคำถามปลายปิดหรือเสนอหัวข้อแนะนำสั้นๆ ด้วยคำลงท้าย "ครับ" เสมอ

--- คลังความรู้เฉพาะกิจ ---
{selected_knowledge}
"""

    # ส่งตรงไปที่ Gemini API
    for key in API_KEYS:
        try:
            client = genai.Client(api_key=key)
            response = client.models.generate_content_stream(
                model="gemini-1.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=dynamic_system_instruction,
                    temperature=0.2,
                    max_output_tokens=4096,
                ),
            )
            has_content = False
            for chunk in response:
                if chunk.text:
                    has_content = True
                    yield chunk.text
            if has_content:
                return
        except Exception as e:
            print(f"❌ API Error: {e}")
            continue
        
    # หาก API ขัดข้องทั้งหมด
    yield "ขออภัยด้วยครับ ระบบประมวลผล AI กำลังขัดข้องชั่วคราว เจ้าหน้าที่กำลังดำเนินการแก้ไขครับ"