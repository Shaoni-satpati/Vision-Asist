const canvas = document.getElementById("feed");
const ctx    = canvas.getContext("2d");
const status = document.getElementById("status");
const ws     = new WebSocket(`ws://${location.host}/stream`);

ws.binaryType = "arraybuffer";

ws.onopen  = () => {
    status.textContent = "Live";
    status.style.color = "#4CAF50";
};
ws.onclose = () => {
    status.textContent = "Disconnected";
    status.style.color = "#f44336";
};
ws.onerror = () => {
    status.textContent = "Connection Error";
    status.style.color = "#f44336";
};

ws.onmessage = (event) => {
  const blob = new Blob([event.data], { type: "image/jpeg" });
  const url  = URL.createObjectURL(blob);
  const img  = new Image();
  img.onload = () => {
    canvas.width  = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    URL.revokeObjectURL(url);
  };
  img.src = url;
};
