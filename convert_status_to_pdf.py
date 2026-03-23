from markdown2pdf import convert_markdown_to_pdf

def create_pdf():
    try:
        convert_markdown_to_pdf(
            'Project_Status_Report.md',
            'Project_Status_Report.pdf'
        )
        print("✅ PDF created successfully: Project_Status_Report.pdf")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_pdf()