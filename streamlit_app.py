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
# Added a small 'size' and opacity to ensure boxes are visible even if narrow
# Also applied stroke and strokeWidth to the 'box' sub-property for clarity
base_boxplot = alt.Chart(melted_df).mark_boxplot(
    extent='min-max',
    size=20, # Give it a fixed size to ensure visibility
    opacity=0.7, # Add some opacity
    box=alt.MarkConfig(stroke='black', strokeWidth=0.5) # Apply stroke to the box itself
).encode(
    x=alt.X("Antibiotic:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL, log scale)"),
    color=alt.Color(
        "Gram_Staining:N",
        scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),
        legend=alt.Legend(title="Gram Staining")
    )
)

# ---- Layer individual points on top of the boxplot ----
# This ensures all data points are visible, even if the box is very small
point_layer = alt.Chart(melted_df).mark_circle(size=40, opacity=0.8, stroke='black', strokeWidth=0.2).encode(
    x=alt.X("Antibiotic:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log")), # Share the same log scale
    color=alt.Color(
        "Gram_Staining:N",
        scale=alt.Scale(range=["#1f77b4", "#ff7f0e"])
    ),
    tooltip=[
        alt.Tooltip("Bacteria:N", title="Bacterium"),
        alt.Tooltip("Antibiotic:N", title="Antibiotic"),
        alt.Tooltip("MIC:Q", title="MIC (µg/mL)", format=".3f"),
        alt.Tooltip("Gram_Staining:N", title="Gram Staining")
    ]
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
emoji_annotation = alt.Chart(pd.DataFrame({
    "Antibiotic": ["Penicillin"],
    "MIC": [400],
    "emoji": ["😱"]
})).mark_text(
    align="center",
    baseline="middle",
    fontSize=20
).encode(
    x="Antibiotic:N",
    y="MIC:Q",
    text="emoji:N"
)

# ---- Combine all chart elements for the main box plot ----
# Layer the points on top of the boxplot
final_chart = (base_boxplot + point_layer + annotations + arrow_annotation + emoji_annotation).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    titleFontSize=14,
    labelFontSize=12
)

# ---- Scatter Plot for Individual Bacteria MICs (kept as a separate detailed view) ----
individual_mic_chart = alt.Chart(melted_df).mark_circle(size=60, opacity=0.7).encode(
    x=alt.X("Antibiotic:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL, log scale)"),
    color=alt.Color(
        "Gram_Staining:N",
        scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),
        legend=alt.Legend(title="Gram Staining")
    ),
    tooltip=[
        alt.Tooltip("Bacteria:N", title="Bacterium"),
        alt.Tooltip("Antibiotic:N", title="Antibiotic"),
        alt.Tooltip("MIC:Q", title="MIC (µg/mL)", format=".3f"),
        alt.Tooltip("Gram_Staining:N", title="Gram Staining"),
        alt.Tooltip("Genus:N", title="Genus")
    ]
).properties(
    title="Individual Bacteria MIC Values"
).interactive() # Allows zooming and panning


# ---- Streamlit App Layout ----
st.title("Antibiotic Effectiveness by Gram Staining")
st.markdown("**Lower MIC = More Effective** - Penicillin shows reduced effectiveness against Gram-negative bacteria.")

# Display the main chart
st.altair_chart(final_chart, use_container_width=True)

# Add explanation for the main chart
st.markdown("""
### Key Observations (Box Plot):
- **Penicillin** is highly effective against Gram-positive bacteria (low MIC values) but much less effective against Gram-negative bacteria (high MIC values).
- **Neomycin** and **Streptomycin** show more consistent effectiveness across both Gram types.
- The outer membrane of Gram-negative bacteria makes them naturally resistant to Penicillin.
""")

st.markdown("---") # Separator

st.subheader("Detailed View: Individual Bacteria MICs")
st.markdown("Hover over points for details. You can zoom and pan this chart.")
st.altair_chart(individual_mic_chart, use_container_width=True)

# Add explanation for the new chart
st.markdown("""
### Understanding the Individual MICs Chart:
This scatter plot shows the Minimum Inhibitory Concentration (MIC) for each specific bacterium against the three antibiotics. Each circle represents a single bacterium's response to an antibiotic.
- **Hover** over any circle to see the exact bacterium name, antibiotic, MIC value, Gram staining, and genus.
- This view helps to identify individual bacteria that might be particularly sensitive or resistant, even within a group.
""")


