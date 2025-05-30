import streamlit as st
from fpdf import FPDF
from datetime import date
import os

st.set_page_config(page_title="HydroTerra Product Evaluation Tool", layout="centered")

st.image("HydroTerra_Logo Boxed.jpg", width=200)
st.title("HydroTerra Product Evaluation Tool")
st.markdown("Generate structured GPT-based product evaluations with branded PDF export.")

# Product input section
st.header("1. Enter Product Info")
product_name = st.text_input("Product Name")
model_title = st.text_input("Model or Page Title")
product_url = st.text_input("Product URL")
summary = st.text_area("Product Summary (1–2 sentences)")

# GPT output section
st.header("2. Paste GPT Output")
gpt_output = st.text_area("Paste the full GPT-generated report here")

# Generate PDF
if st.button("Generate PDF Report") and gpt_output and product_name:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    logo_path = "HydroTerra_Logo Boxed.jpg"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=60)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Product Evaluation Report", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Product Name: {product_name}", ln=True)
    pdf.cell(200, 10, f"Model: {model_title}", ln=True)
    pdf.cell(200, 10, f"URL: {product_url}", ln=True)
    pdf.multi_cell(0, 10, f"Summary: {summary}")
    pdf.ln(5)
    pdf.cell(200, 10, f"Generated: {date.today().strftime('%d %B %Y')}", ln=True)
    pdf.ln(5)
    
    for section in gpt_output.strip().split("\n\n"):
        lines = section.strip().split("\n")
        if lines:
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(0, 10, lines[0])
            pdf.set_font("Arial", "", 11)
            for line in lines[1:]:
                pdf.multi_cell(0, 8, line)
            pdf.ln(3)

    filename = f"{product_name.replace(' ', '_')}_Evaluation_Report.pdf"
    pdf.output(filename)
    
    with open(filename, "rb") as f:
        st.download_button("📄 Download PDF", f, file_name=filename, mime="application/pdf")