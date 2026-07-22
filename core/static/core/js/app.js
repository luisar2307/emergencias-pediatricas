document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const menuButton = document.getElementById("menuButton");
    const sidebarClose = document.getElementById("sidebarClose");
   const currentDay = document.getElementById("currentDay");

    function openSidebar() {
        if (!sidebar || !sidebarOverlay) {
            return;
        }

        sidebar.classList.add("open");
        sidebarOverlay.classList.add("active");
        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
        if (!sidebar || !sidebarOverlay) {
            return;
        }

        sidebar.classList.remove("open");
        sidebarOverlay.classList.remove("active");
        document.body.style.overflow = "";
    }

    if (menuButton) {
        menuButton.addEventListener("click", openSidebar);
    }

    if (sidebarClose) {
        sidebarClose.addEventListener("click", closeSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", closeSidebar);
    }

    document.querySelectorAll(".navigation-link").forEach(function (link) {
        link.addEventListener("click", function () {
            if (window.innerWidth <= 980) {
                closeSidebar();
            }
        });
    });

    document.querySelectorAll(".alert-close-button").forEach(function (button) {
        button.addEventListener("click", function () {
            const alert = button.closest(".alert-message");

            if (!alert) {
                return;
            }

            alert.style.opacity = "0";
            alert.style.transform = "translateY(-8px)";

            window.setTimeout(function () {
                alert.remove();
            }, 250);
        });
    });

    if (currentDate) {
        const date = new Date();

        currentDate.textContent = new Intl.DateTimeFormat(
            "es-EC",
            {
                weekday: "short",
                day: "2-digit",
                month: "short",
                year: "numeric",
            }
        ).format(date);
    }

    window.addEventListener("resize", function () {
        if (window.innerWidth > 980) {
            closeSidebar();
        }
    });
});