from fpdf import FPDF


class createPdf():
    def __init__(self):
        pdf = FPDF('P', 'mm', 'Letter')
        pdf.set_font('courier')
        pdf.add_page()