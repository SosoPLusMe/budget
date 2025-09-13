let rows = true;

document.addEventListener("DOMContentLoaded", function() {
    const rowsBtn = document.getElementById("rowsBtn");
    const gridBtn = document.getElementById("gridBtn");
    const barcont = document.getElementById("barcont");
    const gridboxes = document.getElementsByClassName("gridboxes");

    rowsBtn.addEventListener("click", function() {
        rows = true;
        barcont.style.display = "block";

        for (let box of gridboxes) {
            box.style.display = "none";}
    });

    gridBtn.addEventListener("click", function() {
        rows = false;
        barcont.style.display = "none";
        for (let box of gridboxes) {
            box.style.display = "flex";}
    });
});