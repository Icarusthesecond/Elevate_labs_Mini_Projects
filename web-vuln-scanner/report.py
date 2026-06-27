from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_pdf(results, summary):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scan_report_{timestamp}.pdf"

    doc = SimpleDocTemplate(f"static/{filename}", pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Web Vulnerability Scan Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Pages Crawled: {summary['total_pages']}", styles['Normal']))
    elements.append(Paragraph(f"Total Vulnerabilities Found: {summary['total_vulns']}", styles['Normal']))
    elements.append(Paragraph(f"Scan Duration: {summary['scan_time']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    for vuln in results:
        elements.append(Paragraph(f"<b>Type:</b> {vuln['type']}", styles['Normal']))
        elements.append(Paragraph(f"<b>URL:</b> {vuln['url']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Severity:</b> {vuln['severity']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Evidence:</b> {vuln['evidence']}", styles['Normal']))
        elements.append(Paragraph(f"<b>Recommendation:</b> {vuln['recommendation']}", styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)

    return filename   # 👈 IMPORTANT
