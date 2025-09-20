let rows = true;

document.addEventListener("DOMContentLoaded", function() {
    const rowsBtn = document.getElementById("rowsBtn");
    const gridBtn = document.getElementById("gridBtn");
    const barcont = document.getElementById("barcont");
    const gridboxes = document.getElementsByClassName("gridboxes");

    rowsBtn.addEventListener("click", function() {
        rows = true;
        barcont.style.display = "table";


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


window.onload = function () {
  google.accounts.id.initialize({
    client_id: "856146957797-l1gnuoe0eesg6v1aldtd351aueuf659e.apps.googleusercontent.com",
    callback: handleCredentialResponse
  });

  google.accounts.id.renderButton(
    document.getElementById("g_id_signin"),
    { theme: "outline", size: "large" }
  );
};

function handleCredentialResponse(response) {
  fetch("/google-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: response.credential })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      window.location.href = "/";
    } else {
      alert("Google login failed");
    }
  });
}
