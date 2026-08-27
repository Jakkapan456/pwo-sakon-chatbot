import os
import base64

def get_ui_css():
    img_path = "bg_lotus.jpg"
    img_base64 = ""
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

    return f"""<style>
    .stApp {{ background: linear-gradient(180deg, #fff5f8 0%, #ffeef3 100%); }}
    .stButton>button {{ width: 100%; border-radius: 20px; border: 1px solid #ff80ab; color: #e91e63; font-weight: bold; background: white; margin-bottom: 4px; }}
    
    [data-testid="stMainBlockContainer"], .main .block-container {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.86)), url("data:image/jpeg;base64,{img_base64}") !important;
        background-size: cover !important; background-position: center !important; border-radius: 20px; padding: 15px;
    }}
    
    .stChatMessage {{ border-radius: 18px !important; padding: 12px 16px !important; margin-bottom: 12px !important; background: linear-gradient(145deg, #fff 0%, #fff0f5 100%) !important; border: 1px solid rgba(248,187,208,0.8) !important; }}
    [data-testid="stChatMessageAvatarAssistant"] {{ background: white !important; border: 2px solid #ff80ab !important; border-radius: 50% !important; }}
    
    .user-container {{ display: flex; justify-content: flex-end; margin-bottom: 12px; width: 100%; }}
    .user-bubble {{ background: linear-gradient(135deg, #e91e63, #ff4081); color: white; padding: 10px 16px; border-radius: 18px 18px 2px 18px; max-width: 85%; font-weight: 500; }}

    /* ล้างการบังคับตำแหน่งออก ปล่อยให้ Streamlit จัดกึ่งกลางเองตามธรรมชาติ */
    div[data-testid="stChatInput"] {{
        width: 100% !important;
        margin: 0 auto !important;
    }}
    
    /* ปรับแค่กรอบใสๆ ด้านล่างให้เว้นขอบซ้าย-ขวาพอดี */
    div[data-testid="stBottomBlockContainer"] {{
        background: transparent !important;
        padding-left: 15px !important;
        padding-right: 15px !important;
    }}
    </style>"""