import os
import sys

# Set font config path manually if needed on Windows
if sys.platform == "win32":
    os.environ.setdefault("FONTCONFIG_PATH", "C:/Windows/Fonts")

from weasyprint import HTML


def create_pdf(resume: str, cover_letter: str) -> bytes:
    html_content = f"""
    <html>
    <head>
        <meta charset='utf-8'/>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 24px; }}
            h1 {{ color: #2c3e50; }}
            .section {{ margin-bottom: 28px; }}
            .content {{ white-space: pre-wrap; background: #f7f9fc; padding: 14px; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="section">
            <h1>Optimized Resume</h1>
            <div class="content">{resume}</div>
        </div>
        <div class="section">
            <h1>Tailored Cover Letter</h1>
            <div class="content">{cover_letter}</div>
        </div>
    </body>
    </html>
    """
    return HTML(string=html_content).write_pdf()
