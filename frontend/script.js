// ==== BASE URL ====
const BASE_URL = "http://127.0.0.1:8000";
const API_USERS = `${BASE_URL}/users`;
const API_FILES = `${BASE_URL}/files`;
const API_AI = `${BASE_URL}/ai`;

// ============ SIGNUP ============
const signupBtn = document.getElementById("signupBtn");
if (signupBtn) {
  signupBtn.addEventListener("click", async () => {
    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    const res = await fetch(`${API_USERS}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    if (res.ok) {
      alert("✅ Signup successful! Please login now.");
      window.location.href = "index.html";
    } else {
      const err = await res.json();
      alert(`❌ ${err.detail}`);
    }
  });
}

// ============ LOGIN ============
const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
  loginBtn.addEventListener("click", async () => {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const res = await fetch(`${API_USERS}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      alert("✅ Login successful!");
      window.location.href = "dashboard.html";
    } else {
      alert(`❌ ${data.detail}`);
    }
  });
}

// ============ LOGOUT ============
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
  });
}

// ============ LOAD FILES ============
async function loadFiles() {
  const tableBody = document.querySelector("#fileTable tbody");
  if (!tableBody) return;

  const res = await fetch(`${API_FILES}/list`);
  const data = await res.json();

  tableBody.innerHTML = "";
  data.files.forEach((file) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${file.filename}</td>
      <td>
        <button onclick="downloadFile('${file.filename}')">⬇️ Download</button>
        <button onclick="deleteFile('${file.filename}')">🗑️ Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

// ============ UPLOAD FILE ============
const uploadBtn = document.getElementById("uploadBtn");
if (uploadBtn) {
  uploadBtn.addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    if (!file) {
      alert("⚠️ Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_FILES}/upload`, { method: "POST", body: formData });
    if (res.ok) {
      alert("✅ File uploaded successfully!");
      loadFiles();
    } else {
      const err = await res.json();
      alert(`❌ ${err.detail}`);
    }
  });
}

// ============ DOWNLOAD FILE ============
async function downloadFile(filename) {
  const res = await fetch(`${API_FILES}/download/${filename}`);
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

// ============ DELETE FILE ============
async function deleteFile(filename) {
  if (!confirm(`Are you sure you want to delete "${filename}"?`)) return;

  const res = await fetch(`${API_FILES}/delete/${filename}`, { method: "DELETE" });
  if (res.ok) {
    alert("🗑️ File deleted!");
    loadFiles();
  } else {
    const err = await res.json();
    alert(`❌ ${err.detail}`);
  }
}

// ============ GEMINI ANALYSIS ============
const aiBtn = document.getElementById("aiBtn");
if (aiBtn) {
  aiBtn.addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    const aiOutput = document.getElementById("aiOutput");
    const file = fileInput.files[0];

    if (!file) {
      alert("⚠️ Please select a file to analyze.");
      return;
    }

    aiOutput.textContent = "🧠 Analyzing file with Gemini...";

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_AI}/analyze_file`, { method: "POST", body: formData });
    const data = await res.json();

    if (res.ok) {
      aiOutput.textContent = data.summary;
    } else {
      aiOutput.textContent = `❌ ${data.detail}`;
    }
  });
}

// Auto-load files when dashboard opens
if (window.location.pathname.endsWith("dashboard.html")) loadFiles();
