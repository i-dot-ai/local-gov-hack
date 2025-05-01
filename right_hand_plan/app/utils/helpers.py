from fpdf import FPDF

def generate_pdf_report(validation_result, relevant_policies):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Validation Report", ln = True, align = 'C')
    pdf.ln(10)
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt = validation_result)
    pdf.ln(10)
    pdf.set_font("Arial", size = 12)
    pdf.cell(0, 10, txt = "Relevant Policies:", ln = True, align = 'L')
    for policy in relevant_policies:
        pdf.cell(0, 10, txt = policy, ln = True, align = 'L')
    pdf.output("validation_report.pdf")
    return "validation_report.pdf"