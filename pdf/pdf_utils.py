from tkinter import filedialog

from fpdf import FPDF


def save_as_pdf(explanation):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, f"Explanation:\n{explanation}")
    filename = filedialog.asksaveasfilename(defaultextension=".pdf")
    if filename:
        pdf.output(filename)
