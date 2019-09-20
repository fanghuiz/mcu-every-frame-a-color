// Toggle dark mode
function dark_toggle() {
    var el1 = document.getElementById("dark-reader");
    var icon = document.getElementById("dark-reader-icon");
    if(el1.disabled) {
        el1.disabled = false;
        // icon.setAttribute("src", 'moon.svg');
        localStorage.setItem("darkreader", "enabled");
    } else {
        el1.disabled = true;
        // icon.setAttribute("src", 'sun.svg');
        localStorage.setItem("darkreader", "disabled");
    }
}
