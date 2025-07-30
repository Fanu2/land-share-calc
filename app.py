import streamlit as st
import pandas as pd
import io
from fractions import Fraction
import plotly.express as px

KANAL_TO_MARLA = 20
MARLA_TO_SARSAI = 9
KANAL_TO_ACRE = 0.125
KILAS_IN_KANAL = 8

st.set_page_config(page_title="Land Share Calculator", layout="wide")
st.title("🧮 Punjab Rural Land Share Calculator - Polished UI & Estate Pie Chart")

def breakdown_area(share_kanal):
    kila = int(share_kanal // KILAS_IN_KANAL)
    kanal_remain = share_kanal % KILAS_IN_KANAL
    kanal = int(kanal_remain)
    marla_fraction = (kanal_remain - kanal) * KANAL_TO_MARLA
    marla = int(marla_fraction)
    sarshai = round((marla_fraction - marla) * MARLA_TO_SARSAI)
    return kila, kanal, marla, sarshai

def parse_fraction(frac_str):
    try:
        if ' ' in frac_str:
            whole, frac = frac_str.split()
            return float(int(whole) + Fraction(frac))
        else:
            return float(Fraction(frac_str))
    except Exception:
        return None

def to_excel_bytes(df1, df2, validation_df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df1.to_excel(writer, index=False, sheet_name='Detailed Output')
    df2.to_excel(writer, index=False, sheet_name='Owner Summary')
    validation_df.to_excel(writer, index=False, sheet_name='Validation Report')
    writer.close()
    output.seek(0)
    return output

if 'rows' not in st.session_state:
    st.session_state.rows = [{}]

st.sidebar.header("Input Mode")
input_method = st.sidebar.radio("Choose input method", ["Manual Entry", "Upload Excel File"])

validation_errors = []

data_rows = []
df_uploaded = pd.DataFrame()

if input_method == "Upload Excel File":
    uploaded_file = st.sidebar.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])
    if uploaded_file:
        df_uploaded = pd.read_excel(uploaded_file)
        st.subheader("Uploaded Data Preview")
        st.dataframe(df_uploaded)

        # Editable table for correction
        st.subheader("Edit Uploaded Data")
        edited_df = st.experimental_data_editor(df_uploaded, num_rows="dynamic")

else:
    st.sidebar.subheader("Manual Entry Rows")
    if st.sidebar.button("Add Row"):
        st.session_state.rows.append({})
    if st.sidebar.button("Remove Last Row") and len(st.session_state.rows) > 1:
        st.session_state.rows.pop()

    st.subheader("Manual Land Entry")
    for i in range(len(st.session_state.rows)):
        with st.expander(f"Entry {i+1}"):
            cols = st.columns([1.2,1.2,1.2,1,1,2,1])
            with cols[0]:
                khewat = st.text_input("Khewat No", key=f"khewat_{i}", placeholder="e.g. 123")
            with cols[1]:
                marba = st.text_input("Marba No", key=f"marba_{i}", placeholder="e.g. 456")
            with cols[2]:
                killa = st.text_input("Killa No", key=f"killa_{i}", placeholder="e.g. 7")
            with cols[3]:
                kanal = st.number_input("Total Area (Kanal)", 0.0, 10000.0, step=0.1, key=f"kanal_{i}")
            with cols[4]:
                marla = st.number_input("Total Area (Marla)", 0.0, 19.0, step=0.1, key=f"marla_{i}")
            with cols[5]:
                owner = st.text_input("Owner Name", key=f"owner_{i}", placeholder="Owner full name")
            with cols[6]:
                share_frac = st.text_input("Share Fraction (e.g. 1/2)", key=f"share_{i}", placeholder="e.g. 1/2")

            frac = parse_fraction(share_frac) if share_frac else None
            if frac is None and share_frac:
                validation_errors.append(f"Row {i+1}: Invalid share fraction '{share_frac}'")

            if frac is not None and share_frac:
                area_kanal = kanal + (marla / KANAL_TO_MARLA)
                share_area = area_kanal * frac
                kila, kanal_out, marla_out, sarshai_out = breakdown_area(share_area)
                data_rows.append({
                    "Khewat": khewat,
                    "Marba": marba,
                    "Killa": killa,
                    "Owner": owner,
                    "Share Fraction": share_frac,
                    "Share Area (Kanal)": share_area,
                    "Kila": kila,
                    "Kanal": kanal_out,
                    "Marla": marla_out,
                    "Sarshai": sarshai_out,
                    "Acre": round(share_area * KANAL_TO_ACRE, 3)
                })

