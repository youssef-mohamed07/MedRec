"""
Convert Markdown presentation to PDF using ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

def parse_markdown_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF with ReportLab"""
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderColor=colors.HexColor('#3498db'),
        borderWidth=2,
        borderPadding=5,
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold',
        leftIndent=10,
        borderColor=colors.HexColor('#3498db'),
        borderWidth=1,
        borderPadding=3,
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=8,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=10,
        spaceBefore=10,
        backColor=colors.HexColor('#f4f4f4'),
    )
    
    # Split content by lines
    lines = content.split('\n')
    
    is_first_h1 = True
    in_code_block = False
    code_lines = []
    in_table = False
    table_data = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            if not in_code_block and not in_table:
                elements.append(Spacer(1, 0.1*inch))
            continue
        
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_lines)
                elements.append(Preformatted(code_text, code_style))
                code_lines = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # Handle horizontal rules
        if line == '---':
            elements.append(PageBreak())
            continue
        
        # Handle headers
        if line.startswith('# '):
            text = line[2:].strip()
            if is_first_h1:
                elements.append(Paragraph(text, title_style))
                is_first_h1 = False
            else:
                elements.append(PageBreak())
                elements.append(Paragraph(text, h1_style))
        elif line.startswith('## '):
            text = line[3:].strip()
            elements.append(Paragraph(text, h2_style))
        elif line.startswith('### '):
            text = line[4:].strip()
            elements.append(Paragraph(text, h3_style))
        
        # Handle tables
        elif line.startswith('|'):
            if not in_table:
                in_table = True
                table_data = []
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            # Skip separator rows
            if not all(c.replace('-', '').strip() == '' for c in cells):
                table_data.append(cells)
        else:
            # End table if we were in one
            if in_table:
                if table_data:
                    t = Table(table_data)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(t)
                    elements.append(Spacer(1, 0.2*inch))
                table_data = []
                in_table = False
            
            # Handle bullet points
            if line.startswith('- ') or line.startswith('* '):
                text = '• ' + line[2:]
                elements.append(Paragraph(text, body_style))
            # Handle numbered lists
            elif re.match(r'^\d+\.', line):
                elements.append(Paragraph(line, body_style))
            # Handle bold text
            elif line.startswith('**') and line.endswith('**'):
                text = '<b>' + line[2:-2] + '</b>'
                elements.append(Paragraph(text, body_style))
            # Regular paragraph
            else:
                # Convert markdown bold to HTML
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                # Convert markdown code to HTML
                text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
                elements.append(Paragraph(text, body_style))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF created successfully: {pdf_file}")

if __name__ == "__main__":
    md_file = "GRADUATION_PRESENTATION.md"
    pdf_file = "GRADUATION_PRESENTATION.pdf"
    
    try:
        parse_markdown_to_pdf(md_file, pdf_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
