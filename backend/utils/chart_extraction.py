import fitz
import os

def extract_charts(filepath, output_dir):
    doc = fitz.open(filepath)
    charts = []
    for page in doc:
        for img in page.get_images():
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            chart_path = os.path.join(output_dir, f"chart_{xref}.png")
            pix.save(chart_path)
            charts.append(chart_path)
            pix = None
    return charts
