document.addEventListener('DOMContentLoaded', () => {

    // ----- تحديث الوقت -----
    function updateClock() {
        const now = new Date();
        const timeElement = document.getElementById('current-time');

        if (timeElement) {
            timeElement.innerText = now.toLocaleString('ar-SA');
        }
    }

    updateClock();
    setInterval(updateClock, 1000);


    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');


    // الأقسام
    const sections = {
        all: document.getElementById('all-section'),
        recent: document.getElementById('recent-section')
    };


    const menuItems = dropdownMenu
        ? dropdownMenu.querySelectorAll('.dropdown-item[data-section]')
        : [];


    // فتح وإغلاق القائمة
    if (hamburgerBtn && dropdownMenu) {

        hamburgerBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (
                !hamburgerBtn.contains(e.target) &&
                !dropdownMenu.contains(e.target)
            ) {
                dropdownMenu.classList.remove('active');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (
                e.key === 'Escape' &&
                dropdownMenu.classList.contains('active')
            ) {
                dropdownMenu.classList.remove('active');
            }
        });
    }


    // ===== القسم الافتراضي =====
    Object.values(sections).forEach(section => {
        if (section) {
            section.classList.remove('active-section');
        }
    });

    if (sections.recent) {
        sections.recent.classList.add('active-section');
    }


    // تفعيل آخر تنبيه بالقائمة
    menuItems.forEach(item => {
        item.classList.remove('active-item');

        if (item.dataset.section === 'recent') {
            item.classList.add('active-item');
        }
    });


    // التنقل بين الأقسام
    menuItems.forEach(item => {

        item.addEventListener('click', (e) => {
            e.preventDefault();

            const sectionId = item.dataset.section;

            if (!sectionId) return;


            // إخفاء الجميع
            Object.values(sections).forEach(section => {
                if (section) {
                    section.classList.remove('active-section');
                }
            });


            // إظهار المطلوب
            if (sections[sectionId]) {
                sections[sectionId].classList.add('active-section');
            }


            // العنصر النشط
            menuItems.forEach(mi => {
                mi.classList.remove('active-item');
            });

            item.classList.add('active-item');


            // إغلاق القائمة
            if (dropdownMenu) {
                dropdownMenu.classList.remove('active');
            }

        });

    });

});


// ===== فتح الصورة =====
function openImageModal(src) {

    const modal = document.getElementById("imageModal");
    const modalImage = document.getElementById("modalImage");

    if (!modal || !modalImage) return;

    modal.style.display = "flex";
    modalImage.src = src;
}


// ===== إغلاق الصورة =====
function closeImageModal() {

    const modal = document.getElementById("imageModal");

    if (!modal) return;

    modal.style.display = "none";
}