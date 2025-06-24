import os
import sys

# Set font config path manually if needed
if sys.platform == "win32":
    os.environ["FONTCONFIG_PATH"] = "C:/Windows/Fonts"

from weasyprint import HTML

def generate_pdf(resume: str, cover_letter: str) -> bytes:
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            h1 {{
                color: #333;
            }}
            .section {{
                margin-bottom: 40px;
            }}
            .content {{
                white-space: pre-wrap;
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
            }}
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
