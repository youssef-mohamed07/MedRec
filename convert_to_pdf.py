"""
Convert Markdown presentation to PDF
"""
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def markdown_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF with styling"""
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    # Add CSS styling
    css_style = """
    @page {
        size: A4;
        margin: 2cm;
        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10pt;
            color: #666;
        }
    }
    
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        font-size: 11pt;
    }
    
    h1 {
        color: #2c3e50;
        font-size: 24pt;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 20px;
        page-break-before: always;
    }
    
    h1:first-of-type {
        page-break-before: avoid;
        font-size: 28pt;
        text-align: center;
        color: #3498db;
    }
    
    h2 {
        color: #34495e;
        font-size: 18pt;
        margin-top: 20px;
        border-left: 4px solid #3498db;
        padding-left: 10px;
    }
    
    h3 {
        color: #7f8c8d;
        font-size: 14pt;
        margin-top: 15px;
    }
    
    code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 10pt;
    }
    
    pre {
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 9pt;
        line-height: 1.4;
    }
    
    pre code {
        background-color: transparent;
        color: #ecf0f1;
        padding: 0;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        font-size: 10pt;
    }
    
    th {
        background-color: #3498db;
        color: white;
        padding: 10px;
        text-align: left;
        font-weight: bold;
    }
    
    td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 5px 0;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 15px;
        margin: 15px 0;
        color: #555;
        font-style: italic;
    }
    
    hr {
        border: none;
        border-top: 2px solid #ecf0f1;
        margin: 30px 0;
    }
    
    strong {
        color: #2c3e50;
        font-weight: 600;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    .page-break {
        page-break-after: always;
    }
    """
    
    # Create full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>MedRec - Graduation Project Presentation</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert to PDF
    HTML(string=full_html).write_pdf(
        pdf_file,
        stylesheets=[CSS(string=css_style)]
    )
    
    print(f"✅ PDF created successfully: {pdf_file}")

if __name__ == "__main__":
    md_file = "GRADUATION_PRESENTATION.md"
    pdf_file = "GRADUATION_PRESENTATION.pdf"
    
    if Path(md_file).exists():
        markdown_to_pdf(md_file, pdf_file)
    else:
        print(f"❌ Error: {md_file} not found")
