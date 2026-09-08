/**
 * Developer Registration System - Logic & Form Validation
 * =======================================================
 * 
 * 📌 สรุปตำแหน่ง BUG ทั้ง 2 จุด (สำหรับส่งงานและให้ Tester ทดสอบ):
 * -------------------------------------------------------
 * 🐛 BUG จุดที่ 1: Contact Number (เบอร์โทรศัพท์)
 *    - ไฟล์: script.js ฟังก์ชัน validatePhone()
 *    - พฤติกรรม: เบอร์โทรศัพท์มาตรฐานในไทยต้องมี 10 หลัก (เช่น 0812345678) 
 *      แต่โค้ด Regex ดันตรวจสอบเงื่อนไขเป็น 9 หลัก (^0[0-9]{8}$) 
 *      ทำให้เมื่อกรอก 10 หลัก ระบบจะแจ้งเตือนว่าผิด แต่ถ้ากรอก 9 หลัก ระบบกลับให้ผ่าน!
 * 
 * 🐛 BUG จุดที่ 2: Terms & Conditions Checkbox (ยอมรับเงื่อนไข)
 *    - ไฟล์: script.js ฟังก์ชัน validateTerms()
 *    - พฤติกรรม: ช่องกดยอมรับเงื่อนไขมีดอกจันสีแดง (*) บังคับเลือก 
 *      แต่ในโค้ด Validation มีการตั้งค่าข้ามการเช็ค (isTermsValid = true) 
 *      ทำให้แม้ผู้ใช้ "ไม่ได้ติ๊กเครื่องหมายถูก" (Unchecked) ระบบก็ยังยอมให้ Submit ผ่านฉลุย!
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('regForm');
    const resetBtn = document.getElementById('resetBtn');
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resumeFile');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    
    const editStudentBtn = document.getElementById('editStudentBtn');
    const studentDisplay = document.getElementById('studentDisplay');
    const successModal = document.getElementById('successModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modalSummary = document.getElementById('modalSummary');

    // ----------------------------------------------------------------
    // 0. ระบบสลับโหมด: โหมดแก้แล้ว (No Bug) vs โหมดจำลองบัคเดิม (Bug Mode)
    // ----------------------------------------------------------------
    let isBugMode = false; // ค่าเริ่มต้น: โหมดแก้ไขบัคแล้ว (Bug Free)

    const btnModeFixed = document.getElementById('btnModeFixed');
    const btnModeBug = document.getElementById('btnModeBug');
    const modeBadge = document.getElementById('modeBadge');
    const modeTitle = document.getElementById('modeTitle');
    const modeDescription = document.getElementById('modeDescription');
    const modeSwitchCard = document.getElementById('modeSwitchCard');

    function updateModeUI(bugActive) {
        isBugMode = bugActive;
        inputIds.forEach(id => clearError(id)); // ล้าง error เก่าเมื่อสลับโหมด

        if (isBugMode) {
            btnModeBug.classList.add('active');
            btnModeFixed.classList.remove('active');
            modeSwitchCard.classList.add('bug-active');
            modeBadge.className = 'mode-badge badge-bug';
            modeBadge.textContent = '🐛 BUG MODE (จำลองบัค)';
            modeTitle.textContent = 'โหมดปัจจุบัน: จำลองบัคเดิมสำหรับทดสอบ (Bug Mode)';
            modeDescription.textContent = '⚠️ เบอร์ 10 หลักจะ Error (รับแค่ 9 หลัก) และไม่ติ๊ก Terms ก็ยังกดส่งได้';
        } else {
            btnModeFixed.classList.add('active');
            btnModeBug.classList.remove('active');
            modeSwitchCard.classList.remove('bug-active');
            modeBadge.className = 'mode-badge badge-fixed';
            modeBadge.textContent = '✨ FIXED (สมบูรณ์)';
            modeTitle.textContent = 'โหมดปัจจุบัน: แก้ไขบัคแล้ว (Bug-Free Version)';
            modeDescription.textContent = '✅ ระบบรองรับเบอร์ 10 หลักถูกต้อง และบังคับติ๊กยอมรับเงื่อนไขก่อนส่ง';
        }
    }

    window.switchMode = updateModeUI;

    if (btnModeFixed && btnModeBug) {
        btnModeFixed.addEventListener('click', () => updateModeUI(false));
        btnModeBug.addEventListener('click', () => updateModeUI(true));
    }

    // ----------------------------------------------------------------
    // 0.1 จัดการชื่อและรหัสนักศึกษา (Student Profile)
    // ----------------------------------------------------------------
    const savedStudent = localStorage.getItem('student_info');
    if (savedStudent) {
        studentDisplay.textContent = savedStudent;
    }

    editStudentBtn.addEventListener('click', () => {
        const currentText = studentDisplay.textContent;
        const newInfo = prompt('กรุณากรอก [รหัสนักศึกษา : ชื่อ-นามสกุล (ภาษาไทย)]:', currentText);
        if (newInfo && newInfo.trim() !== '') {
            studentDisplay.textContent = newInfo.trim();
            localStorage.setItem('student_info', newInfo.trim());
        }
    });

    // ----------------------------------------------------------------
    // 1. จัดการการอัปโหลดไฟล์ (File Drag & Drop)
    // ----------------------------------------------------------------
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect();
        }
    });

    fileInput.addEventListener('change', handleFileSelect);

    function handleFileSelect() {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
            fileNameDisplay.textContent = `📄 ${file.name} (${fileSizeMB} MB)`;
            clearError('resumeFile');
        } else {
            fileNameDisplay.textContent = 'คลิกเพื่อเลือกไฟล์ หรือลากไฟล์มาวางที่นี่';
        }
    }

    // ----------------------------------------------------------------
    // 2. Helper Functions สำหรับแสดง/ลบ Error
    // ----------------------------------------------------------------
    function setError(fieldId, message) {
        const errorElement = document.getElementById(fieldId + 'Error');
        const inputElement = document.getElementById(fieldId);
        
        if (errorElement) {
            errorElement.textContent = message;
        }
        
        if (inputElement) {
            const group = inputElement.closest('.form-group') || inputElement.closest('.file-dropzone');
            if (group) group.classList.add('has-error');
        }
    }

    function clearError(fieldId) {
        const errorElement = document.getElementById(fieldId + 'Error');
        const inputElement = document.getElementById(fieldId);
        
        if (errorElement) {
            errorElement.textContent = '';
        }
        
        if (inputElement) {
            const group = inputElement.closest('.form-group') || inputElement.closest('.file-dropzone');
            if (group) group.classList.remove('has-error');
        }
    }

    // Realtime Error Clearing
    const inputIds = ['fullName', 'email', 'phone', 'dob', 'experience', 'role', 'salary', 'resumeFile', 'terms'];
    inputIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => clearError(id));
            el.addEventListener('change', () => clearError(id));
        }
    });

    // ----------------------------------------------------------------
    // 3. ฟังก์ชันการตรวจสอบข้อมูล (Validation Functions)
    // ----------------------------------------------------------------

    // 3.1 ตรวจสอบชื่อ-นามสกุล
    function validateFullName() {
        const value = document.getElementById('fullName').value.trim();
        const nameRegex = /^[a-zA-Z\u0E00-\u0E7F\s\.]+$/;

        if (!value) {
            setError('fullName', 'กรุณากรอกชื่อ-นามสกุล');
            return false;
        }
        if (value.length < 3) {
            setError('fullName', 'ชื่อ-นามสกุลต้องมีความยาวอย่างน้อย 3 ตัวอักษร');
            return false;
        }
        if (!nameRegex.test(value)) {
            setError('fullName', 'ชื่อ-นามสกุลต้องเป็นตัวอักษรภาษาไทยหรืออังกฤษเท่านั้น (ห้ามมีตัวเลข)');
            return false;
        }
        clearError('fullName');
        return true;
    }

    // 3.2 ตรวจสอบอีเมล
    function validateEmail() {
        const value = document.getElementById('email').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!value) {
            setError('email', 'กรุณากรอกอีเมล');
            return false;
        }
        if (!emailRegex.test(value)) {
            setError('email', 'รูปแบบอีเมลไม่ถูกต้อง (เช่น user@example.com)');
            return false;
        }
        clearError('email');
        return true;
    }

    // 3.3 ตรวจสอบเบอร์โทรศัพท์ (รองรับทั้งโหมด Fixed และโหมดจำลอง Bug)
    function validatePhone() {
        const value = document.getElementById('phone').value.trim();
        if (!value) {
            setError('phone', 'กรุณากรอกเบอร์โทรศัพท์');
            return false;
        }

        if (isBugMode) {
            // 🐛 โหมดจำลองบัคเดิม: ตรวจสอบแค่ 9 หลัก (^0[0-9]{8}$)
            const phoneRegexBug = /^0[0-9]{8}$/;
            if (!phoneRegexBug.test(value)) {
                setError('phone', 'เบอร์โทรศัพท์ต้องขึ้นต้นด้วย 0 และประกอบด้วยตัวเลข 10 หลัก (จำลอง Bug: โค้ดรับแค่ 9 หลัก)');
                return false;
            }
        } else {
            // ✅ โหมดแก้ไขแล้ว: ตรวจสอบ 10 หลัก (^0[0-9]{9}$) ถูกต้องตามมาตรฐานไทย
            const phoneRegexFixed = /^0[0-9]{9}$/;
            if (!phoneRegexFixed.test(value)) {
                setError('phone', 'เบอร์โทรศัพท์ต้องขึ้นต้นด้วย 0 และประกอบด้วยตัวเลข 10 หลัก (เช่น 0812345678)');
                return false;
            }
        }

        clearError('phone');
        return true;
    }

    // 3.4 ตรวจสอบวันเกิด
    function validateDob() {
        const value = document.getElementById('dob').value;
        if (!value) {
            setError('dob', 'กรุณาเลือกวันเดือนปีเกิด');
            return false;
        }
        const selectedDate = new Date(value);
        const today = new Date();
        if (selectedDate > today) {
            setError('dob', 'วันเดือนปีเกิดต้องไม่ใช่วันที่ในอนาคต');
            return false;
        }
        clearError('dob');
        return true;
    }

    // 3.5 ตรวจสอบประสบการณ์
    function validateExperience() {
        const value = document.getElementById('experience').value;
        if (!value) {
            setError('experience', 'กรุณาเลือกระดับประสบการณ์');
            return false;
        }
        clearError('experience');
        return true;
    }

    // 3.6 ตรวจสอบตำแหน่งงาน
    function validateRole() {
        const value = document.getElementById('role').value;
        if (!value) {
            setError('role', 'กรุณาเลือกตำแหน่งที่ต้องการสมัคร');
            return false;
        }
        clearError('role');
        return true;
    }

    // 3.7 ตรวจสอบเงินเดือน
    function validateSalary() {
        const value = document.getElementById('salary').value.trim();
        if (!value) {
            setError('salary', 'กรุณาระบุเงินเดือนที่คาดหวัง');
            return false;
        }
        if (Number(value) <= 0) {
            setError('salary', 'จำนวนเงินเดือนต้องมากกว่า 0');
            return false;
        }
        clearError('salary');
        return true;
    }

    // 3.8 ตรวจสอบไฟล์อัปโหลด
    function validateFile() {
        if (!fileInput.files || fileInput.files.length === 0) {
            setError('resumeFile', 'กรุณาอัปโหลดไฟล์เอกสาร Resume / ID');
            return false;
        }
        const file = fileInput.files[0];
        const validExtensions = ['pdf', 'jpg', 'jpeg', 'png'];
        const fileExt = file.name.split('.').pop().toLowerCase();
        
        if (!validExtensions.includes(fileExt)) {
            setError('resumeFile', 'อนุญาตเฉพาะไฟล์นามสกุล .pdf, .jpg, .png เท่านั้น');
            return false;
        }

        if (file.size > 10 * 1024 * 1024) {
            setError('resumeFile', 'ขนาดไฟล์ต้องไม่เกิน 10 MB');
            return false;
        }

        clearError('resumeFile');
        return true;
    }

    // 3.9 ตรวจสอบข้อตกลงและเงื่อนไข (รองรับทั้งโหมด Fixed และโหมดจำลอง Bug)
    function validateTerms() {
        const termsCheckbox = document.getElementById('terms');
        
        if (isBugMode) {
            // 🐛 โหมดจำลองบัคเดิม: Bypass การตรวจสอบเงื่อนไข (ไม่ติ๊กก็ผ่าน)
            clearError('terms');
            return true;
        } else {
            // ✅ โหมดแก้ไขแล้ว: บังคับต้องติ๊กยอมรับเงื่อนไข
            if (!termsCheckbox.checked) {
                setError('terms', 'คุณต้องยอมรับข้อกำหนดและเงื่อนไขก่อนลงทะเบียน');
                return false;
            }
            clearError('terms');
            return true;
        }
    }

    // ----------------------------------------------------------------
    // 4. Form Submit Handler
    // ----------------------------------------------------------------
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // ตรวจสอบความถูกต้องทุกฟิลด์
        const isNameValid = validateFullName();
        const isEmailValid = validateEmail();
        const isPhoneValid = validatePhone();
        const isDobValid = validateDob();
        const isExpValid = validateExperience();
        const isRoleValid = validateRole();
        const isSalaryValid = validateSalary();
        const isFileValid = validateFile();
        const isTermsValid = validateTerms();

        const isFormValid = isNameValid && isEmailValid && isPhoneValid && isDobValid &&
                            isExpValid && isRoleValid && isSalaryValid && isFileValid && isTermsValid;

        if (isFormValid) {
            // ดึงข้อมูลมาแสดงในสรุป Modal
            const fullName = document.getElementById('fullName').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const roleText = document.getElementById('role').options[document.getElementById('role').selectedIndex].text;
            const salary = Number(document.getElementById('salary').value).toLocaleString();
            const workplace = document.querySelector('input[name="workplace"]:checked')?.parentElement.textContent.trim();
            const contactMethod = document.querySelector('input[name="contactMethod"]:checked')?.parentElement.textContent.trim();

            modalSummary.innerHTML = `
                <div class="modal-summary-item">
                    <span>ชื่อผู้สมัคร:</span>
                    <span>${fullName}</span>
                </div>
                <div class="modal-summary-item">
                    <span>อีเมล:</span>
                    <span>${email}</span>
                </div>
                <div class="modal-summary-item">
                    <span>เบอร์โทร:</span>
                    <span>${phone}</span>
                </div>
                <div class="modal-summary-item">
                    <span>ตำแหน่ง:</span>
                    <span>${roleText}</span>
                </div>
                <div class="modal-summary-item">
                    <span>เงินเดือนที่คาดหวัง:</span>
                    <span>${salary} บาท</span>
                </div>
                <div class="modal-summary-item">
                    <span>รูปแบบการทำงาน:</span>
                    <span>${workplace}</span>
                </div>
                <div class="modal-summary-item">
                    <span>ช่องทางติดต่อ:</span>
                    <span>${contactMethod}</span>
                </div>
            `;

            successModal.classList.add('active');
        } else {
            // Scroll ไปยังจุดที่มี error จุดแรก
            const firstError = document.querySelector('.has-error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

    // ----------------------------------------------------------------
    // 5. Reset & Modal Closing Handlers
    // ----------------------------------------------------------------
    resetBtn.addEventListener('click', () => {
        inputIds.forEach(id => clearError(id));
        fileNameDisplay.textContent = 'คลิกเพื่อเลือกไฟล์ หรือลากไฟล์มาวางที่นี่';
    });

    closeModalBtn.addEventListener('click', () => {
        successModal.classList.remove('active');
    });
});
