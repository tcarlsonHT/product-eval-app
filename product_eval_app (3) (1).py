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

# GPT Prompt Generator
if product_name and model_title and product_url and summary:
    st.header("2. Generate GPT Prompt")
    prompt = f'''
You are an environmental technology analyst for HydroTerra.

Evaluate the following product and provide a structured report with:
1. Product Overview (including service gap, innovation, and market alignment)
2. Supplier and Distribution Considerations
3. Competitive Landscape (whether the supplier competes with Solinst or Aquaread)
4. Product Portfolio Review (a table with product name, description, HydroTerra fit, and a rating out of 5)
5. Overall Recommendation and Next Steps
6. A scoring summary out of 35 points:
   - Service Gap (10)
   - Innovation (5)
   - Market Fit (10)
   - Supplier Accessibility (5)
   - Integration Potential (5)

Product Name: {product_name}  
Title: {model_title}  
URL: {product_url}  
Summary: {summary}
'''.strip()
    st.code(prompt, language="markdown")
    st.markdown("👉 Copy this prompt into [ChatGPT](https://chat.openai.com) and paste the response below.")

# GPT output section
st.header("3. Paste GPT Output")
gpt_output = st.text_area("Paste the full GPT-generated report here")

def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "•": "-", "…": "...",
        "×": "x", "°": " degrees"
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Remove or downgrade unsupported characters
    return text.encode("latin-1", "ignore").decode("latin-1")

# Generate PDF
if st.button("Generate PDF Report") and gpt_output and product_name:
    cleaned_output = clean_text(gpt_output)
    cleaned_summary = clean_text(summary)

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
    pdf.multi_cell(0, 10, f"Summary: {cleaned_summary}")
    pdf.ln(5)
    pdf.cell(200, 10, f"Generated: {date.today().strftime('%d %B %Y')}", ln=True)
    pdf.ln(5)

    for section in cleaned_output.strip().split("\n\n"):
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