// ==== BASE URL ====
const BASE_URL = "http://127.0.0.1:8000";
const API_USERS = `${BASE_URL}/users`;
const API_FILES = `${BASE_URL}/files`;
const API_AI = `${BASE_URL}/ai`;

// ======== PAGE LOAD PROTECTION ========
document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname.endsWith("dashboard.html")) {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "index.html";
    } else {
      loadFiles();
    }
  }
});

// ======== SIGNUP ========
const signupBtn = document.getElementById("signupBtn");
if (signupBtn) {
  signupBtn.addEventListener("click", async () => {
    const username = document.getElementById("signupUsername").value.trim();
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value.trim();

    if (!username || !email || !password) {
      alert("⚠️ Fill all fields!");
      return;
    }

    const res = await fetch(`${API_USERS}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();
    if (res.ok) {
      alert("✅ Signup successful! Please login.");
      window.location.href = "index.html";
    } else {
      alert(`❌ ${data.detail}`);
    }
  });
}

// ======== LOGIN ========
const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
  loginBtn.addEventListener("click", async () => {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    if (!email || !password) {
      alert("⚠️ Fill both fields!");
      return;
    }

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

// ======== LOGOUT ========
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
  });
}

// ======== UPLOAD FILE ========
const uploadBtn = document.getElementById("uploadBtn");
if (uploadBtn) {
  uploadBtn.addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
      alert("⚠️ Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_FILES}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (res.ok) {
        alert("✅ File uploaded!");
        loadFiles();
      } else {
        alert(`❌ ${data.detail || "Upload failed"}`);
      }
    } catch (err) {
      console.error("Upload error:", err);
      alert("⚠️ Upload failed. Check backend logs.");
    }
  });
}


// ======== LOAD FILES ========
async function loadFiles() {
  const tableBody = document.querySelector("#fileTable tbody");
  if (!tableBody) return;

  tableBody.innerHTML = "<tr><td colspan='2'>⏳ Loading...</td></tr>";

  const res = await fetch(`${API_FILES}/list`);
  const data = await res.json();

  tableBody.innerHTML = "";
  if (!data.files || data.files.length === 0) {
    tableBody.innerHTML = "<tr><td colspan='2'>No files yet.</td></tr>";
    return;
  }

  data.files.forEach((file) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${file.filename}</td>
      <td>
        <a href="${file.url}" target="_blank">🌐 View</a>
        <button onclick="deleteFile('${file.public_id}')">🗑️ Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

// ======== DELETE FILE ========
async function deleteFile(publicId) {
  if (!confirm("Delete this file?")) return;

  try {
    const res = await fetch(`${API_FILES}/delete/${encodeURIComponent(publicId)}`, {
      method: "DELETE",
    });

    const data = await res.json();
    if (res.ok) {
      alert("🗑️ Deleted!");
      loadFiles();
    } else {
      alert(`❌ ${data.detail}`);
    }
  } catch (err) {
    console.error("Delete error:", err);
    alert("⚠️ Delete failed.");
  }
}

// ======== ANALYZE WITH GEMINI ========
const aiBtn = document.getElementById("aiBtn");
if (aiBtn) {
  aiBtn.addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const aiOutput = document.getElementById("aiOutput");

    if (!file) {
      alert("⚠️ Select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_AI}/analyze_file`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (res.ok) {
        aiOutput.textContent = data.summary;
      } else {
        aiOutput.textContent = `❌ ${data.detail}`;
      }
    } catch (err) {
      aiOutput.textContent = "⚠️ Failed to analyze file.";
    }
  });
}
