import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="HazMap App", layout="wide")

# --------- Mock Database ---------
mock_assets = [
    {
        "Date": datetime(2024, 5, 10), "Surveyor": "Simon Harrop", "Building Name": "Chemistry Block",
        "Floor": "Ground", "Location": "Entrance Lobby", "Item": "Vinyl Flooring", "Material Code": "FL01",
        "Material": "Vinyl", "Sample Number": "S001", "Sample Notes": "Dark grey with flecks",
        "Approach": "Encapsulation", "Recommended Action": "Monitor", "Recommended Comments": "Monitor for wear",
        "HazMat Identification": "Yes", "Product Type": "Flooring", "Condition": "Fair",
        "Surface Treatment": "Sealed", "Asbestos Type": "Chrysotile", "Material Score": 5, "Priority Score": 4,
        "Total Score": 9, "Product Description": "Resilient floor tiles", "Condition Description": "Minor cracks",
        "Surface Treatment Description": "Surface sealed", "Tags": ["Confirmed HazMat"]
    },
    {
        "Date": datetime(2024, 5, 10), "Surveyor": "Simon Harrop", "Building Name": "Chemistry Block",
        "Floor": "Level 1", "Location": "Toilet", "Item": "Pipe Insulation", "Material Code": "PI01",
        "Material": "Thermal insulation", "Sample Number": "S002", "Sample Notes": "Fibrous white wrap",
        "Approach": "Removal", "Recommended Action": "Remove", "Recommended Comments": "Immediate removal required",
        "HazMat Identification": "Yes", "Product Type": "Pipes", "Condition": "Poor",
        "Surface Treatment": "Unsealed", "Asbestos Type": "Amosite", "Material Score": 8, "Priority Score": 6,
        "Total Score": 14, "Product Description": "Thermal lagging on pipes", "Condition Description": "Crumbling",
        "Surface Treatment Description": "Exposed wrap", "Tags": ["Confirmed HazMat", "Requires Reinspection"]
    },
    {
        "Date": datetime(2024, 5, 10), "Surveyor": "Simon Harrop", "Building Name": "Physics Annex",
        "Floor": "Basement", "Location": "Utility Room", "Item": "Ceiling Panels", "Material Code": "CL01",
        "Material": "ACM", "Sample Number": "S003", "Sample Notes": "Loose board with gaps",
        "Approach": "Monitoring", "Recommended Action": "Reinspect", "Recommended Comments": "Check integrity monthly",
        "HazMat Identification": "Yes", "Product Type": "Ceiling", "Condition": "Poor",
        "Surface Treatment": "Painted", "Asbestos Type": "Crocidolite", "Material Score": 7, "Priority Score": 5,
        "Total Score": 12, "Product Description": "Suspended panel ceiling", "Condition Description": "Visible damage",
        "Surface Treatment Description": "Old paint layers", "Tags": ["Confirmed HazMat"]
    },
    {
        "Date": datetime(2024, 5, 11), "Surveyor": "Simon Harrop", "Building Name": "Library Wing",
        "Floor": "Level 2", "Location": "Main Hall", "Item": "Wall Plaster", "Material Code": "WL01",
        "Material": "Plaster", "Sample Number": "S004", "Sample Notes": "Smooth white plaster",
        "Approach": "None", "Recommended Action": "Monitor", "Recommended Comments": "Check during next review",
        "HazMat Identification": "No", "Product Type": "Walls", "Condition": "Good",
        "Surface Treatment": "Painted", "Asbestos Type": "", "Material Score": 1, "Priority Score": 1,
        "Total Score": 2, "Product Description": "Wall finish plaster", "Condition Description": "No visible damage",
        "Surface Treatment Description": "Painted surface", "Tags": ["No HazMat Detected"]
    },
    {
        "Date": datetime(2024, 5, 11), "Surveyor": "Simon Harrop", "Building Name": "Admin Office",
        "Floor": "Ground", "Location": "Reception", "Item": "Ceiling Tiles", "Material Code": "CL02",
        "Material": "Mineral fibre", "Sample Number": "S005", "Sample Notes": "Lightweight panels",
        "Approach": "Monitoring", "Recommended Action": "Reinspect", "Recommended Comments": "Annual review",
        "HazMat Identification": "No", "Product Type": "Ceiling", "Condition": "Good",
        "Surface Treatment": "Painted", "Asbestos Type": "", "Material Score": 1, "Priority Score": 2,
        "Total Score": 3, "Product Description": "Non-ACM ceiling panels", "Condition Description": "Intact",
        "Surface Treatment Description": "Smooth paint", "Tags": ["No HazMat Detected"]
    },
    {
        "Date": datetime(2024, 5, 12), "Surveyor": "Simon Harrop", "Building Name": "Engineering Lab",
        "Floor": "Basement", "Location": "Pump Room", "Item": "Pipes", "Material Code": "PI02",
        "Material": "Insulation", "Sample Number": "S006", "Sample Notes": "Peeling insulation",
        "Approach": "Removal", "Recommended Action": "Remove", "Recommended Comments": "High priority",
        "HazMat Identification": "Yes", "Product Type": "Pipes", "Condition": "Poor",
        "Surface Treatment": "Unsealed", "Asbestos Type": "Amosite", "Material Score": 9, "Priority Score": 6,
        "Total Score": 15, "Product Description": "Aged thermal wrap", "Condition Description": "Brittle",
        "Surface Treatment Description": "Fibrous", "Tags": ["Confirmed HazMat", "Actioned"]
    },
    {
        "Date": datetime(2024, 5, 12), "Surveyor": "Simon Harrop", "Building Name": "Medical Sciences",
        "Floor": "Level 1", "Location": "Lecture Theatre", "Item": "Wall Panels", "Material Code": "WL02",
        "Material": "Composite", "Sample Number": "S007", "Sample Notes": "Soundproof panel",
        "Approach": "Monitoring", "Recommended Action": "Reinspect", "Recommended Comments": "No immediate risk",
        "HazMat Identification": "No", "Product Type": "Walls", "Condition": "Good",
        "Surface Treatment": "Painted", "Asbestos Type": "", "Material Score": 2, "Priority Score": 2,
        "Total Score": 4, "Product Description": "Acoustic composite panels", "Condition Description": "Stable",
        "Surface Treatment Description": "Painted", "Tags": ["No HazMat Detected"]
    },
    {
        "Date": datetime(2024, 5, 13), "Surveyor": "Simon Harrop", "Building Name": "Arts Building",
        "Floor": "Level 3", "Location": "Studio", "Item": "Ceiling Tiles", "Material Code": "CL03",
        "Material": "Textured paint ACM", "Sample Number": "S008", "Sample Notes": "Decorative swirl",
        "Approach": "Encapsulation", "Recommended Action": "Monitor", "Recommended Comments": "Low priority",
        "HazMat Identification": "Yes", "Product Type": "Ceiling", "Condition": "Fair",
        "Surface Treatment": "Painted", "Asbestos Type": "Chrysotile", "Material Score": 4, "Priority Score": 3,
        "Total Score": 7, "Product Description": "Decorative finish tiles", "Condition Description": "Faded",
        "Surface Treatment Description": "Old paint", "Tags": ["Confirmed HazMat"]
    },
    {
        "Date": datetime(2024, 5, 13), "Surveyor": "Simon Harrop", "Building Name": "Lecture Hall 2",
        "Floor": "Ground", "Location": "Back Door", "Item": "Fire Door", "Material Code": "DR01",
        "Material": "Insulated core", "Sample Number": "S009", "Sample Notes": "Metal covered",
        "Approach": "Monitoring", "Recommended Action": "Monitor", "Recommended Comments": "No visible issues",
        "HazMat Identification": "No", "Product Type": "Doors", "Condition": "Good",
        "Surface Treatment": "Painted", "Asbestos Type": "", "Material Score": 1, "Priority Score": 1,
        "Total Score": 2, "Product Description": "Heavy-duty fire door", "Condition Description": "New install",
        "Surface Treatment Description": "Paint intact", "Tags": ["No HazMat Detected"]
    },
    {
        "Date": datetime(2024, 5, 13), "Surveyor": "Simon Harrop", "Building Name": "Science West",
        "Floor": "Roof", "Location": "Maintenance Hatch", "Item": "Roof Sheeting", "Material Code": "RF01",
        "Material": "Corrugated cement", "Sample Number": "S010", "Sample Notes": "Light grey, weathered",
        "Approach": "Encapsulation", "Recommended Action": "Reinspect", "Recommended Comments": "Check after storms",
        "HazMat Identification": "Yes", "Product Type": "Roof", "Condition": "Fair",
        "Surface Treatment": "Unsealed", "Asbestos Type": "Chrysotile", "Material Score": 6, "Priority Score": 5,
        "Total Score": 11, "Product Description": "Old corrugated panels", "Condition Description": "Aged surface",
        "Surface Treatment Description": "Unsealed", "Tags": ["Confirmed HazMat"]
    }
]

