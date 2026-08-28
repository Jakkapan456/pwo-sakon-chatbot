import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from responses import get_ai_response
from components import render_header, render_sidebar
from PIL import Image
from config import LOGO_URL  

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="AI ผู้ช่วยสิทธิสวัสดิการ พมจ.สกลนคร",
    page_icon=LOGO_URL,  
    layout="wide",
    initial_sidebar_state="auto"
)

# 📌 ฟังก์ชันตั้งค่า Sidebar แบบเคลียร์ f-string ออกทั้งหมด ป้องกัน Error 100%
def set_sidebar_background(image_file):
    try:
        encoded_string = ""
        if os.path.exists(image_file):
            with open(image_file, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
        
        css = f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.82), rgba(255, 255, 255, 0.82)), url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"], 
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] .stButton > button {{
            background: linear-gradient(135deg, #FFF8DC 0%, #FFD700 50%, #DAA520 100%) !important; 
            border: 2px solid #FF8C00 !important; 
            border-radius: 16px !important; 
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.5) !important; 
            transition: all 0.3s ease !important; 
            transform: none !important;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"]:hover, 
        [data-testid="stSidebar"] button:hover,
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: linear-gradient(135deg, #FFFFE0 0%, #FFC107 50%, #FF8C00 100%) !important; 
            border-color: #FF4500 !important; 
            box-shadow: 0 8px 30px rgba(255, 165, 0, 0.8) !important; 
            transform: none !important;
        }}

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
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        pass

# 📌 เรียกใช้งานฟังก์ชันตั้งค่า Sidebar
set_sidebar_background("sidebar_bg.jpg") 

# 2. แปลงรูปภาพ bg_lotus.jpg ให้เป็น Base64 อัตโนมัติสำหรับทำพื้นหลังตรงกลาง
lotus_img_path = "bg_lotus.jpg"
lotus_base64 = ""
if os.path.exists(lotus_img_path):
    with open(lotus_img_path, "rb") as f:
        lotus_base64 = base64.b64encode(f.read()).decode()

# 3. ปรับแต่ง CSS หลักของหน้าเว็บ
st.markdown("""
    <style>
    html, body {
        scroll-behavior: smooth;
        height: 100%;
    }
    .stApp { 
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }
    
    button:hover, 
    .stButton > button:hover, 
    div[data-testid="stExpander"]:hover {
        transform: none !important;
    }

    .block-container {
        max-width: 100% !important;
        width: 100% !important;
        min-height: 100vh !important;
        padding-top: 12rem !important; 
        padding-bottom: 8rem !important; 
        margin: 0 !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-radius: 0px !important;
        box-shadow: none !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }

    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
        background-color: #ffffff !important;
        border: 2px solid #FF80AB !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        box-shadow: 0 4px 12px rgba(233, 30, 99, 0.3) !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    [data-testid="collapsedControl"] svg {
        fill: #E91E63 !important;
        width: 24px !important;
        height: 24px !important;
    }

    #MainMenu, footer {
        display: none !important;
    }

    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 100% !important;
        }
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 6rem !important;
        }
    }
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
        st.session_state.sidebar_state = "collapsed"
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