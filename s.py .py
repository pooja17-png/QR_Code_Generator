import streamlit as st
import qrcode
from io import BytesIO
import re

#AI for recipient name suggestion
try:
    from keybert import KeyBERT
    kw_model = KeyBERT()
except ImportError:
    kw_model = None

def suggest_name(upi):
    prefix = upi.split('@')[0]
    if kw_model:
        keywords = kw_model.extract_keywords(prefix)
        if keywords:
            return keywords[0][0].title()
    return re.sub(r'[\._\-]+', ' ', prefix).title() or "Recipient"

def generate_qr(data):
    qr = qrcode.make(data)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf

st.title("💸 Simple UPI QR Code Generator")

upi_id = st.text_input("Enter your UPI ID (e.g. yourname@okaxis):")

if upi_id:
    # Validate UPI format
    pattern = r'^[\w.\-_]{2,256}@[a-zA-Z]{2,64}$'
    if not re.match(pattern, upi_id):
        st.error("⚠️ Invalid UPI ID format. Please enter a valid UPI ID.")
    else:
        recipient_name = suggest_name(upi_id)
        st.success(f"✅ Valid UPI ID! Recipient Name: **{recipient_name}**")

        # Construct UPI URL
        upi_url = f'upi://pay?pa={upi_id}&pn={recipient_name}&mc=1234'

        # Generate and display QR code
        qr_img = generate_qr(upi_url)
        st.image(qr_img, width=250)

        # Download button
        st.download_button("Download QR Code", qr_img, file_name="upi_qr.png", mime="image/png")
else:
    st.info("👆 Please enter your UPI ID to generate QR code.")
