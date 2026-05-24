document.addEventListener("DOMContentLoaded", () => {

    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');

    const sections = {
        analysis: document.getElementById('analysis-section'),
        alerts: document.getElementById('alerts-section'),
        settings: document.getElementById('settings-section')
    };

    const menuItems = dropdownMenu 
        ? dropdownMenu.querySelectorAll('.dropdown-item[data-section]') 
        : [];


    /* فتح وإغلاق القائمة */
    if (hamburgerBtn && dropdownMenu) {
        hamburgerBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!hamburgerBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
                dropdownMenu.classList.remove('active');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                dropdownMenu.classList.remove('active');
            }
        });
    }


    /* تغيير الأقسام */
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            const sectionId = item.dataset.section;
            if (!sectionId) return;

            Object.values(sections).forEach(sec => {
                if (sec) sec.classList.remove('active-section');
            });

            if (sections[sectionId]) {
                sections[sectionId].classList.add('active-section');
            }

            menuItems.forEach(mi => mi.classList.remove('active-item'));
            item.classList.add('active-item');

            dropdownMenu.classList.remove('active');
        });
    });

    /* تفعيل افتراضي */
    if (sections.analysis) {
        sections.analysis.classList.add('active-section');
    }
});

// ==========================================
// منطق معالجة الصور، الكاميرا، والنافذة المنبثقة
// ==========================================

let stream;

// فتح نافذة الخيارات
function openSelectionModal() {
    document.getElementById('optionsModal').classList.add('modal-active');
}

// إغلاق نافذة الخيارات
function closeSelectionModal() {
    document.getElementById('optionsModal').classList.remove('modal-active');
}

// محاكاة الضغط على اختيار ملف من الجهاز
function triggerFileInput() {
    closeSelectionModal();
    document.getElementById('hiddenFileInput').click();
}

// عند اختيار ملف بنجاح من الجهاز
function handleFileSelected() {
    const fileInput = document.getElementById('hiddenFileInput');
    const fileStatus = document.getElementById('fileStatus');
    const submitBtn = document.getElementById('submitAnalysisBtn');

    if (fileInput.files && fileInput.files.length > 0) {
        fileStatus.innerText = ` تم اختيار ملف: ${fileInput.files[0].name}`;
        fileStatus.style.color = "#4caf50"; // لون أخضر للنجاح
        submitBtn.style.display = "block";   // إظهار زر التحليل
    }
}