if "assets" not in st.session_state:
    st.session_state.assets = mock_assets

# --------- Sidebar Navigation ---------
st.sidebar.title("Client & Project")
client = st.sidebar.selectbox("Select Client", ["UWA", "Tetra Tech", "Other"])
project = st.sidebar.text_input("Site Name (Project)", "Crawley Campus - Chemistry Building")

st.title(f"Project: {project}")
st.subheader("Add Site Asset")

# --------- Asset Entry Form ---------
with st.form("asset_form"):
    st.markdown("### General")
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date", datetime.today())
        surveyor = st.text_input("Surveyor")
        building_name = st.text_input("Building Name")
        floor = st.text_input("Floor")
        location = st.text_input("Location")
    with col2:
        item = st.text_input("Item")
        material_code = st.text_input("Material Code")
        material = st.text_input("Material")
        sample_number = st.text_input("Sample Number")
        sample_notes = st.text_area("Sample Notes")
    with col3:
        approach = st.selectbox("Approach", ["Encapsulation", "Removal", "Monitoring", "None"])
        rec_action = st.selectbox("Recommended Action", ["Remove", "Monitor", "Reinspect"])
        rec_comments = st.text_area("Recommended Comments")

    st.markdown("### Identification & Risk Score")
    col4, col5, col6 = st.columns(3)
    with col4:
        hazmat_id = st.selectbox("HazMat Identification", ["Yes", "No"])
        product_type = st.text_input("Product Type")
        condition = st.selectbox("Condition", ["Good", "Fair", "Poor"])
        surface_treatment = st.text_input("Surface Treatment")
    with col5:
        asbestos_type = st.text_input("Asbestos Type")
        material_score = st.number_input("Material Score", 0, 10)
        priority_score = st.number_input("Priority Score", 0, 10)
        total_score = material_score + priority_score
    with col6:
        product_desc = st.text_area("Product Description")
        condition_desc = st.text_area("Condition Description")
        surface_desc = st.text_area("Surface Treatment Description")

    tags = st.multiselect("Tags", ["Pending Lab", "Confirmed HazMat", "No HazMat Detected", "Requires Reinspection", "Actioned", "Cleared for Works", "Review Required"])

    submitted = st.form_submit_button("Add Asset")
    if submitted:
        st.session_state.assets.append({
            "Date": date,
            "Surveyor": surveyor,
            "Building Name": building_name,
            "Floor": floor,
            "Location": location,
            "Item": item,
            "Material Code": material_code,
            "Material": material,
            "Sample Number": sample_number,
            "Sample Notes": sample_notes,
            "Approach": approach,
            "Recommended Action": rec_action,
            "Recommended Comments": rec_comments,
            "HazMat Identification": hazmat_id,
            "Product Type": product_type,
            "Condition": condition,
            "Surface Treatment": surface_treatment,
            "Asbestos Type": asbestos_type,
            "Material Score": material_score,
            "Priority Score": priority_score,
            "Total Score": total_score,
            "Product Description": product_desc,
            "Condition Description": condition_desc,
            "Surface Treatment Description": surface_desc,
            "Tags": tags
        })
        st.success("Asset added successfully!")

# --------- Display Assets ---------
st.subheader("Recorded Site Assets")
if st.session_state.assets:
    df = pd.DataFrame(st.session_state.assets)

    selected_tags = st.multiselect("Filter by Tag", ["Pending Lab", "Confirmed HazMat", "No HazMat Detected", "Requires Reinspection", "Actioned", "Cleared for Works", "Review Required"])
    if selected_tags:
        df = df[df['Tags'].apply(lambda x: any(tag in x for tag in selected_tags))]

    st.dataframe(df, use_container_width=True)

    # --------- Export Buttons ---------
    st.markdown("### Export Options")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Export to CSV", csv, "hazmat_assets.csv", "text/csv")
    with col_exp2:
        try:
            import pdfkit
            html = df.to_html(index=False)
            pdf = pdfkit.from_string(html, False)
            st.download_button("Export to PDF", pdf, "hazmat_assets.pdf", "application/pdf")
        except:
            st.info("PDF export requires `pdfkit` and `wkhtmltopdf` installed.")
else:
    st.info("No assets recorded yet.")