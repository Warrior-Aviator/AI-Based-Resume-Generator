function collectFormAsResumeText() {
  const name = document.getElementById("name").value || "Candidate Name";
  const contact = document.getElementById("contact").value || "Email | Phone | Location";
  const summary = document.getElementById("summary").value;
  const education = document.getElementById("education").value;
  const experience = document.getElementById("experience").value;
  const projects = document.getElementById("projects").value;
  const skills = document.getElementById("skills").value;
  const hobbies = document.getElementById("hobbies").value;
  const achievements = document.getElementById("achievements").value;

  // Compose a plaintext resume for the model
  return `NAME: ${name}\nCONTACT: ${contact}\n\nSUMMARY\n${summary}\n\nEDUCATION\n${education}\n\nEXPERIENCE\n${experience}\n\nPROJECTS\n${projects}\n\nSKILLS\n${skills}\n\nHOBBIES\n${hobbies}\n\nACHIEVEMENTS\n${achievements}`;
}

function setScore(val) {
  const n = Math.max(0, Math.min(100, parseInt(val || 0)));
  const el = document.getElementById("scoreFill");
  el.style.width = `${n}%`;
  el.textContent = `${n}%`;
}

document.getElementById("optimizeBtn").addEventListener("click", async () => {
  const resumeText = collectFormAsResumeText();
  const jobDescription = document.getElementById("jobDescription").value || "";
  const template = document.getElementById("templateSelect").value;

  try {
    const response = await fetch("/optimize-resume", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
        template: template
      })
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("resumeOutput").innerText = data.optimized_resume || "";
      document.getElementById("coverLetterOutput").innerText = data.cover_letter || "";
      setScore(data.match_score || 0);
    } else {
      document.getElementById("resumeOutput").innerText = "❌ " + (data.error || "Something went wrong");
      document.getElementById("coverLetterOutput").innerText = "";
      setScore(0);
    }
  } catch (err) {
    console.error("Request failed:", err);
    document.getElementById("resumeOutput").innerText = "⚠️ Request failed. Check console for details.";
    document.getElementById("coverLetterOutput").innerText = "";
    setScore(0);
  }
});

// Preview button → posts to /preview in a new tab with the chosen template and current outputs
document.getElementById("previewBtn").addEventListener("click", () => {
  const form = document.getElementById("previewForm");
  form.innerHTML = ""; // reset

  const add = (name, val) => {
    const input = document.createElement("input");
    input.type = "hidden"; input.name = name; input.value = val; form.appendChild(input);
  };

  add("template", document.getElementById("templateSelect").value);
  add("name", document.getElementById("name").value || "Candidate Name");
  add("contact_info", document.getElementById("contact").value || "Email | Phone | Location");
  add("summary", document.getElementById("summary").value);
  add("education", document.getElementById("education").value);
  add("experience", document.getElementById("experience").value);
  add("projects", document.getElementById("projects").value);
  add("skills", document.getElementById("skills").value);
  add("hobbies", document.getElementById("hobbies").value);
  add("achievements", document.getElementById("achievements").value);
  add("cover_letter", document.getElementById("coverLetterOutput").innerText);

  form.submit();
});

// Download PDF → use optimized text currently displayed
document.getElementById("downloadPdfBtn").addEventListener("click", async () => {
  const resume = document.getElementById("resumeOutput").innerText.trim();
  const cover = document.getElementById("coverLetterOutput").innerText.trim();
  if (!resume) { alert("Please run Optimize first."); return; }

  const response = await fetch("/generate-pdf", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ resume_text: resume, cover_letter: cover })
  });
  const data = await response.json();
  if (data.pdf_path) {
    window.location.href = data.pdf_path; // open/download
  } else {
    alert("❌ Failed to generate PDF");
  }
});
