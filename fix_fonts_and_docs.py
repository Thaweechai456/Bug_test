import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def set_font_run(run, font_name="TH Sarabun PSK", size_pt=16, bold=None, color_rgb=None):
    if bold is not None:
        run.bold = bold
    if size_pt is not None:
        run.font.size = Pt(size_pt)
    if color_rgb is not None:
        run.font.color.rgb = color_rgb
        
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
        
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    
    lang = rPr.find(qn('w:lang'))
    if lang is None:
        lang = OxmlElement('w:lang')
        rPr.append(lang)
    lang.set(qn('w:val'), 'th-TH')
    lang.set(qn('w:bidi'), 'th-TH')
    lang.set(qn('w:eastAsia'), 'th-TH')

def enforce_doc_fonts(doc, default_font="TH Sarabun PSK"):
    for p in doc.paragraphs:
        for r in p.runs:
            set_font_run(r, font_name=default_font)
            
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        set_font_run(r, font_name=default_font)

def build_workshop1():
    doc = docx.Document('Workshop_Developer_to_Tester_completed.docx')
    
    # Table 0: Student info
    t0 = doc.tables[0]
    t0.rows[1].cells[0].text = ''
    r1 = t0.rows[1].cells[0].paragraphs[0].add_run('66040233102')
    set_font_run(r1, bold=True, size_pt=16)
    
    t0.rows[1].cells[1].text = ''
    r2 = t0.rows[1].cells[1].paragraphs[0].add_run('นายทวีชัย นามฮาด')
    set_font_run(r2, bold=True, size_pt=16)
    
    cell_img = t0.rows[1].cells[2]
    cell_img.text = ''
    p_img = cell_img.paragraphs[0]
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists('screenshots/01_website_header.png'):
        p_img.add_run().add_picture('screenshots/01_website_header.png', width=Inches(2.5))
        
    # P11 Overview
    for i, p in enumerate(doc.paragraphs):
        if '1.1 ' in p.text and ('นำภาพ' in p.text or 'ภาพหน้าเว็บ' in p.text):
            p.text = ''
            r = p.add_run('1.1 ภาพหน้าเว็บไซต์ของผู้พัฒนา (Developer Website Overview):')
            set_font_run(r, bold=True, size_pt=16)
            
            if i + 1 < len(doc.paragraphs):
                p_pic = doc.paragraphs[i+1]
                p_pic.text = ''
                p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if os.path.exists('screenshots/01_website_overview.png'):
                    p_pic.add_run().add_picture('screenshots/01_website_overview.png', width=Inches(5.5))
            break

    # Part 3 Evidence
    for i, p in enumerate(doc.paragraphs):
        if '3.5 ' in p.text:
            if i + 1 < len(doc.paragraphs):
                p_ev = doc.paragraphs[i+1]
                p_ev.text = ''
                r_ev = p_ev.add_run('Evidence: ตรวจสอบจากส่วน Bug Spoilers และผลการทดสอบกรอกเบอร์โทรศัพท์ 10 หลักบนหน้าเว็บพบข้อผิดพลาด:')
                set_font_run(r_ev, size_pt=16)
            break

    # Table 2 Bug report Evidence
    t2 = doc.tables[2]
    c_ev = t2.rows[5].cells[1]
    c_ev.text = ''
    r_t2 = c_ev.paragraphs[0].add_run('หลักฐานข้อผิดพลาด: Regex ใน script.js ตรวจสอบความยาว 9 หลัก แทนที่จะเป็น 10 หลัก ทำให้กรอกเบอร์มาตรฐานแล้วขึ้น Error\n')
    set_font_run(r_t2, size_pt=15)
    if os.path.exists('screenshots/03_bug1_phone_10digits_fail.png'):
        c_ev.paragraphs[0].add_run().add_picture('screenshots/03_bug1_phone_10digits_fail.png', width=Inches(4.5))

    # Part 5 Re-test
    for i, p in enumerate(doc.paragraphs):
        if '5.1 ' in p.text:
            p_ans1 = doc.paragraphs[i+1]
            p_ans1.text = ''
            r_ans1 = p_ans1.add_run('ทำการ Re-test ทดสอบกรณีเดิมซ้ำทั้งหมด 100% หลังแก้ไขโค้ดใน script.js ทั้งจุดเบอร์โทรศัพท์และจุดยอมรับเงื่อนไข')
            set_font_run(r_ans1, size_pt=16)
        elif '5.2 ' in p.text:
            p_ans2 = doc.paragraphs[i+1]
            p_ans2.text = ''
            r_ans2 = p_ans2.add_run('ผลการ Re-test: PASS ทั้งหมด (ทุกกรณีทำงานถูกต้องสมบูรณ์ตามเกณฑ์มาตรฐาน)')
            set_font_run(r_ans2, bold=True, size_pt=16, color_rgb=RGBColor(22, 101, 52))
        elif '5.3 ' in p.text:
            p_ans3 = doc.paragraphs[i+1]
            p_ans3.text = ''
            r_ans3 = p_ans3.add_run(
                'สรุปผลจากการทดสอบจริงหลังแก้ไขโค้ด:\n'
                '1) จุดที่ 1 (validatePhone): แก้ไข Regex เป็น /^0[0-9]{9}$/ ส่งผลให้เบอร์ 10 หลัก (0812345678) ผ่านการตรวจสอบ (PASS) และเมื่อกรอก 9 หลัก (081234567) ระบบจะแจ้งเตือนว่าผิด (PASS)\n'
                '2) จุดที่ 2 (validateTerms): ลบตัวแปร Bypass และตรวจ !termsCheckbox.checked จริง ส่งผลให้หากไม่ติ๊กถูก ระบบจะแสดงข้อความเตือนและไม่อนุญาตให้ Submit (PASS) และเมื่อติ๊กถูกจะลงทะเบียนสำเร็จ (PASS)'
            )
            set_font_run(r_ans3, size_pt=16)

    # Re-test screenshots heading & pictures order
    for i, p in enumerate(doc.paragraphs):
        if 'ภาพหลักฐานการ Re-test' in p.text:
            p.text = ''
            r_head = p.add_run('📷 ภาพหลักฐานการ Re-test หลังแก้ไขโค้ด (PASS ทุกเงื่อนไข):')
            set_font_run(r_head, bold=True, size_pt=16, color_rgb=RGBColor(30, 64, 175))
            break

    # Checklist items in Workshop 1
    checklist_items = [
        'ฉันอธิบายการทำงานของส่วนที่ได้รับมอบหมายได้',
        'ฉันสร้าง Test Data และ Expected Result ได้',
        'ฉันทดลองระบบจริงและบันทึก Actual Result',
        'ฉันพบ Bug และมีหลักฐาน',
        'ฉันเขียน Bug Report ให้ผู้อื่นทำตามได้',
        'ฉัน Re-test และสรุป PASS / FAIL ได้'
    ]
    
    chk_idx = 0
    for p in doc.paragraphs:
        txt = p.text.strip()
        if any(item[:10] in txt for item in checklist_items) or ('ฉัน' in txt and ('PASS' in txt or 'Re-test' in txt or 'Bug' in txt or 'Test Data' in txt or 'Actual' in txt or 'อธิบาย' in txt)):
            # only in checklist section
            if chk_idx < len(checklist_items):
                p.text = ''
                r_chk = p.add_run('[✓] ' + checklist_items[chk_idx])
                set_font_run(r_chk, bold=True, size_pt=16, color_rgb=RGBColor(20, 83, 45))
                chk_idx += 1

    enforce_doc_fonts(doc)
    doc.save('Workshop_Developer_to_Tester_completed.docx')
    print('Workshop 1 built!')

