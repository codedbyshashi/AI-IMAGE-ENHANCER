document.addEventListener("DOMContentLoaded", () => {

  const btnImg = document.getElementById("btnImg");
  const btnAudio = document.getElementById("btnAudio");

  btnImg.addEventListener("click", async () => {
    const file = document.getElementById("imageFile").files[0];
    const status = document.getElementById("imgStatus");

    if (!file) {
      status.innerText = "Please select an image.";
      return;
    }

    const resolution = document.getElementById("imgRes").value;
    const strength = document.getElementById("imgStrength").value;

    status.innerText = "Uploading & processing...";

    const form = new FormData();
    form.append("file", file);
    form.append("resolution", resolution);
    form.append("strength", strength);

    try {
      const resp = await fetch("/api/process-image", {
        method: "POST",
        body: form
      });

      const data = await resp.json();

      document.getElementById("imgOriginal").src = data.original_url;
      document.getElementById("imgProcessed").src = data.processed_url;

      const dl = document.getElementById("imgDownload");
      dl.href = data.processed_url;
      dl.style.display = "inline-block";

      status.innerText = "Done ✔";
    } catch (e) {
      status.innerText = "Error ❌";
      console.error(e);
    }
  });

});
