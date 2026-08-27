import os
import base64

def get_ui_css():
    """
    ฟังก์ชันส่งคืน CSS สำหรับตกแต่งสีพื้นหลัง ปุ่มกด และช่องแชทพร้อมรูปภาพบึงบัว
    """
    # 📌 แปลงรูปภาพ bg_lotus.jpg ให้เป็น Base64 อัตโนมัติ
    img_path = "bg_lotus.jpg"
    img_base64 = ""
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

    return f"""<style>
    /* พื้นหลังหน้าเว็บหลัก */
    .stApp {{ 
        background: linear-gradient(180deg, #fff5f8 0%, #ffeef3 100%); 
    }}
    
    /* ปุ่มกดทางด่วน */
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
    
    /* 📌 บังคับใส่พื้นหลังรูปบึงบัวแบบโปร่งแสงตรงพื้นที่แชทตรงกลาง */
    [data-testid="stMainBlockContainer"], .main .block-container {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.86)), url("data:image/jpeg;base64,{img_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-radius: 20px;
        padding: 25px;
    }}

    /* กล่องแชต AI */
    .stChatMessage {{ 
        border-radius: 18px !important; 
        padding: 12px 16px !important; 
        margin-bottom: 12px !important; 
        background: linear-gradient(145deg, #fff 0%, #fff0f5 100%) !important; 
        border: 1px solid rgba(248,187,208,0.8) !important; 
        box-shadow: 0 6px 16px rgba(233,30,99,0.06) !important; 
        max-width: 85% !important; 
    }}
    [data-testid="stChatMessageAvatarAssistant"] {{ 
        background: white !important; 
        border: 2px solid #ff80ab !important; 
        border-radius: 50% !important; 
    }}
    
    /* กล่องแชต User */
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
        max-width: 80%; 
        box-shadow: 0 4px 12px rgba(233,30,99,0.25); 
        font-weight: 500; 
        word-break: break-word; 
    }}
    </style>"""