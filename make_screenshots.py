import os
from playwright.sync_api import sync_playwright

os.makedirs('screenshots', exist_ok=True)
with open('screenshots/sample_resume.pdf', 'wb') as f:
    f.write(b'%PDF-1.4 sample test resume file')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
    
    # 1. Full page overview
    page.goto(url)
    page.wait_for_timeout(500)
    page.screenshot(path='screenshots/01_website_overview.png', full_page=True)
    page.screenshot(path='screenshots/01_website_header.png', clip={'x': 0, 'y': 0, 'width': 1280, 'height': 720})
    
    # 2. Bug Spoilers open
    page.click('summary.bug-summary')
    page.wait_for_timeout(300)
    page.locator('.bug-accordion-section').scroll_into_view_if_needed()
    page.locator('.bug-accordion-section').screenshot(path='screenshots/02_bug_spoilers.png')
    
    # 3. Retest: 9 digits rejected (PASS)
    page.reload()
    page.wait_for_timeout(300)
    page.fill('#fullName', 'นายทวีชัย นามฮาด')
    page.fill('#email', 'tester@example.com')
    page.fill('#phone', '081234567')
    page.fill('#dob', '2000-01-15')
    page.select_option('#experience', 'junior')
    page.select_option('#role', 'qa_tester')
    page.fill('#salary', '25000')
    page.set_input_files('#resumeFile', os.path.abspath('screenshots/sample_resume.pdf'))
    page.evaluate('document.getElementById("terms").checked = true')
    page.click('#submitBtn')
    page.wait_for_timeout(500)
    page.locator('#phone').scroll_into_view_if_needed()
    page.screenshot(path='screenshots/07_retest_phone_9digits_rejected.png', clip={'x': 200, 'y': 250, 'width': 880, 'height': 380})
    
    # 4. Retest: Terms unchecked rejected (PASS)
    page.reload()
    page.wait_for_timeout(300)
    page.fill('#fullName', 'นายทวีชัย นามฮาด')
    page.fill('#email', 'tester@example.com')
    page.fill('#phone', '0812345678')
    page.fill('#dob', '2000-01-15')
    page.select_option('#experience', 'junior')
    page.select_option('#role', 'qa_tester')
    page.fill('#salary', '25000')
    page.set_input_files('#resumeFile', os.path.abspath('screenshots/sample_resume.pdf'))
    page.evaluate('document.getElementById("terms").checked = false')
    page.click('#submitBtn')
    page.wait_for_timeout(500)
    page.locator('.checkbox-container').scroll_into_view_if_needed()
    page.screenshot(path='screenshots/09_retest_terms_unchecked_rejected.png', clip={'x': 200, 'y': 380, 'width': 880, 'height': 350})
    
    # 5. Retest: All valid + 10 digits + terms checked -> Success Modal (PASS)
    page.evaluate('document.getElementById("terms").checked = true')
    page.click('#submitBtn')
    page.wait_for_timeout(500)
    page.screenshot(path='screenshots/10_retest_all_valid_submit_success.png')

    # 6. DFG Diagram
    dfg_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin:0; padding:25px; font-family:"Segoe UI", Tahoma, sans-serif; background:#f8fafc; display:flex; justify-content:center; }
  .card { background:white; border:2px solid #e2e8f0; border-radius:16px; padding:24px 32px; box-shadow:0 8px 24px rgba(0,0,0,0.06); width:760px; }
  .title { font-size:20px; font-weight:700; color:#1e293b; margin-bottom:18px; text-align:center; }
  .node { background:#e0f2fe; border:2px solid #0284c7; border-radius:10px; padding:12px 18px; text-align:center; font-weight:600; color:#0369a1; margin:8px auto; width:480px; box-shadow:0 2px 6px rgba(2,132,199,0.15); }
  .node.def { background:#fef3c7; border-color:#d97706; color:#92400e; }
  .node.use { background:#e0e7ff; border-color:#4f46e5; color:#3730a3; }
  .node.branch-true { background:#dcfce7; border-color:#16a34a; color:#15803d; }
  .node.branch-false { background:#fee2e2; border-color:#dc2626; color:#991b1b; }
  .arrow { text-align:center; font-size:18px; color:#64748b; font-weight:bold; margin:2px 0; }
  .split { display:flex; justify-content:space-between; gap:16px; margin-top:6px; }
  .branch-box { flex:1; }
  .subtext { font-size:13px; font-weight:normal; opacity:0.85; margin-top:4px; }
</style>
</head>
<body>
<div class="card">
  <div class="title">📊 Data Flow Graph (DFG) - ตัวแปร phone (String)</div>
  <div class="node def">
    <strong>[D1] Define: input#phone</strong>
    <div class="subtext">ผู้ใช้กรอกค่าเบอร์โทรศัพท์ ➔ กำหนดค่าเริ่มต้นให้ตัวแปร phone</div>
  </div>
  <div class="arrow">⬇️ Def-Clear Path</div>
  <div class="node use">
    <strong>[U1] P-Use (Predicate): validatePhone()</strong>
    <div class="subtext">เงื่อนไข Regular Expression /^0[0-9]{9}$/ ตรวจสอบความยาว 10 หลัก</div>
  </div>
  <div class="arrow">⬇️ Condition Branching</div>
  <div class="split">
    <div class="branch-box">
      <div class="node branch-true">
        <strong>[U2] True Branch</strong>
        <div class="subtext">เบอร์ 10 หลักถูกต้อง (PASS) ➔ clearError() ➔ C-Use ใน Form Submit Modal</div>
      </div>
    </div>
    <div class="branch-box">
      <div class="node branch-false">
        <strong>[U3] False Branch</strong>
        <div class="subtext">เบอร์ 9 หลัก / ผิดรูปแบบ ➔ setError() แสดงข้อความแจ้งเตือน Error</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""
    page.set_content(dfg_html)
    page.wait_for_timeout(300)
    page.locator(".card").screenshot(path="screenshots/dfg_diagram.png")
    
    browser.close()
    print("ALL_SCREENSHOTS_DONE")
