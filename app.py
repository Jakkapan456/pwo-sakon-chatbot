import streamlit as st
import streamlit.components.v1 as components
import base64
from responses import get_ai_response
from components import render_header, render_sidebar
from PIL import Image
from config import LOGO_URL  

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="AI ผู้ช่วยสิทธิสวัสดิการ พมจ.สกลนคร",
    page_icon=LOGO_URL,  
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📌 ฟังก์ชันสำหรับตั้งค่ารูปภาพพื้นหลัง Sidebar พร้อมแต่งกล่องเมนูและ Popover เป็นสีเหลืองทองอร่าม
def set_sidebar_background(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        
        css = f"""
        <style>
        /* สร้างเลเยอร์สีขาวโปร่งแสง 82% (0.82) ทับบนรูปภาพ */
        [data-testid="stSidebar"] {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.82), rgba(255, 255, 255, 0.82)), url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        /* 🌟 ตกแต่งกล่องเมนูและ Expander ใน Sidebar ให้เป็นสีเหลืองทองอร่าม */
        [data-testid="stSidebar"] [data-testid="stExpander"], 
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] .stButton > button {{
            background: linear-gradient(135deg, #FFF8DC 0%, #FFD700 50%, #DAA520 100%) !important; 
            border: 2px solid #FF8C00 !important; 
            border-radius: 16px !important; 
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.5) !important; 
            transition: all 0.3s ease !important; 
            transform: none !important; /* 📌 บังคับห้ามขยับเด็ดขาด */
        }}

        /* ✨ ลูกเล่นตอนเอาเมาส์ไปชี้เมนู Sidebar (เปลี่ยนแค่สีสว่างขึ้น ไม่มีเอฟเฟกต์เด้ง) */
        [data-testid="stSidebar"] [data-testid="stExpander"]:hover, 
        [data-testid="stSidebar"] button:hover,
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: linear-gradient(135deg, #FFFFE0 0%, #FFC107 50%, #FF8C00 100%) !important; 
            border-color: #FF4500 !important; 
            box-shadow: 0 8px 30px rgba(255, 165, 0, 0.8) !important; 
            transform: none !important; /* 📌 บังคับห้ามขยับเด็ดขาด */
        }}

        /* 👑 ปรับตัวหนังสือใน Sidebar ให้คมชัดตัดกับพื้นหลังสีทอง */
        [data-testid="stSidebar"] [data-testid="stExpander"] summary p,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] button p {{
            color: #4A3B00 !important; 
            font-weight: bold !important;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        }}
        
        .streamlit-expanderHeader {{
            color: #4A3B00 !important;
            font-weight: bold !important;
        }}

        /* 📌 🌟 ตกแต่งกล่อง Popover ตรงกลางให้เป็นสีทองอร่ามแพรวพราว */
        div[data-testid="stPopoverBody"] {{
            position: fixed !important; 
            top: 50% !important;                     
            left: 320px !important;                  
            transform: translateY(-50%) !important;  
            width: 450px !important;    
            max-height: 80vh !important;             
            overflow-y: auto !important; 
            background: linear-gradient(135deg, #FFFDF0 0%, #FFF8DC 100%) !important; 
            border: 2px solid #DAA520 !important; 
            border-radius: 16px !important;
            box-shadow: 0 8px 35px rgba(218, 165, 32, 0.5) !important; 
            z-index: 999999 !important;
            padding: 15px !important;
        }}

        /* 🌟 ปรับแต่งปุ่มและตัวเลือกด้านในกล่อง Popover ให้เป็นสีทองอร่าม */
        div[data-testid="stPopoverBody"] button {{
            background: linear-gradient(135deg, #FFF8DC 0%, #FFD700 100%) !important;
            border: 1.5px solid #DAA520 !important;
            border-radius: 12px !important;
            color: #4A3B00 !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important; /* เปลี่ยนเป็นสมูท */
            transform: none !important; /* 📌 บังคับห้ามขยับเด็ดขาด */
        }}

        /* เปลี่ยนแค่สี ไม่ให้ปุ่มเด้งขยายตอน Hover */
        div[data-testid="stPopoverBody"] button:hover {{
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 20px rgba(255, 165, 0, 0.6) !important;
            transform: none !important; /* 📌 บังคับห้ามขยับเด็ดขาด */
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        pass

# 📌 เรียกใช้งานฟังก์ชันตั้งค่า Sidebar
set_sidebar_background("sidebar_bg.jpg") 

# 2. แปลงรูปภาพ bg_lotus.jpg ให้เป็น Base64 อัตโนมัติสำหรับทำพื้นหลังตรงกลาง
import os
lotus_img_path = "bg_lotus.jpg"
lotus_base64 = ""
if os.path.exists(lotus_img_path):
    with open(lotus_img_path, "rb") as f:
        lotus_base64 = base64.b64encode(f.read()).decode()

# 3. ปรับแต่ง CSS หลักของหน้าเว็บ
st.markdown(f"""
    <style>
    html, body {{
        scroll-behavior: smooth;
        height: 100%;
    }}
    .stApp {{ 
        background-image: linear-gradient(rgba(255, 240, 245, 0.85), rgba(255, 240, 245, 0.85)), url("data:image/jpeg;base64,{lotus_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* 📌 ปิดการเด้งของปุ่มทั้งหมดในเว็บแบบถาวร หักล้างโค้ดที่ซ่อนอยู่ */
    button:hover, 
    .stButton > button:hover, 
    div[data-testid="stExpander"]:hover,
    div[data-testid="stPopoverBody"] button:hover {{
        transform: none !important;
    }}

    /* 📌 ขยายพื้นที่แชท (สำหรับจอคอมพิวเตอร์) */
    .block-container {{
        max-width: 100% !important;
        width: 100% !important;
        min-height: 100vh !important;
        padding-top: 12rem !important; 
        padding-bottom: 8rem !important; 
        margin: 0 !important;
        background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url("data:image/jpeg;base64,{lotus_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-radius: 0px !important;
        box-shadow: none !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }}

    /* 📌 บังคับจัดกึ่งกลางให้โลโก้ */
    [data-testid="stVerticalBlock"] > div:has(img) {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        width: 100%;
    }}

    /* 📌 ขยับหัวข้อข้อความมาทางซ้ายเพื่อให้คำว่า "สิทธิ" ตรงกับโลโก้พอดี */
    .main-title, .sub-title {{
        text-align: center !important;
        width: 100% !important;
        transform: translateX(-35px) !important; 
    }}

    /* 📌 ล็อคช่องพิมพ์ข้อความด้านล่างให้อยู่กับที่ (สำหรับจอคอม) */
    [data-testid="stChatInput"] {{
        position: fixed !important;
        bottom: 20px !important;
        left: 55% !important;
        transform: translateX(-50%) !important;
        width: 65% !important;
        z-index: 99999 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
        border-radius: 16px !important;
    }}
    
    button[title="View fullscreen"], [data-testid="stElementToolbar"] {{ display: none !important; }}
    hr {{ margin: 15px 0; border: 0; border-top: 1px solid #E0E0E0; }}
    
    .stChatMessage {{ padding: 6px 10px !important; font-size: 14px !important; }}
    .stChatMessage[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {{
        flex-direction: row-reverse !important;
        text-align: right !important;
        background-color: #FFE4E1 !important;
        border-radius: 14px 14px 0px 14px !important;
        margin-left: auto !important;
        max-width: 75% !important;
        width: fit-content !important;
        padding: 8px 12px !important;
    }}
    .stChatMessage[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) div[data-testid="stMarkdownContainer"] p {{ text-align: right !important; }}
    .stChatMessage[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {{
        background-color: #FFFFFF !important;
        border-radius: 14px 14px 14px 0px !important;
        margin-right: auto !important;
        max-width: 80% !important;
        border: 1px solid #FFD1DC !important;
        padding: 8px 12px !important;
    }}
    .stChatMessage[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) div[data-testid="stMarkdownContainer"] p {{ text-align: left !important; }}

    /* ดีไซน์วงกลมหมุนๆ (Loading Spinner) แบบสมูท */
    .loading-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: 'Sarabun', sans-serif;
        font-size: 14px;
        color: #555555;
    }}
    .spinner {{
        width: 20px;
        height: 20px;
        border: 3px solid #FFC0CB;
        border-top: 3px solid #FF1493;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }}
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    /* 🚫 ซ่อนเมนูด้านบนและ Footer ด้านล่างของ Streamlit */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    .stApp > header {{
        display: none !important;
    }}
    #MainMenu {{
        visibility: hidden !important;
    }}
    footer {{
        display: none !important;
    }}
    .viewerBadge_container_link, .viewerBadge_link {{
        display: none !important;
    }}

    /* ========================================================
       📱 แก้ไขสำหรับมือถือโดยเฉพาะ (ให้แชทกว้างเต็มจอแบบ Gemini)
       ======================================================== */
    @media (max-width: 768px) {{
        /* ลดขอบซ้ายขวาของหน้าจอหลักลง ให้กินพื้นที่น้อยที่สุด */
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 6rem !important;
        }}
        
        /* ขยายกล่องแชทฝั่ง User ให้กว้างเกือบเต็มจอ */
        .stChatMessage[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {{
            max-width: 95% !important;
        }}
        
        /* ขยายกล่องแชทฝั่ง AI ให้กว้างเกือบเต็มจอ */
        .stChatMessage[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {{
            max-width: 95% !important;
        }}

        /* จัดช่องพิมพ์ด้านล่างให้สมดุลและอยู่ตรงกลางจอ */
        [data-testid="stChatInput"] {{
            width: 95% !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# 4. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. เรียก Sidebar ด้านซ้าย
render_sidebar()

# 6. แสดงผลหน้าแรก
if len(st.session_state.messages) == 0:
    render_header()

# 7. แสดงกล่องแชททั้งหมด
for message in st.session_state.messages:
    avatar_icon = "✨" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        if message["role"] == "user":
            user_text = message.get("content", "") or message.get("text", "")
            if user_text:
                st.write(user_text)
            if "file" in message and message["file"] is not None:
                st.image(message["file"], width=300)
        else:
            st.write(message["content"])

# 8. จัดการคำตอบ AI
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_msg = st.session_state.messages[-1]
    
    query_text = last_user_msg.get("prompt") or last_user_msg.get("text") or last_user_msg.get("content", "")
    has_file = "file" in last_user_msg and last_user_msg["file"] is not None
    
    if not query_text and has_file:
        query_text = "ช่วยอธิบายหรือวิเคราะห์รูปภาพนี้ให้หน่อยครับ"
    elif not query_text:
        query_text = "สวัสดีครับ"

    if has_file:
        try:
            pil_image = Image.open(last_user_msg["file"])
            ai_payload = [query_text, pil_image]
        except Exception:
            ai_payload = query_text
    else:
        ai_payload = query_text

    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        message_placeholder.markdown(
            """
            <div class="loading-container">
                <div class="spinner"></div>
                <span>กำลังค้นหาข้อมูลและเรียบเรียงคำตอบ...</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        ai_stream = get_ai_response(ai_payload)
        reply = message_placeholder.write_stream(ai_stream)
        
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
    
# 9. ช่องพิมพ์ข้อความ
prompt_container = st.chat_input("พิมพ์ข้อความที่นี่", accept_file=True, file_type=["jpg", "jpeg", "png", "pdf"])

if prompt_container:
    user_text = ""
    uploaded_files = []
    
    if hasattr(prompt_container, "text"):
        user_text = prompt_container.text
        if hasattr(prompt_container, "files"):
            uploaded_files = prompt_container.files
    elif isinstance(prompt_container, dict):
        user_text = prompt_container.get("text", "")
        uploaded_files = prompt_container.get("files", [])
    else:
        user_text = str(prompt_container)

    message_data = {"role": "user", "text": user_text if user_text else ""}
    
    if uploaded_files:
        message_data["file"] = uploaded_files[0]
        
    if user_text or uploaded_files:
        st.session_state.messages.append(message_data)
        st.rerun()

# 10. สคริปต์ Auto-scroll
if len(st.session_state.messages) > 0:
    components.html(
        """
        <script>
            function forceScrollToBottom() {
                const mainSection = window.parent.document.querySelector('section.main');
                if (mainSection) {
                    mainSection.scrollTo({
                        top: mainSection.scrollHeight,
                        behavior: 'smooth'
                    });
                }

                const chatMessages = window.parent.document.querySelectorAll('[data-testid="stChatMessage"]');
                if (chatMessages.length > 0) {
                    const lastMessage = chatMessages[chatMessages.length - 1];
                    lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
                }
            }

            forceScrollToBottom();
            setTimeout(forceScrollToBottom, 50);
            setTimeout(forceScrollToBottom, 150);
        </script>
        """,
        height=0,
        width=0,
    )