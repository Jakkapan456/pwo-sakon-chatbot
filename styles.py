import os
import base64

def get_ui_css():
    """
    ฟังก์ชันส่งคืน CSS สำหรับตกแต่งสีพื้นหลัง ปุ่มกด และช่องแชทพร้อมรูปภาพบึงบัว
    📌 อัปเดต: รองรับ Responsive Design ทุกขนาดหน้าจอ (Mobile, Tablet, Laptop, Desktop)
    """
    # 📌 แปลงรูปภาพ bg_lotus.jpg ให้เป็น Base64 อัตโนมัติ
    img_path = "bg_lotus.jpg"
    img_base64 = ""
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

    return f"""<style>
    /* =========================================
       1. สไตล์พื้นฐานทั่วไป (Global Styles)
       ========================================= */
    .stApp {{ 
        background: linear-gradient(180deg, #fff5f8 0%, #ffeef3 100%); 
    }}
    
    .stButton>button {{ 
        width: 100%; 
        border-radius: 20px; 
        border: 1px solid #ff80ab; 
        color: #e91e63; 
        font-weight: bold; 
        background: white; 
        transition: all 0.3s; 
        margin-bottom: 4px; 
    }}
    .stButton>button:hover {{ 
        background: linear-gradient(135deg, #e91e63, #ff4081); 
        color: white !important; 
        transform: translateY(-2px); 
    }}
    
    [data-testid="stMainBlockContainer"], .main .block-container {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.86)), url("data:image/jpeg;base64,{img_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-radius: 20px;
    }}

    .stChatMessage {{ 
        border-radius: 18px !important; 
        padding: 12px 16px !important; 
        margin-bottom: 12px !important; 
        background: linear-gradient(145deg, #fff 0%, #fff0f5 100%) !important; 
        border: 1px solid rgba(248,187,208,0.8) !important; 
        box-shadow: 0 6px 16px rgba(233,30,99,0.06) !important; 
    }}
    [data-testid="stChatMessageAvatarAssistant"] {{ 
        background: white !important; 
        border: 2px solid #ff80ab !important; 
        border-radius: 50% !important; 
    }}
    
    .user-container {{ 
        display: flex; 
        justify-content: flex-end; 
        margin-bottom: 12px; 
        width: 100%; 
    }}
    .user-bubble {{ 
        background: linear-gradient(135deg, #e91e63, #ff4081); 
        color: white; 
        padding: 10px 16px; 
        border-radius: 18px 18px 2px 18px; 
        box-shadow: 0 4px 12px rgba(233,30,99,0.25); 
        font-weight: 500; 
        word-break: break-word; 
    }}

    /* =========================================
       2. ระบบ RESPONSIVE (Mobile First Approach)
       อ้างอิง: Mobile (Base), Tablet (488px), Laptop (768px), Desktop (1824px)
       ========================================= */

    /* 📱 1. MOBILE (Base - ค่าเริ่มต้นสำหรับจอมือถือ) */
    .stApp .main .block-container {{
        padding: 15px 10px !important;
    }}
    div[data-testid="stBottomBlockContainer"] {{
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}
    div[data-testid="stChatInput"] {{
        width: 95% !important;
        max-width: 95% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-bottom: 15px !important;
        display: flex !important;
        justify-content: center !important;
    }}
    .stChatMessage {{ max-width: 95% !important; }}
    .user-bubble {{ max-width: 90% !important; }}


    /* 💊 2. TABLET (หน้าจอตั้งแต่ 488px ขึ้นไป) */
    @media (min-width: 488px) {{
        .stApp .main .block-container {{
            padding: 20px 15px !important;
        }}
        div[data-testid="stChatInput"] {{
            width: 90% !important;
            max-width: 90% !important;
        }}
        .stChatMessage {{ max-width: 90% !important; }}
        .user-bubble {{ max-width: 85% !important; }}
    }}

    /* 💻 3. LAPTOP (หน้าจอตั้งแต่ 768px ขึ้นไป) */
    @media (min-width: 768px) {{
        .stApp .main .block-container {{
            padding: 25px 25px !important;
        }}
        div[data-testid="stChatInput"] {{
            width: 80% !important;
            max-width: 750px !important; /* จัดกรอบไม่ให้กว้างเกินไปเวลาเปิดในคอม */
            padding-bottom: 25px !important;
        }}
        .stChatMessage {{ max-width: 85% !important; }}
        .user-bubble {{ max-width: 80% !important; }}
    }}

    /* 🖥️ 4. DESKTOP (หน้าจอ Ultrawide ตั้งแต่ 1824px ขึ้นไป) */
    @media (min-width: 1824px) {{
        .stApp .main .block-container {{
            padding: 40px !important;
        }}
        div[data-testid="stChatInput"] {{
            max-width: 1000px !important;
        }}
        .stChatMessage {{ max-width: 75% !important; }}
        .user-bubble {{ max-width: 70% !important; }}
    }}
    </style>"""