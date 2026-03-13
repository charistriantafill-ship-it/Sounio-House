import streamlit as st
import requests
import os
from datetime import datetime

API_URL = "https://sheetdb.io/api/v1/ncc7d3mzgjt97"

st.set_page_config(page_title="Sounio Garden House Check-in", page_icon="🏠")

if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.title("Sounio Garden House 🏠")
st.subheader("Φόρμα Check-in / Registration Form")

with st.form("checkin_form", clear_on_submit=True):
    residence = st.radio(
        "Είστε μόνιμος κάτοικος Ελλάδας; / Are you a Greek resident?", 
        ("Ναι / Yes", "Όχι / No"),
        key="residence_choice"
    )
    
    name = st.text_input("Ονοματεπώνυμο / Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Τηλέφωνο / Phone Number")

    # Χρησιμοποιούμε ξεχωριστά Blocks για να μην "μπερδεύεται" η μνήμη του Streamlit
    if residence == "Ναι / Yes":
        identity_val = st.text_input("ΑΦΜ (Υποχρεωτικό)", key="afm_box")
        country = "Ελλάδα"
    else:
        identity_val = st.text_input("Αριθμός Διαβατηρίου ή Ταυτότητας / Passport or ID Number", key="passport_box")
        country = st.text_input("Χώρα Προέλευσης / Country of Origin", key="country_box")

    submit = st.form_submit_button("Υποβολή Στοιχείων / Submit")

if submit:
    if name and identity_val:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {
            "Ημερομηνία": now,
            "Τύπος": residence,
            "Όνομα": name,
            "Χώρα": country,
            "Στοιχείο": identity_val,
            "Email": email,
            "Τηλέφωνο": phone
        }
        try:
            response = requests.post(API_URL, json={"data": [data]})
            if response.status_code == 201:
                st.success("Η υποβολή έγινε επιτυχώς! Σας ευχαριστούμε.")
                st.balloons()
            else:
                st.error("Κάτι πήγε στραβά με το Excel.")
        except Exception as e:
            st.error(f"Σφάλμα σύνδεσης: {e}")
    else:
        st.error("Παρακαλούμε συμπληρώστε τα υποχρεωτικά πεδία (Όνομα & ΑΦΜ/Διαβατήριο).")


