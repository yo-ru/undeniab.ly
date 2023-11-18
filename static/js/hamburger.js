document.getElementById("hamburger-close").addEventListener("click", function() {
    document.getElementById("hamburger-menu").classList.add("hidden");
});

document.getElementById("hamburger-open").addEventListener("click", function() {
    document.getElementById("hamburger-menu").classList.remove("hidden");
});