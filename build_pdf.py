import markdown
import sys
from weasyprint import HTML, CSS

def markdown_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=['tables'])
    
    css_style = '''
    @page { size: A4; margin: 2cm; }
    body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; font-size: 14pt; direction: rtl; text-align: right; }
    h1 { color: #2c3e50; font-size: 24pt; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 20px; }
    h2 { color: #34495e; font-size: 18pt; margin-top: 20px; border-right: 4px solid #3498db; padding-right: 10px; }
    ul { padding-right: 30px; }
    '''

    full_html = f'''<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="UTF-8"></head><body>{html_content}</body></html>'''

    HTML(string=full_html).write_pdf(pdf_file, stylesheets=[CSS(string=css_style)])

markdown_to_pdf("Project_Status_Report.md", "Project_Status_Report.pdf")
