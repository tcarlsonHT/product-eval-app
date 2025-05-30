#!/bin/bash
# Setup script for wkhtmltopdf on Streamlit Cloud

mkdir -p ~/.local/bin
curl -L -o ~/.local/bin/wkhtmltopdf https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.alpine3.12.x86_64.apk
chmod +x ~/.local/bin/wkhtmltopdf
echo "Wkhtmltopdf installed to ~/.local/bin"