def build_workshop2():
    doc = docx.Document('Workshop2_DataFlowDetection_completed.docx')
    
    # Table 0: Student info
    t0 = doc.tables[0]
    t0.rows[1].cells[0].text = ''
    r1 = t0.rows[1].cells[0].paragraphs[0].add_run('66040233102')
    set_font_run(r1, bold=True, size_pt=16)
    
    t0.rows[1].cells[1].text = ''
    r2 = t0.rows[1].cells[1].paragraphs[0].add_run('นายทวีชัย นามฮาด')
    set_font_run(r2, bold=True, size_pt=16)
    
    cell_img = t0.rows[1].cells[2]
    cell_img.text = ''
    p_img = cell_img.paragraphs[0]
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists('screenshots/01_website_header.png'):
        p_img.add_run().add_picture('screenshots/01_website_header.png', width=Inches(2.5))
        
    # Table 2: Website Overview
    t2 = doc.tables[2]
    cell_t2 = t2.rows[0].cells[0]
    cell_t2.text = ''
    p_t2 = cell_t2.paragraphs[0]
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists('screenshots/01_website_overview.png'):
        p_t2.add_run().add_picture('screenshots/01_website_overview.png', width=Inches(5.5))
        
    # Mission 2 Step 1 & 5
    for p in doc.paragraphs:
        if 'หลักฐานจาก Bug Spoilers' in p.text or '[แทรก Screenshot ของ Source' in p.text:
            p.text = ''
            r_sp = p.add_run('หลักฐานจาก Bug Spoilers บนเว็บไซต์:')
            set_font_run(r_sp, bold=True, size_pt=16)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if os.path.exists('screenshots/02_bug_spoilers.png'):
                p.add_run('\n').add_picture('screenshots/02_bug_spoilers.png', width=Inches(5.0))
        elif 'โครงสร้าง Data Flow Graph' in p.text or '[แทรก DFG แบบลูกศร' in p.text:
            p.text = ''
            r_dfg = p.add_run('โครงสร้าง Data Flow Graph (DFG) ของตัวแปร phone:')
            set_font_run(r_dfg, bold=True, size_pt=16)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if os.path.exists('screenshots/dfg_diagram.png'):
                p.add_run('\n').add_picture('screenshots/dfg_diagram.png', width=Inches(5.2))

    # Table 13: Test Results Evidence
    t13 = doc.tables[13]
    c1 = t13.rows[1].cells[3]
    c1.text = ''
    if os.path.exists('screenshots/04_bug1_phone_9digits_pass_modal.png'):
        c1.paragraphs[0].add_run().add_picture('screenshots/04_bug1_phone_9digits_pass_modal.png', width=Inches(2.2))
    c2 = t13.rows[2].cells[3]
    c2.text = ''
    if os.path.exists('screenshots/03_bug1_phone_10digits_fail.png'):
        c2.paragraphs[0].add_run().add_picture('screenshots/03_bug1_phone_10digits_fail.png', width=Inches(2.2))
    t13.rows[3].cells[1].text = 'ระบบแสดง phone error แจ้งเตือนรูปแบบไม่ถูกต้อง'
    t13.rows[3].cells[2].text = 'PASS'
    c3 = t13.rows[3].cells[3]
    c3.text = ''
    if os.path.exists('screenshots/06_phone_invalid_letters_error.png'):
        c3.paragraphs[0].add_run().add_picture('screenshots/06_phone_invalid_letters_error.png', width=Inches(2.2))
    c4 = t13.rows[4].cells[3]
    c4.text = ''
    if os.path.exists('screenshots/02_bug_spoilers.png'):
        c4.paragraphs[0].add_run().add_picture('screenshots/02_bug_spoilers.png', width=Inches(2.2))

    # Table 15: Bug Report Evidence
    t15 = doc.tables[15]
    c15 = t15.rows[8].cells[1]
    c15.text = 'หลักฐานจาก Bug Spoilers และการทดสอบ:\n'
    if os.path.exists('screenshots/03_bug1_phone_10digits_fail.png'):
        c15.paragraphs[0].add_run().add_picture('screenshots/03_bug1_phone_10digits_fail.png', width=Inches(4.2))

    # Table 16: Re-test Results & Evidence
    t16 = doc.tables[16]
    t16.rows[1].cells[1].text = 'ใช้ Test Data เดิม: ทดสอบเบอร์ 9 หลัก, 10 หลัก และกรณีไม่ติ๊กยอมรับเงื่อนไข'
    t16.rows[1].cells[2].text = 'ใช้ Test Data เดิม: ทดสอบเบอร์ 9 หลัก, 10 หลัก และกรณีไม่ติ๊กยอมรับเงื่อนไข'
    
    t16.rows[2].cells[1].text = 'หลังแก้ไขโค้ด: เบอร์ 10 หลักผ่านการตรวจสอบ, เบอร์ 9 หลักขึ้น Error ถูกต้อง, และไม่ติ๊ก Terms จะส่งฟอร์มไม่ได้'
    t16.rows[2].cells[2].text = 'หลังแก้ไขโค้ด: เบอร์ 10 หลักผ่านการตรวจสอบ, เบอร์ 9 หลักขึ้น Error ถูกต้อง, และไม่ติ๊ก Terms จะส่งฟอร์มไม่ได้'
    
    t16.rows[3].cells[1].text = 'PASS (ผ่านการทดสอบ 100%)'
    t16.rows[3].cells[2].text = 'PASS (ผ่านการทดสอบ 100%)'
    
    c16_1 = t16.rows[4].cells[1]
    c16_1.text = 'ภาพหลักฐาน Re-test สำเร็จ:\n'
    if os.path.exists('screenshots/10_retest_all_valid_submit_success.png'):
        c16_1.paragraphs[0].add_run().add_picture('screenshots/10_retest_all_valid_submit_success.png', width=Inches(3.8))
        
    c16_2 = t16.rows[4].cells[2]
    c16_2.text = 'หลักฐานปฏิเสธเบอร์ 9 หลัก:\n'
    if os.path.exists('screenshots/07_retest_phone_9digits_rejected.png'):
        c16_2.paragraphs[0].add_run().add_picture('screenshots/07_retest_phone_9digits_rejected.png', width=Inches(3.8))

    # Fix Reflection Question 2 in Workshop 2
    for i, p in enumerate(doc.paragraphs):
        if '2. หลังทำกิจกรรมนี้ ฉันเห็นความสัมพันธ์' in p.text:
            if i + 1 < len(doc.paragraphs):
                p_ans2 = doc.paragraphs[i+1]
                p_ans2.text = ''
                r_ans2 = p_ans2.add_run(
                    'Source Code บอก Def/Use และ branch ส่วน Test Case เลือก Input เพื่อให้เดินผ่าน Path ที่ต้องการพิสูจน์\n'
                    'phone เป็นตัวอย่างที่ทำให้เห็นความเชื่อมโยงจาก input ไปสู่ regex และผล validation\n'
                    'ดังนั้น Test Case สามารถสร้างจากโครงสร้างของโปรแกรมได้'
                )
                set_font_run(r_ans2, size_pt=16)
            break

    # Fix Checklist in Workshop 2 (at the very bottom after "CHECKLIST ก่อนส่งงาน")
    ws2_checklist_items = [
        '[✓] เลือกตัวแปรจริงจาก Source Code',
        '[✓] ระบุ Def และ Use',
        '[✓] แยก P-use / C-use เมื่อพบ',
        '[✓] สร้าง Data Map / Mini DFG',
        '[✓] หา Def-Use Pair และ Path',
        '[✓] สร้าง Test Case จาก Path',
        '[✓] บันทึก Expected / Actual / PASS/FAIL',
        '[✓] แนบ Evidence',
        '[✓] ทำ Bug Report และ Re-test เมื่อพบ Defect'
    ]
    
    chk_found = False
    for i, p in enumerate(doc.paragraphs):
        if 'CHECKLIST ก่อนส่งงาน' in p.text or 'Checklist ก่อนส่งงาน' in p.text:
            chk_found = True
            if i + 1 < len(doc.paragraphs):
                p_chk = doc.paragraphs[i+1]
                p_chk.text = ''
                for item in ws2_checklist_items:
                    r = p_chk.add_run(item + '    ')
                    set_font_run(r, bold=True, size_pt=15, color_rgb=RGBColor(20, 83, 45))
            break

    enforce_doc_fonts(doc)
    doc.save('Workshop2_DataFlowDetection_completed.docx')
    print('Workshop 2 built!')

if __name__ == '__main__':
    build_workshop1()
    build_workshop2()
