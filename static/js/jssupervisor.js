document.addEventListener("DOMContentLoaded", () => {

const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

const showAllBtn = document.getElementById("showAllBtn");
const pendingBtn = document.getElementById("pendingBtn");
const reportsBtn = document.getElementById("reportsBtn");

const totalCard = document.getElementById("totalCard");
const pendingCard = document.getElementById("pendingCard");

const rows = document.querySelectorAll(".data-row");

const applicationsSection = document.getElementById("applicationsSection");
const reportsSection = document.getElementById("reportsSection");

function closeSidebar(){
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
    menuBtn.style.display = "block";
}

function showApplications(){
    if (applicationsSection) applicationsSection.style.display = "block";
    if (reportsSection) reportsSection.style.display = "none";
}

function showReports(){
    if (applicationsSection) applicationsSection.style.display = "none";
    if (reportsSection) reportsSection.style.display = "block";
}

function showAllRows(){
    showApplications();
    rows.forEach(row => {
        row.style.display = "";
    });
}

function showPendingRows(){
    showApplications();
    rows.forEach(row => {
        const status = (row.dataset.status || "").trim();

        if(status === "In Progress"){
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

menuBtn.addEventListener("click", () => {
    sidebar.classList.add("active");
    overlay.classList.add("active");
    menuBtn.style.display = "none";
});

overlay.addEventListener("click", closeSidebar);

if(showAllBtn){
    showAllBtn.addEventListener("click", (e) => {
        e.preventDefault();
        showAllRows();
        closeSidebar();
    });
}

if(pendingBtn){
    pendingBtn.addEventListener("click", (e) => {
        e.preventDefault();
        showPendingRows();
        closeSidebar();
    });
}

if(totalCard){
    totalCard.addEventListener("click", () => {
        showAllRows();
    });
}

if(pendingCard){
    pendingCard.addEventListener("click", () => {
        showPendingRows();
    });
}

if(reportsBtn){
    reportsBtn.addEventListener("click", (e) => {
        e.preventDefault();
        showReports();
        closeSidebar();
    });
}

});