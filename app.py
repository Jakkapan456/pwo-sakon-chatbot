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

# 3. ปรับแต่ง CSS หลักแบบปลอดภัย
st.markdown(f"""
    <style>
    html, body {{
        scroll-behavior: smooth;
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
        padding-top: 3rem !important; 
        padding-bottom: 8rem !important; 
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}

    .stAppDeployButton, 
    [data-testid="stAppDeployButton"], 
    div[class*="viewerBadge"] {{
        transform: scale(0.6) !important; 
        transform-origin: bottom right !important; 
        opacity: 0.3 !important; 
        transition: all 0.3s ease !important;
        z-index: 999 !important;
    }}
    
    .stAppDeployButton:hover, 
    [data-testid="stAppDeployButton"]:hover, 
    div[class*="viewerBadge"]:hover {{
        opacity: 1 !important;
        transform: scale(0.8) !important;
    }}

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

    [data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {{
        background-color: #FFE4E1 !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        max-width: 80% !important;
        width: fit-content !important;
        border-bottom-right-radius: 4px !important;
        border: 1px solid #FFB6C1 !important;
    }}

    [data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) {{
        background-color: #FFFFFF !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        max-width: 85% !important;
        width: fit-content !important;
        border-bottom-left-radius: 4px !important;
        border: 1px solid #FFD1DC !important;
    }}
    
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 8rem !important;
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

# 🚨 11. สคริปต์ JavaScript แบบฝังรากลึก (Global Event Listener) ทำงานทุกครั้ง 🚨
components.html(
    """
    <script>
        const win = window.parent.window;
        const doc = window.parent.document;
        
        // ตรวจสอบว่าเคยฝังคำสั่งนี้ไปหรือยัง เพื่อไม่ให้มันทำงานซ้ำซ้อน
        if (!win._globalSidebarListenerActive) {
            
            // ดักจับการคลิกทุกอย่างที่เกิดขึ้นในหน้าจอเว็บ (ทำงานตลอดกาล)
            doc.addEventListener('click', function(e) {
                const sidebar = doc.querySelector('[data-testid="stSidebar"]');
                
                // ตรวจสอบว่าผู้ใช้คลิกโดนพื้นที่ "ภายใน Sidebar" ใช่หรือไม่
                if (sidebar && sidebar.contains(e.target)) {
                    
                    // เช็คให้แน่ใจว่าคลิกโดน "ปุ่มคำถาม" (ไม่ใช่ปุ่มกากบาทปิดหน้าต่างด้านบน)
                    const isHeader = e.target.closest('[data-testid="stSidebarHeader"]');
                    const isClickable = e.target.closest('button') || e.target.closest('div[role="button"]');
                    
                    if (!isHeader && isClickable) {
                        
                        // รอเสี้ยววินาทีให้ระบบรับคำสั่งกล่องแชทไปก่อน แล้วจึงสั่ง "ปิดหน้าต่าง" ทันที
                        setTimeout(() => {
                            // จำลองการกดปุ่ม X (กากบาท) หรือลูกศรปิด
                            const closeBtn = doc.querySelector('button[aria-label="Close sidebar"]') || 
                                             doc.querySelector('[data-testid="stSidebarHeader"] button') ||
                                             doc.querySelector('button[kind="header"]');
                            if (closeBtn) {
                                closeBtn.click();
                            }
                            
                            // ส่งคำสั่งกดยกเลิก (ESC) ซ้ำอีกชั้น เผื่อมือถือบางรุ่นไม่ตอบสนอง
                            doc.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, code: 'Escape', bubbles: true }));
                            
                            // เลื่อนหน้าต่างแชทลงด้านล่างสุดให้สมูท
                            const mainArea = doc.querySelector('section.main');
                            if (mainArea) {
                                mainArea.scrollTo({ top: mainArea.scrollHeight, behavior: 'smooth' });
                            }
                        }, 150); 
                    }
                }
            }, true); // ใช้โหมด Capture ดักจับก่อนที่โค้ดอื่นๆ จะทำงาน
            
            // บันทึกสถานะว่าระบบดักจับทำงานแล้ว
            win._globalSidebarListenerActive = true; 
        }
    </script>
    """,
    height=0,
    width=0,
)