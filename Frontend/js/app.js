const uploadBtn = document.getElementById("upload-btn");
const fileInput = document.getElementById("pdf-upload");
const summaryOutput = document.getElementById("summary-output");
const loading = document.getElementById("loading");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");
const uploadedFileName = document.getElementById("uploaded-file-name");

let fileId = null;

uploadBtn.addEventListener("click", (e) => {
  e.preventDefault();
  e.stopPropagation();

  const file = fileInput.files[0];
  if (!file || file.type !== "application/pdf") {
    alert("Please select a valid PDF file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  loading.classList.remove("hidden");
  summaryOutput.innerText = "Generating summary...";

  fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData,
  })
    .then((res) => {
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      return res.json();
    })
    .then((data) => {
      fileId = data.id;
      console.log("✅ Upload Success:", fileId);
      uploadedFileName.innerText = `✅ File uploaded: ${file.name}`;
      fileInput.disabled = true;
      uploadBtn.disabled = true;
      chatInput.disabled = false;
      sendBtn.disabled = false;
      getSummary(fileId);
    })
    .catch((err) => {
      uploadedFileName.innerText = "";
      summaryOutput.innerText = "❌ Upload failed.";
      console.error("❌ Upload Error:", err);
    })
    .finally(() => {
      loading.classList.add("hidden");
    });
});

function getSummary(id) {
  fetch(`http://localhost:8000/summary/${id}`)
    .then((res) => {
      if (!res.ok) throw new Error(`Summary error: ${res.status}`);
      return res.json();
    })
    .then((data) => {
      summaryOutput.innerText = data.summary || "⚠️ No summary found.";
    })
    .catch((err) => {
      summaryOutput.innerText = "❌ Failed to load summary.";
      console.error("❌ Summary Fetch Error:", err);
    });
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const question = chatInput.value.trim();
  if (!question || !fileId) return;

  // Add user message
  chatBox.innerHTML += `
    <div class="text-gray-200 bg-gray-700 p-2 rounded-lg w-fit max-w-full">${question}</div>
  `;
  chatInput.value = "";

  fetch(`http://localhost:8000/chat/${fileId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: question }),
  })
    .then((res) => {
      if (!res.ok) throw new Error(`Chat error: ${res.status}`);
      return res.json();
    })
    .then((data) => {
      chatBox.innerHTML += `
        <div class="text-blue-200 bg-blue-900 p-2 rounded-lg w-fit max-w-full ml-auto">${data.response}</div>
      `;
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch((err) => {
      chatBox.innerHTML += `<div class="text-red-400">❌ Chat failed.</div>`;
      console.error("❌ Chat Error:", err);
    });
});
