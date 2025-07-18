import streamlit as st
import pandas as pd
import altair as alt

# ---- Raw Data ----
data = [
    {"Bacteria":"Aerobacter aerogenes", "Penicillin":870, "Streptomycin":1, "Neomycin":1.6, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Bacillus anthracis", "Penicillin":0.001, "Streptomycin":0.01, "Neomycin":0.007, "Gram_Staining":"positive", "Genus": "other"},
    {"Bacteria":"Brucella abortus", "Penicillin":1, "Streptomycin":2, "Neomycin":0.02, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Diplococcus pneumoniae", "Penicillin":0.005, "Streptomycin":11, "Neomycin":10, "Gram_Staining":"positive", "Genus": "other"},
    {"Bacteria":"Escherichia coli", "Penicillin":100, "Streptomycin":0.4, "Neomycin":0.1, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Klebsiella pneumoniae", "Penicillin":850, "Streptomycin":1.2, "Neomycin":1, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Mycobacterium tuberculosis", "Penicillin":800, "Streptomycin":5, "Neomycin":2, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Proteus vulgaris", "Penicillin":3, "Streptomycin":0.1, "Neomycin":0.1, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Pseudomonas aeruginosa", "Penicillin":850, "Streptomycin":2, "Neomycin":0.4, "Gram_Staining":"negative", "Genus": "other"},
    {"Bacteria":"Salmonella (Eberthella) typhosa", "Penicillin":1, "Streptomycin":0.4, "Neomycin":0.008, "Gram_Staining":"negative", "Genus": "Salmonella"},
    {"Bacteria":"Salmonella schottmuelleri", "Penicillin":10, "Streptomycin":0.8, "Neomycin":0.09, "Gram_Staining":"negative", "Genus": "Salmonella"},
    {"Bacteria":"Staphylococcus albus", "Penicillin":0.007, "Streptomycin":0.1, "Neomycin":0.001, "Gram_Staining":"positive", "Genus": "Staphylococcus"},
    {"Bacteria":"Staphylococcus aureus", "Penicillin":0.03, "Streptomycin":0.03, "Neomycin":0.001, "Gram_Staining":"positive", "Genus": "Staphylococcus"},
    {"Bacteria":"Streptococcus fecalis", "Penicillin":1, "Streptomycin":1, "Neomycin":0.1, "Gram_Staining":"positive", "Genus": "Streptococcus"},
    {"Bacteria":"Streptococcus hemolyticus", "Penicillin":0.001, "Streptomycin":14, "Neomycin":10, "Gram_Staining":"positive", "Genus": "Streptococcus"},
    {"Bacteria":"Streptococcus viridans", "Penicillin":0.005, "Streptomycin":10, "Neomycin":40, "Gram_Staining":"positive", "Genus": "Streptococcus"}
]

# ---- Convert to DataFrame ----
df = pd.DataFrame(data)

# ---- Melt DataFrame to long format ----
melted_df = df.melt(
    id_vars=["Bacteria", "Gram_Staining", "Genus"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC"
)

# ---- Base Boxplot ----
base_boxplot = alt.Chart(melted_df).mark_boxplot(extent='min-max', size=30).encode(
    x=alt.X("Antibiotic:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL, log scale)"),
    color=alt.Color(
        "Gram_Staining:N",
        scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),
        legend=alt.Legend(title="Gram Staining")
    )
)

# ---- Annotation for Gram-positive sensitivity ----
annotations = alt.Chart(pd.DataFrame({
    "Antibiotic": ["Penicillin"],
    "MIC": [0.001],
    "text": ["Gram-positive sensitive"]
})).mark_text(
    align="left", dx=5, dy=-10, fontSize=10, color="#ff7f0e"
).encode(
    x="Antibiotic:N",
    y="MIC:Q",
    text="text:N"
)

# ---- Arrow annotation for Gram-negative resistance ----
arrow_annotation = alt.Chart(pd.DataFrame({
    "Antibiotic": ["Penicillin"],
    "MIC": [600],
    "text": ["Penicillin's reduced effectiveness\nagainst Gram-negative bacteria"]
})).mark_text(
    align="center",
    dy=-20,
    fontSize=12,
    fontWeight="bold",
    color="#1f77b4"
).encode(
    x="Antibiotic:N",
    y="MIC:Q",
    text="text:N"
)

# ---- Emoji annotation ----
# Position it near the Penicillin column, slightly above the arrow annotation
emoji_annotation = alt.Chart(pd.DataFrame({
    "Antibiotic": ["Penicillin"],
    "MIC": [800], # Adjust this value to move the emoji up/down
    "emoji": ["😱"]
})).mark_text(
    align="center",
    baseline="middle",
    fontSize=20 # Adjust size as needed
).encode(
    x="Antibiotic:N",
    y="MIC:Q",
    text="emoji:N"
)


# ---- Combine all chart elements ----
final_chart = (base_boxplot + annotations + arrow_annotation + emoji_annotation).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    titleFontSize=14,
    labelFontSize=12
)

# ---- Streamlit App Layout ----
st.title("Antibiotic Effectiveness by Gram Staining")
st.markdown("**Lower MIC = More Effective** - Penicillin shows reduced effectiveness against Gram-negative bacteria.")

# Display the chart
st.altair_chart(final_chart, use_container_width=True)

# Add explanation
st.markdown("""
### Key Observations:
- **Penicillin** is highly effective against Gram-positive bacteria (low MIC values) but much less effective against Gram-negative bacteria (high MIC values).
- **Neomycin** and **Streptomycin** show more consistent effectiveness across both Gram types.
- The outer membrane of Gram-negative bacteria makes them naturally resistant to Penicillin.
""")

