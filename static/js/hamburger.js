if (window.location.pathname.includes("/dashboard")) {
    document.getElementById("dashboard-hamburger").addEventListener("click", function() {
        sidebar = document.getElementById("dashboard-sidebar")
        hamburger = document.getElementById("dashboard-hamburger")
        sidebarClose = document.getElementById("sidebar-close")
        if (sidebar.classList.contains("-translate-x-full")) {
        sidebar.classList.remove("-translate-x-full");
        hamburger.classList.add("hidden");
        sidebarClose.classList.remove("hidden");
        } else {
        sidebar.classList.add("-translate-x-full");
        }
    });

    document.getElementById("sidebar-close").addEventListener("click", function() {
        sidebar = document.getElementById("dashboard-sidebar")
        hamburger = document.getElementById("dashboard-hamburger")
        sidebarClose = document.getElementById("sidebar-close")
        if (!sidebar.classList.contains("-translate-x-full")) {
        sidebar.classList.add("-translate-x-full");
        hamburger.classList.remove("hidden");
        sidebarClose.classList.add("hidden");
        }
    });
} else {
    document.getElementById("hamburger-close").addEventListener("click", function() {
        document.getElementById("hamburger-menu").classList.add("hidden");
    });

    document.getElementById("hamburger-open").addEventListener("click", function() {
        document.getElementById("hamburger-menu").classList.remove("hidden");
    });
}
