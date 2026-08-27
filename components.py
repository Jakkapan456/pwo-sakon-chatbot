import streamlit as st
import os

# 📌 โครงสร้างข้อมูล 1: หมวดกรมต่างๆ (เปลี่ยนคำสั่งเป็น URL ของแต่ละเรื่อง)
DEPARTMENTS_DATA = {
    "กรมกิจการเด็กเเละเยาวชน ": [
        ("🔎ข้อมูล และจุดบริการภาครัฐ เกี่ยวกับเด็กเเละเยาวชน", "https://www.info.go.th/search?lat=13.7588311&lng=100.5405449&search=%E0%B9%80%E0%B8%94%E0%B9%87%E0%B8%81"),

        ("💻เด็กเเรกเกิด", "https://csgproject.dcy.go.th/login.do"),
        ("💻ระบบสารสนเทศเพื่อการคุ้มครองเด็ก", "https://cpis.dcy.go.th/officer-login"),
        ("💻ประเมินสถานพัฒนาเด็กปฐมวัยออนไลน์", "https://ecdis.dcy.go.th/"),
        ("💻ระบบตรวจสอบสถานะสิทธิโครงการเงินอุดหนุนเพื่อการเลี้ยงดูเด็กเเรกเกิด", "https://csgcheck.dcy.go.th/public/eq/popSubsidy.do?ms=1640160450538"),
        ("💻ระบบการจองจัดเลี้ยงอาหารในสถานสงเคราะห์", "https://mealforchild.dcy.go.th/"),
        ("💻ระบบบริการศูนย์อํานวยการรับเด็กเป็นบุตรบุญธรรมผ่านระบบดิจิทัล", "https://adoption.dcy.go.th/"),
        ("💻ระบบรับแจ้งเหตุกรมกิจการเด็กและเยาวชน", "https://cpis.dcy.go.th/login"),
        ("💻ระบบสวัสดิการเด็กและครอบครัว", "https://welfare.dcy.go.th/"),
        ("💻ระบบติดตามการใช้บริการ พม", "https://status.m-society.go.th/main"),
        ("💻แอปพลิเคชั่น", "https://www.dcy.go.th/content/1636520311278/1689689138655"),

        ("Dashboard รายงานข้อมูลของเด็กเเละเยาวชน", "https://dcy.go.th/"),
      


    ],
    "กรมกิจการผู้สูงอายุ ": [
        ("🔎ข้อมูล และจุดบริการภาครัฐ เกี่ยวกับผู้สูงอายุ", "https://www.info.go.th/search?tag_cate_id=94fc5592-b810-472f-a4b7-2cae35ee2f91"),
        ("🖥️ระบบขอเงินสนับสนุนโครงการ", "https://project.dop.go.th/Account/Login"),
        ("🖥️ระบบให้บริการกู้ยืมเงินทุนประกอบการอาชีพ", "https://odf.dop.go.th/login"),
        ("🖥️หลักสูตรออนไลน์การดูเเลผู้สูงอายุขั้นเบื้องต้นจํานวน 18 ชั่วโมง", "https://thaielderlycare.dop.go.th/"),
        ("🖥️ร้องเรียนการทุจริตเเละประพฤติมิชอบ", "https://www.dop.go.th/th/formcomplaint"),

        ("📲การให้บริการสงเคราะห์ผู้สูงอายุในภาวะยากลําบาก", "https://www.dop.go.th/thai/service_information/1/15"),
        ("📲การสนับสนุนการจัดการศพผู้สูงอายุตามประเพณี", "https://www.dop.go.th/thai/service_information/1/15"),
        ("📲การปรับสภาพเเวดล้อมเเละสิ่งอํานวยควาสะดวก", "https://www.dop.go.th/thai/service_information/1/15"),
        ("📲การขอเข้ารับบริการใน ศพส.", "https://www.dop.go.th/thai/service_information/1/15" ),
        ("Facebook", "https://www.facebook.com/olderfund"),
        ("YouTube", "https://www.youtube.com/channel/UCNECvcwNQNyuf21jRdRY-TQ"),
        ("Instagram", "https://www.instagram.com/olderfund?utm_source=qr"),
        ("Line", "https://lin.ee/mGAwGbl"),
        
    ],
    "กรมกิจการสตรีและสถาบันครอบครัว ": [
        ("🌐ปักหมุด หยุดเหตุ", "https://www.dwf.go.th/contents/36953"),
        ("🌐เเจ้งเหตุความรุนเเรงในครอบครัว", "https://eservice1300.m-society.go.th/"),
        ("🌐สมัครฝึกอบรมอาชีพ", "https://dlc.dwf.go.th/prd/dwf-academy/home"),
        ("🌐ปรึกษาปัญหาครอบครัว", "https://xn--42ca5dfr6ac6azcd1c9c9f0e.com/startup/list"),
        ("🌐สำนักงานคณะกรรมการป้องกันและปราบปรามการทุจริตเเห่งชาต", "https://www.nacc.go.th/allcomplaint?csrt=12374973521377089763"),
        ("🌐สำนักงานคณะกรรมการป้องกันและปราบปรามการทุจริตในภาครัฐ", "https://anonymous.pacc.go.th/"),
        ("📝คําร้องคณะกรรมการวินิจฉัยการเลือกปฎิบัติโดยไม่เป็นธรรมระหว่างเพศ)", "https://www.dwf.go.th/uploads/Downloads/e5bf5545-b924-4937-ba6f-2aa28eee392c%E0%B8%A7%E0%B8%A5%E0%B8%9E01%20%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B8%84%E0%B8%B3%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%87.pdf"),
        ("📝เเบบฟอร์มขอใช้ห้องหรืออุปกรณ์ของกลุ่มเทคโนโลยีสารสนเทศ (กทส.)", "https://drive.google.com/drive/folders/1dVooBq919qj-SYYsQjHpUylkyHFmSyhG"),
        ("💬ติดตามสถานะร้องทุกข์ ร้องเรียน", "https://complain.dwf.go.th/public/checkStatusComplaint.do"),
        ("💬ข้อคิดเห็นเเละข้อเสนอเเนะ บริการของสค.", "https://complain.dwf.go.th/public/complaint.do"),
        ("💬ร้องเรียนการฌาปนกิจสงเคราะห์", "https://cmt.dwf.go.th/portal/complaint.php"),
        ("💬ร้องเรียนการให้บริการกองทุนสงเสริมความเท่าเทียมระหว่างเพศ", "https://gepf.dwf.go.th/home/index"),
        ("💬ร้องทุกข์ ร้องเรียนทั่วไป", "https://complain.dwf.go.th/public/complaint.do"),
        ("🚨ติดตามสถานะ", "https://complain.dwf.go.th/public/checkStatusComplaint.do"),
        ("🚨ร้องเรียนการทุจริต", "https://complain.dwf.go.th/public/fraudComplaint.do"),
        ("🚨มาตรการและแนวทางการจัดการเรื่องร้องเรียนการทุจริตและประพฤติมิชอบ", "https://dwf.go.th/contents/72191"),
        ("📞ติดต่อเรา กรมกิจการสตรีและสถาบันครอบครัว (สค.)", "https://www.dwf.go.th/contents/130"),



    ],
    "กรมส่งเสริมเเละพัฒนาคุณภาพชีวิตคนพิการ": [
        ("🪪บัตรประจําตัวคนพิการ", "https://dep.go.th/th/rights-welfares-services/disabled-person-id-card"),
        ("💰กองทุนส่งเสริมเเละพัฒนาคุณภาพชีวิตคนพิการ", "https://dep.go.th/th/rights-welfares-services/disabled-person-fund"),
        ("🤝การจัดบริการผู้ช่วยคนพิการ", "https://dep.go.th/th/rights-welfares-services/disabled-person-assistant-services"),
        ("🏠การรับคนพิการเข้าสถานคุ้มครอง", "https://dep.go.th/th/rights-welfares-services/home-for-disabled-person"),
        ("🦾อาชีวบําบัด", "https://dep.go.th/th/rights-welfares-services/occupational-therapy"),
        ("🧏ล่ามภาษามือ", "https://dep.go.th/th/rights-welfares-services/sign-language-interpreter"),
        ("🦽เครื่องช่วยความพิการ", "https://dep.go.th/th/rights-welfares-services/disability-aids"),
        ("💵เงินสงเคราะห์", "https://dep.go.th/th/rights-welfares-services/disability-allowance"),
        ("❓คําถามที่พบบ่อย", "https://dep.go.th/th/rights-welfares-services/faq"),
        ("💼การกู้ยืมเงินเพื่อการประกอบอาชีพ", "https://dep.go.th/th/rights-welfares-services/borrow-money"),
        ("🧑‍💼จ้างงานคนพิการ", "https://dep.go.th/th/rights-welfares-services/%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📊1.ผลการสำรวจความพึงพอใจการให้บริการ", "https://dep.go.th/th/rights-welfares-services/1-%E0%B8%9C%E0%B8%A5%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%AA%E0%B8%B3%E0%B8%A3%E0%B8%A7%E0%B8%88%E0%B8%84%E0%B8%A7%E0%B8%B2%E0%B8%A1%E0%B8%9E%E0%B8%B6%E0%B8%87%E0%B8%9E%E0%B8%AD%E0%B9%83%E0%B8%88%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📈2.ข้อมูลเชิงสถิติการให้บริการ", "https://dep.go.th/th/rights-welfares-services/2-%E0%B8%82%E0%B9%89%E0%B8%AD%E0%B8%A1%E0%B8%B9%E0%B8%A5%E0%B9%80%E0%B8%8A%E0%B8%B4%E0%B8%87%E0%B8%AA%E0%B8%96%E0%B8%B4%E0%B8%95%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3-3"),
        ("📉3.สถิติการให้ความช่วยเหลือเงินสงเคราะห์และฟื้นฟูสมรรถภาพคนพิการ", "https://dep.go.th/th/rights-welfares-services/3-%E0%B8%AA%E0%B8%96%E0%B8%B4%E0%B8%95%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B8%84%E0%B8%A7%E0%B8%B2%E0%B8%A1%E0%B8%8A%E0%B9%88%E0%B8%A7%E0%B8%A2%E0%B9%80%E0%B8%AB%E0%B8%A5%E0%B8%B7%E0%B8%AD%E0%B9%80%E0%B8%87%E0%B8%B4%E0%B8%99%E0%B8%AA%E0%B8%87%E0%B9%80%E0%B8%84%E0%B8%A3%E0%B8%B2%E0%B8%B0%E0%B8%AB%E0%B9%8C%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B8%9F%E0%B8%B7%E0%B9%89%E0%B8%99%E0%B8%9F%E0%B8%B9%E0%B8%AA%E0%B8%A1%E0%B8%A3%E0%B8%A3%E0%B8%96%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📖คู่มือการจัดบริการล่ามภาษามือ", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%88%E0%B8%B1%E0%B8%94%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%A5%E0%B9%88%E0%B8%B2%E0%B8%A1%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B8%A1%E0%B8%B7%E0%B8%AD"),
        ("♿สิ่งอำนวยความสะดวกสำหรับคนพิการ", "https://dep.go.th/th/rights-welfares-services/conveniences-for-disabled-person"),
        ("🏢ศูนย์บริการคนพิการทั่วไป", "https://dep.go.th/th/rights-welfares-services/general-servicecenter"),
        ("🦿กายอุปกรณ์สำหรับคนพิการ", "https://dep.go.th/th/rights-welfares-services/devices-pwd"),
        ("🏡ปรับสภาพแวดล้อมที่อยู่อาศัยสำหรับคนพิการ", "https://dep.go.th/th/rights-welfares-services/environment-pwd"),
        ("📘คู่มือคนพิการ", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📂ทำเนียบผลิตภัณฑ์", "https://dep.go.th/th/rights-welfares-services/article-for-job/%E0%B8%97%E0%B8%B3%E0%B9%80%E0%B8%99%E0%B8%B5%E0%B8%A2%E0%B8%9A%E0%B8%9C%E0%B8%A5%E0%B8%B4%E0%B8%95%E0%B8%A0%E0%B8%B1%E0%B8%93%E0%B8%91%E0%B9%8C"),
        ("🗂️ทำเนียบผลิตภัณฑ์คนพิการ", "https://dep.go.th/th/rights-welfares-services/article-for-job/%E0%B8%97%E0%B8%B3%E0%B9%80%E0%B8%99%E0%B8%B5%E0%B8%A2%E0%B8%9A%E0%B8%9C%E0%B8%A5%E0%B8%B4%E0%B8%95%E0%B8%A0%E0%B8%B1%E0%B8%93%E0%B8%91%E0%B9%8C%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📑คู่มือการปฏิบัติตามกฎหมายการจ้างงานคนพิการในหน่วยงานของรัฐ ตามพระราชบัญญัติส่งเสริมและพัฒนาคุณภาพชีวิตคนพิการ พ.ศ. 2550 และที่แก้ไขเพิ่มเติม", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B8%95%E0%B8%B2%E0%B8%A1%E0%B8%81%E0%B8%8E%E0%B8%AB%E0%B8%A1%E0%B8%B2%E0%B8%A2%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%99%E0%B8%AB%E0%B8%99%E0%B9%88%E0%B8%A7%E0%B8%A2%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%A3%E0%B8%B1%E0%B8%90-%E0%B8%95%E0%B8%B2%E0%B8%A1%E0%B8%9E%E0%B8%A3%E0%B8%B0%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%9A%E0%B8%B1%E0%B8%8D%E0%B8%8D%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B8%AA%E0%B9%88%E0%B8%87%E0%B9%80%E0%B8%AA%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B8%9E%E0%B8%B1%E0%B8%92%E0%B8%99%E0%B8%B2%E0%B8%84%E0%B8%B8%E0%B8%93%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B8%8A%E0%B8%B5%E0%B8%A7%E0%B8%B4%E0%B8%95%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3-%E0%B8%9E-%E0%B8%A8-2550-%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%81%E0%B8%81%E0%B9%89%E0%B9%84%E0%B8%82%E0%B9%80%E0%B8%9E%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B9%80%E0%B8%95%E0%B8%B4%E0%B8%A1"),
        ("📋คู่มือการปฏิบัติตามกฎหมายการจ้างงานคนพิการสำหรับนายจ้างหรือเจ้าของสถานประกอบการ ตามพระราชบัญญัติส่งเสริมและพัฒนาคุณภาพชีวิตคนพิการ พ.ศ. 2550 และที่แก้ไขเพิ่มเติม", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B8%95%E0%B8%B2%E0%B8%A1%E0%B8%81%E0%B8%8E%E0%B8%AB%E0%B8%A1%E0%B8%B2%E0%B8%A2%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%99%E0%B8%B2%E0%B8%A2%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B8%AB%E0%B8%A3%E0%B8%B7%E0%B8%AD%E0%B9%80%E0%B8%88%E0%B9%89%E0%B8%B2%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%AA%E0%B8%96%E0%B8%B2%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%AD%E0%B8%9A%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📝คู่มือหรือแนวทางการขอรับบริการสำหรับผู้รับบริการหรือผู้มาติดต่อ (สำหรับประชาชน)", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%82%E0%B8%AD%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📑คู่มือการปรับสภาพแวดล้อมที่อยู่อาศัยสำหรับคนพิการ (ฉบับปรับปรุง)", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B9%83%E0%B8%99%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%AA%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B9%81%E0%B8%A7%E0%B8%94%E0%B8%A5%E0%B9%89%E0%B8%AD%E0%B8%A1%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B8%AD%E0%B8%A2%E0%B8%B9%E0%B9%88%E0%B8%AD%E0%B8%B2%E0%B8%A8%E0%B8%B1%E0%B8%A2%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📑คู่มือการจัดสิ่งอำนวยความสะดวกสำหรับคนพิการ", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%88%E0%B8%B1%E0%B8%94%E0%B8%AA%E0%B8%B4%E0%B9%88%E0%B8%87%E0%B8%AD%E0%B8%B3%E0%B8%99%E0%B8%A7%E0%B8%A2%E0%B8%84%E0%B8%A7%E0%B8%B2%E0%B8%A1%E0%B8%AA%E0%B8%B0%E0%B8%94%E0%B8%A7%E0%B8%81%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),
        ("📖คู่มือการปฏิบัติงานให้บริการประชาชน", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B8%8F%E0%B8%B4%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%8A%E0%B8%B2%E0%B8%8A%E0%B8%99"),
        ("🗂️คู่มือการดำเนินงานศูนย์บริการคนพิการ", "https://dep.go.th/th/rights-welfares-services/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3/%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%94%E0%B8%B3%E0%B9%80%E0%B8%99%E0%B8%B4%E0%B8%99%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%A8%E0%B8%B9%E0%B8%99%E0%B8%A2%E0%B9%8C%E0%B8%9A%E0%B8%A3%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%84%E0%B8%99%E0%B8%9E%E0%B8%B4%E0%B8%81%E0%B8%B2%E0%B8%A3"),


        
    ],
    "กรมพัฒนาสังคมและสวัสดิการ ": [
        ("💵การขอรับเงินอุดหนุนเงินสงเคราะห์", "https://service.dsdw.go.th/Service/01"),
        ("🛡️การขอรับการคุ้มครอง", "https://service.dsdw.go.th/Service/02"),
        ("👥หมวดอาสาสมัครพัฒนาสังคมและความมั่นคงของมนุษย์ (อพม.)", "https://service.dsdw.go.th/Service/03"),
        ("📜การออกหนังสือรับรองให้แก่อาสาสมัครชาวต่างประเทศ", "https://service.dsdw.go.th/Service/09"),
        ("🏡การขอรับบริการ/ต่อสัญญาตามพระราชบัญญัติจัดที่ดินเพื่อการครองชีพ พ.ศ.2511", "https://service.dsdw.go.th/Service/04"),
        ("🎤การขอจดแจ้งเป็นผู้แสดงความสามารถ", "https://service.dsdw.go.th/Service/05"),
        ("🏢การรับรององค์กร/รับรองมาตรฐานการปฏิบัติงาน", "https://service.dsdw.go.th/Service/06"),
        ("💰การขอรับเงินสำหรับองค์กร", "https://service.dsdw.go.th/Service/07"),
        ("🌐การบริการด้านอื่น ๆ", "https://service.dsdw.go.th/Service/08"),
        ("📹วิดีโอคู่มือการใช้งานบริการต่างๆของกรมพัฒนาสังคมเเละสวัสดิการ", "https://service.dsdw.go.th/Service/Tutorial"),
       


    ],
    "สํานักงานปลัดกระทรวงการพัฒนาสังคมฯ ": [
        ("🚨ต่อต้านการค้ามนุษย์", "https://e-aht.com/"),
        ("🏘️สถาบันพัฒนาองค์กรชุมชน", "https://web.codi.or.th/e-service/"),
     

    ]
}

# 📌 โครงสร้างข้อมูล 2: หมวดกฎหมาย (ปุ่มให้ AI ตอบ)
LAW_QUESTIONS = [
    ("หมวดกฎหมายเด็กและเยาวชน", "ขณะนี้ผู้ใช้เลือก [หมวดกฎหมายเด็กและเยาวชน] กรุณากล่าวต้อนรับสั้นๆ บอกภาพรวมของหมวดนี้ใน 2-3 บรรทัด และบอกว่าผู้ใช้สามารถพิมพ์สอบถามประเด็นกฎหมายหรือสิทธิเด็กที่สงสัยเข้ามาได้เลย"),
    ("หมวดกฎหมายสตรีและสถาบันครอบครัว", "ขณะนี้ผู้ใช้เลือก [หมวดกฎหมายสตรีและสถาบันครอบครัว] กรุณากล่าวต้อนรับสั้นๆ บอกภาพรวมของหมวดนี้ใน 2-3 บรรทัด และบอกว่าผู้ใช้สามารถพิมพ์สอบถามประเด็นกฎหมายที่สงสัยเข้ามาได้เลย"),
    ("หมวดกฎหมายคนพิการ", "ขณะนี้ผู้ใช้เลือก [หมวดกฎหมายคนพิการ] กรุณากล่าวต้อนรับสั้นๆ บอกภาพรวมของหมวดนี้ใน 2-3 บรรทัด และบอกว่าผู้ใช้สามารถพิมพ์สอบถามประเด็นสิทธิคนพิการตามกฎหมายเข้ามาได้เลย"),
    ("หมวดกฎหมายผู้สูงอายุ", "ขณะนี้ผู้ใช้เลือก [หมวดกฎหมายผู้สูงอายุ] กรุณากล่าวต้อนรับสั้นๆ บอกภาพรวมของหมวดนี้ใน 2-3 บรรทัด และบอกว่าผู้ใช้สามารถพิมพ์สอบถามประเด็นสิทธิหรือกฎหมายผู้สูงอายุเข้ามาได้เลย"),
]

def render_sidebar():
    """แถบเมนูด้านซ้าย (Sidebar)"""
    with st.sidebar:
        col1, col2 = st.columns([1, 4])
        with col1:
            try:
                st.image("logo_new.png", width=34)
            except Exception:
                pass
        with col2:
            st.markdown("<div style='font-size: 17px; font-weight: bold; color: #333333; margin-top: 4px;'>AI พมจ.สกลนคร</div>", unsafe_allow_html=True)
            
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

        if st.button("➕ เริ่มการสนทนาใหม่", key="side_new_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("---")
        
        # 📌 สร้างลิ้นชักที่ 1: ข้อมูลสิทธิสวัสดิการทั่วไป (ข้างในเป็น Popover -> ลิงก์)
        with st.expander(" ข้อมูลสิทธิสวัสดิการทั่วไป", expanded=False):
            for dept_name, sub_items in DEPARTMENTS_DATA.items():
                with st.popover(dept_name, use_container_width=True):
                    # ใช้ st.link_button เพื่อให้เปิดหน้าเว็บได้
                    for sub_label, link_url in sub_items:
                        st.link_button(sub_label, link_url, use_container_width=True)

        # 📌 สร้างลิ้นชักที่ 2: ดาวน์โหลดแบบฟอร์มเอกสาร 
        with st.expander(" แบบฟอร์มเอกสารสิทธิสวัสดิการต่างๆ (คลิกเพื่อดาวน์โหลด)", expanded=False):
            form_path = "forms"
            if os.path.exists(form_path):
                pdf_files = [f for f in os.listdir(form_path) if f.endswith(".pdf")]
                if pdf_files:
                    for file_name in pdf_files:
                        file_full_path = os.path.join(form_path, file_name)
                        with open(file_full_path, "rb") as f:
                            btn_label = f"📄 {file_name.replace('.pdf', '')}"
                            st.download_button(
                                label=btn_label,
                                data=f,
                                file_name=file_name,
                                mime="application/pdf",
                                key=f"dl_{file_name}",
                                use_container_width=True
                            )
            
        # 📌 สร้างลิ้นชักที่ 3: คำถามเกี่ยวกับ พ.ร.บ กฎหมาย พม. 
        with st.expander(" คำถามเกี่ยวกับ พ.ร.บ กฎหมาย พม.", expanded=False):
            for idx, (label, prompt_text) in enumerate(LAW_QUESTIONS):
                if st.button(label, key=f"law_btn_{idx}", use_container_width=True):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": label,
                        "prompt": prompt_text
                    })
                    st.rerun()

def render_header():
    """แสดงส่วนหัวและโลโก้หน้าแรก"""
    _, col2, _ = st.columns([2, 1, 2])
    with col2:
        try:
            st.image("logo_new.png", width=100)
        except Exception:
            pass

    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <div class='main-title'>AI ผู้ช่วยสิทธิสวัสดิการ</div>
            <div class='sub-title'>สำนักงานพัฒนาสังคมและความมั่นคงของมนุษย์จังหวัดสกลนคร </div>
        </div>
        <hr>
    """, unsafe_allow_html=True)

def render_quick_buttons():
    """แสดงปุ่มคำถามที่พบบ่อยกลางหน้าแรก"""
    st.markdown("<div class='button-header'>💡 หมวดหมู่หน่วยงานและกฎหมาย (กดเพื่อเลือกหัวข้อย่อย):</div>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    idx = 0
    
    # 1. นำหมวดกรมต่างๆ (Popover -> ลิงก์) มาแสดง
    for dept_name, sub_items in DEPARTMENTS_DATA.items():
        with cols[idx % 2]:
            with st.popover(dept_name, use_container_width=True):
                # ใช้ st.link_button เพื่อให้เปิดหน้าเว็บได้
                for sub_label, link_url in sub_items:
                    st.link_button(sub_label, link_url, use_container_width=True)
        idx += 1

    # 2. นำหมวดกฎหมาย (ปุ่มปกติ) มาแสดงต่อท้าย
    for label, prompt_text in LAW_QUESTIONS:
        with cols[idx % 2]:
            if st.button(label, key=f"main_law_{idx}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": label,
                    "prompt": prompt_text
                })
                st.rerun()
        idx += 1

    st.markdown("""
        <div style='text-align: center; color: #666666; font-size: 14px; margin-top: 15px; margin-bottom: 5px;'>
            💬 สามารถพิมพ์ถามนอกเหนือจากคำถามที่พบบ่อยได้ที่ช่องพิมพ์ด้านล่าง
        </div>
        <hr>
    """, unsafe_allow_html=True)