if not df_uploaded.empty:
    df_to_process = edited_df if 'edited_df' in locals() else df_uploaded
    for idx, row in df_to_process.iterrows():
        frac = parse_fraction(str(row.get("Share Fraction", "")))
        if frac is None:
            st.error(f"Invalid fraction in uploaded file row {idx+1}: {row.get('Share Fraction')}")
            continue
        try:
            kanal = float(row["Total Area (Kanal)"])
            marla = float(row["Total Area (Marla)"])
            area_kanal = kanal + (marla / KANAL_TO_MARLA)
            share_area = area_kanal * frac
            kila, kanal_out, marla_out, sarshai_out = breakdown_area(share_area)
            data_rows.append({
                "Khewat": row["Khewat No"],
                "Marba": row["Marba No"],
                "Killa": row["Killa No"],
                "Owner": row["Owner Name"],
                "Share Fraction": row["Share Fraction"],
                "Share Area (Kanal)": share_area,
                "Kila": kila,
                "Kanal": kanal_out,
                "Marla": marla_out,
                "Sarshai": sarshai_out,
                "Acre": round(share_area * KANAL_TO_ACRE, 3)
            })
        except Exception as e:
            st.error(f"Error in uploaded file row {idx+1}: {e}")

if validation_errors:
    for err in validation_errors:
        st.error(err)

if data_rows:
    df = pd.DataFrame(data_rows)
    st.subheader("🔍 Individual Share Calculations")
    st.dataframe(df)

    df['Estate'] = df['Khewat'].astype(str) + "-" + df['Marba'].astype(str) + "-" + df['Killa'].astype(str)

    share_sum = df.groupby('Estate')['Share Fraction'].apply(lambda x: sum(parse_fraction(str(f)) for f in x)).reset_index(name='Total Share')
    invalid_shares = share_sum[(share_sum['Total Share'] < 0.99) | (share_sum['Total Share'] > 1.01)]

    if not invalid_shares.empty:
        st.error("Shares for these estates do not sum to 1:\n" + invalid_shares.to_string(index=False))
    else:
        st.success("All estate shares sum to 1.")

    st.subheader("📊 Owner-wise Summary")
    summary = df.groupby("Owner")["Share Area (Kanal)"].sum().reset_index()
    summary[["Kila", "Kanal", "Marla", "Sarshai", "Acre"]] = summary["Share Area (Kanal)"].apply(
        lambda x: pd.Series(list(breakdown_area(x)) + [round(x * KANAL_TO_ACRE, 3)])
    )
    st.dataframe(summary)

    st.subheader("🏡 Estate-wise Share Distribution")
    estates = sorted(df["Estate"].unique())
    estate_selected = st.selectbox("Select Estate", estates)

    estate_df = df[df["Estate"] == estate_selected]
    fig = px.pie(estate_df, values="Share Area (Kanal)", names="Owner",
                 title=f"Land Share Distribution for Estate: {estate_selected}")
    st.plotly_chart(fig, use_container_width=True)

    xlsx = to_excel_bytes(df, summary, invalid_shares)
    st.download_button("📥 Download Results (Excel with Validation Report)", data=xlsx,
                       file_name="land_share_results.xlsx")
