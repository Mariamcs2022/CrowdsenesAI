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
let stream;

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        const video = document.getElementById("camera");
        video.srcObject = stream;
    } catch (err) {
        alert("تعذر فتح الكاميرا");
        console.log(err);
    }
}

function captureImage() {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("snapshot");

    if (!video || !video.srcObject) {
        alert("افتحي الكاميرا أولاً");
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(function(blob) {
        const file = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });

        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        document.getElementById("hiddenFileInput").files = dataTransfer.files;

        alert("تم التقاط الصورة بنجاح");
    }, "image/jpeg");
}
