document.getElementById("optimizeBtn").addEventListener("click", async () => {
  const resume = document.getElementById("resumeText").value.trim();
  const jobDesc = document.getElementById("jobDesc").value.trim();

  if (!resume || !jobDesc) {
      alert("Please paste both Resume and Job Description!");
      return;
  }

  document.getElementById("optimizeBtn").innerText = "Optimizing...";
  const response = await fetch("/optimize-resume", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: resume, job_description: jobDesc })
  });

  const data = await response.json();
  document.getElementById("optimizeBtn").innerText = "Optimize";

  if (!response.ok) {
      alert(data.error || "Something went wrong!");
      return;
  }

  document.getElementById("optimizedResume").textContent = data.optimized_output.optimized_resume;
  document.getElementById("tailoredCoverLetter").textContent = data.optimized_output.tailored_cover_letter;
  document.getElementById("outputSection").style.display = "block";
});

document.getElementById("downloadBtn").addEventListener("click", async () => {
  const response = await fetch("/download-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
          resume_text: document.getElementById("optimizedResume").textContent,
          cover_letter: document.getElementById("tailoredCoverLetter").textContent
      })
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Optimized_Resume.pdf";
  a.click();
  window.URL.revokeObjectURL(url);
});
