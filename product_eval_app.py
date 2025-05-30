import streamlit as st
import pdfkit
import markdown2
from datetime import date
import os

st.set_page_config(page_title="HydroTerra Product Evaluation Tool", layout="centered")

st.image("HydroTerra_Logo Boxed.jpg", width=200)
st.title("HydroTerra Product Evaluation Tool")
st.markdown("Generate structured GPT-based product evaluations with styled PDF export.")

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

# Generate styled PDF from HTML
if st.button("Generate Styled PDF Report") and gpt_output and product_name:
    with open("pdf_template.html", "r") as f:
        template = f.read()

    gpt_html = markdown2.markdown(gpt_output)
    rendered_html = template.format(
        product_name=product_name,
        model_title=model_title,
        product_url=product_url,
        summary=summary,
        report_date=date.today().strftime("%d %B %Y"),
        gpt_html=gpt_html
    )

    # Output PDF file
    pdf_filename = f"{product_name.replace(' ', '_')}_Evaluation_Report.pdf"
    config_path = os.getenv("WKHTMLTOPDF_CMD", "/usr/bin/wkhtmltopdf")
    if os.path.exists(config_path):
        config = pdfkit.configuration(wkhtmltopdf=config_path)
        pdfkit.from_string(rendered_html, pdf_filename, configuration=config)
    else:
        pdfkit.from_string(rendered_html, pdf_filename)

    with open(pdf_filename, "rb") as f:
        st.download_button("📄 Download Styled PDF", f, file_name=pdf_filename, mime="application/pdf")
