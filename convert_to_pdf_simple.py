"""
Convert Markdown presentation to PDF using markdown2pdf
"""
from markdown2pdf import convert_markdown_to_pdf

def create_pdf():
    """Convert markdown file to PDF"""
    try:
        # Convert markdown to PDF
        convert_markdown_to_pdf(
            'GRADUATION_PRESENTATION.md',
            'GRADUATION_PRESENTATION.pdf'
        )
        print("✅ PDF created successfully: GRADUATION_PRESENTATION.pdf")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_pdf()
