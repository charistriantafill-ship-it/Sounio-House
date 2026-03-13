import streamlit as st
import pandas as pd
import os

# 1. Τίτλος Επιχείρησης (Άλλαξε το "Το Υπέροχο Κατάλυμά μου")
st.set_page_config(page_title="Check-in App", page_icon="🏠")

# 2. Προσθήκη Φωτογραφίας
# Βεβαιώσου ότι η εικόνα είναι στον ίδιο φάκελο και λέγεται π.χ. logo.jpg
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.title("Καλώς ήρθατε στο Sounio Garden House🏠")
st.subheader("Παρακαλούμε συμπληρώστε την επίσημη φόρμα άφιξης")

# Φόρμα στοιχείων
with st.form("checkin_form"):
    name = st.text_input("Ονοματεπώνυμο (όπως αναγράφεται στο διαβατήριο)")
    passport = st.text_input("Αριθμός Ταυτότητας / Διαβατηρίου")
    phone = st.text_input("Τηλέφωνο Επικοινωνίας (με κωδικό χώρας)")
    email = st.text_input("Email")
    
    submit = st.form_submit_button("Ολοκλήρωση Υποβολής")

if submit:
    if name and passport:
        new_data = {"Όνομα": [name], "Διαβατήριο": [passport], "Τηλέφωνο": [phone], "Email": [email]}
        df = pd.DataFrame(new_data)
        
        file_path = "customers.csv"
        if not os.path.isfile(file_path):
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)            
        st.success("Η υποβολή έγινε επιτυχώς! Καλή διαμονή!")
    else:
        st.warning("Παρακαλούμε συμπληρώστε τα υποχρεωτικά πεδία (Όνομα & Διαβατήριο).")