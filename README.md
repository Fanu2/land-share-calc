# 🧮 Punjab Rural Land Share Calculator

A powerful Streamlit-based tool for calculating and visualizing land ownership shares in Punjab's rural estates. Designed with both manual entry and Excel file support, this app breaks down land shares into **Kila, Kanal, Marla, and Sarshai**, and provides validation and pie chart visualizations.

---

## 🔧 Features

- ✅ **Manual data entry** OR **upload from Excel**
- 📊 **Owner-wise and estate-wise share summaries**
- 📈 **Interactive pie chart** for estate share distribution
- 📥 **Downloadable Excel output** with:
  - Detailed owner data
  - Aggregated owner summary
  - Validation report
- ✅ Validates that estate shares sum to **1 (or 100%)**
- 🇮🇳 Supports Punjabi rural land units (Kila, Kanal, Marla, Sarshai, Acre)

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install streamlit pandas openpyxl plotly
📄 Input Formats
Manual Entry

Enter:

    Khewat, Marba, Killa Numbers

    Total area (Kanal + Marla)

    Owner name

    Share fraction (e.g. 1/2, 3/8)

Excel Upload

Use the following column headers:
Khewat No	Marba No	Killa No	Total Area (Kanal)	Total Area (Marla)	Owner Name	Share Fraction
📤 Output

    An Excel file with:

        Detailed Output: Owner-level breakdown

        Owner Summary: Aggregated holdings

        Validation Report: Highlight estates with incorrect total shares

📊 Visual Insights

    Pie chart of share distribution by owner per estate.

    Table of holdings per owner (converted into traditional units).

❗Validation

The app warns you if:

    A share fraction is invalid

    The sum of shares in an estate is not ≈ 1.00 (tolerance ±0.01)

🧠 Units Reference
Unit	Description
1 Kanal	20 Marla
1 Marla	9 Sarshai
1 Kila	8 Kanal
1 Acre	8 Kanal (approx)
📬 Contributions

Feel free to fork this repository or suggest improvements via issues or pull requests!
📃 License

This project is released under the MIT License.

