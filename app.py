import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import re
import qrcode
from io import BytesIO
from responses import get_ai_response
from components import render_header, render_sidebar
from PIL import Image
from config import LOGO_URL  

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="AI ผู้ช่วยสิทธิสวัสดิการ พมจ.สกลนคร",
    page_icon=LOGO_URL,  
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 📌 ฟังก์ชันตั้งค่า Sidebar
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
        }}
        
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
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except Exception as e:
        pass

set_sidebar_background("sidebar_bg.jpg") 

# 2. แปลงรูปภาพ bg_lotus.jpg สำหรับทำพื้นหลังหน้าจอหลัก
lotus_img_path = "bg_lotus.jpg"
lotus_base64 = ""
if os.path.exists(lotus_img_path):
    with open(lotus_img_path, "rb") as f:
        lotus_base64 = base64.b64encode(f.read()).decode()

# 3. ปรับแต่ง CSS หลัก (ท่าไม้ตายลบปุ่ม + ดันกล่องแชททับ)
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

    .block-container {{
        max-width: 100% !important;
        width: 100% !important;
        padding-top: 4rem !important; 
        padding-bottom: 12rem !important; 
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }}

    /* 📌 รักษาปุ่มเมนูมุมซ้ายบนไว้ แต่ซ่อนแถบเครื่องมือมุมขวาบน (Fork/GitHub) */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    [data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* 🚨 ท่าไม้ตาย 1: ใช้ CSS กวาดล้างปุ่มแดง/ม่วงทุกชื่อคลาสที่เป็นไปได้ 🚨 */
    #MainMenu, footer {{ display: none !important; visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}
    #manage-app-button {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}
    [data-testid="manage-app-button"] {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}
    div[class*="viewerBadge"] {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}
    div[class*="styles_viewerBadge"] {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}
    iframe[title*="Streamlit"] {{ display: none !important; opacity: 0 !important; pointer-events: none !important; }}

    /* จัดรูปแบบกล่องแชทไร้เส้นขอบ */
    [data-testid="stChatMessage"] {{
        padding: 12px 16px !important;
        font-size: 15px !important;
        border-radius: 16px !important;
        margin-bottom: 14px !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}
    [data-testid="stChatMessage"] * {{
        border: none !important;
        box-shadow: none !important;
    }}

    /* แชทผู้ใช้ (User) ชิดขวา */
    [data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {{
        background-color: #FFE4E1 !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        max-width: 80% !important;
        width: fit-content !important;
        border-bottom-right-radius: 4px !important;
        border: 1px solid #FFB6C1 !important;
    }}

    /* แชทผู้ช่วย AI ชิดซ้าย */
    [data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {{
        background-color: #FFFFFF !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        max-width: 85% !important;
        width: fit-content !important;
        border-bottom-left-radius: 4px !important;
        border: 1px solid #FFD1DC !important;
    }}

    /* 📱 ปรับแต่งสำหรับหน้าจอมือถือโดยเฉพาะ */
    @media (max-width: 768px) {{
        [data-testid="stSidebar"] {{
            min-width: 0px !important;
            max-width: 0px !important;
            width: 0px !important;
            overflow: hidden !important;
        }}
        .block-container {{
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-bottom: 14rem !important;
        }}
        
        /* 🚨 ท่าไม้ตาย 2: ดันกล่องแชทให้อยู่ "เลเยอร์บนสุด" (z-index 99999999) เหยียบปุ่มมิด! */
        [data-testid="stChatInput"] {{
            position: fixed !important;
            bottom: 15px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            width: 96% !important;
            z-index: 99999999 !important; 
            background: rgba(255, 255, 255, 1) !important; /* พื้นหลังทึบ 100% บังปุ่มสนิท */
            box-shadow: 0 -4px 15px rgba(0,0,0,0.15) !important;
            border-radius: 12px !important;
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

# 7. ฟังก์ชันสร้าง QR Code
def generate_qrcode_image(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

def extract_links_and_render(text):
    st.markdown(text, unsafe_allow_html=True)
    urls = re.findall(r'(https?://[^\s]+)', text)
    if urls:
        st.markdown("---")
        for i, url in enumerate(set(urls)):
            clean_url = url.strip('.,)];?>')
            st.info(f"📱 **QR Code สำหรับสแกนเปิดเว็บไซต์ภายนอก (หน้าที่ {i+1}):**")
            qr_bytes = generate_qrcode_image(clean_url)
            st.image(qr_bytes, width=180)
            st.link_button(f"🌐 คลิกเปิดเว็บไซต์ภายนอก (หน้าที่ {i+1})", clean_url, use_container_width=True)

# 8. แสดงกล่องแชททั้งหมด
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
            content = message["content"]
            extract_links_and_render(content)

# 9. จัดการคำตอบ AI
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
    
# 10. ช่องพิมพ์ข้อความ
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

# 11. สคริปต์ JavaScript แบบมีเกราะป้องกัน: เลื่อนแชท + แอบลบปุ่ม (ไม่พังแม้โดนบล็อก)
if len(st.session_state.messages) > 0:
    components.html(
        """
        <script>
            function safeManageUI() {
                try {
                    const doc = window.parent.document;
                    
                    // สแกนลบปุ่มกวนใจ
                    const badBadges = doc.querySelectorAll('.stDeployButton, [id*="manage-app"], [class*="viewerBadge"]');
                    badBadges.forEach(btn => {
                        btn.style.setProperty('display', 'none', 'important');
                        btn.style.setProperty('opacity', '0', 'important');
                    });

                    // พับ Sidebar และเลื่อนแชทลง
                    const mainArea = doc.querySelector('section.main');
                    if (mainArea) {
                        mainArea.click();
                        mainArea.scrollTo({ top: mainArea.scrollHeight, behavior: 'smooth' });
                    }
                    const chatMessages = doc.querySelectorAll('[data-testid="stChatMessage"]');
                    if (chatMessages.length > 0) {
                        chatMessages[chatMessages.length - 1].scrollIntoView({ behavior: 'smooth', block: 'end' });
                    }
                } catch(e) {
                    // หากเซิร์ฟเวอร์บล็อก จะไม่ฟ้อง Error ขาวโพลนอีกต่อไป
                    console.log("UI Adjusted Safely.");
                }
            }

            safeManageUI();
            setTimeout(safeManageUI, 500);
            setInterval(safeManageUI, 2000);
        </script>
        """,
        height=0,
        width=0,
    )