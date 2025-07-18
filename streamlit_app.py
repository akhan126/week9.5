import pandas as pd
import altair as alt
import streamlit as st

# --- 1. Data Loading and Preparation ---
# Since no specific data was provided, I'm creating a sample DataFrame
# that matches your description. In a real Streamlit app, you would
# load your data here (e.g., from a CSV, Excel, or database).
@st.cache_data
def load_data():
    data = {
        'Bacterial_Species': [
            'Staphylococcus aureus', 'Streptococcus pyogenes', 'Enterococcus faecalis', 'Listeria monocytogenes',
            'Bacillus subtilis', 'Clostridium perfringens', 'Mycobacterium tuberculosis', 'Nocardia asteroides',
            'Escherichia coli', 'Pseudomonas aeruginosa', 'Klebsiella pneumoniae', 'Salmonella enterica',
            'Shigella flexneri', 'Proteus mirabilis', 'Haemophilus influenzae', 'Neisseria gonorrhoeae'
        ],
        'Gram_Staining': [
            'Gram-positive', 'Gram-positive', 'Gram-positive', 'Gram-positive',
            'Gram-positive', 'Gram-positive', 'Gram-positive', 'Gram-positive',
            'Gram-negative', 'Gram-negative', 'Gram-negative', 'Gram-negative',
            'Gram-negative', 'Gram-negative', 'Gram-negative', 'Gram-negative'
        ],
        'Genus': [ # Added Genus column for the new chart's melting
            'Staphylococcus', 'Streptococcus', 'Enterococcus', 'Listeria',
            'Bacillus', 'Clostridium', 'Mycobacterium', 'Nocardia',
            'Escherichia', 'Pseudomonas', 'Klebsiella', 'Salmonella',
            'Shigella', 'Proteus', 'Haemophilus', 'Neisseria'
        ],
        'Penicillin': [0.01, 0.005, 16, 0.5, 0.05, 0.1, 10, 2, 128, 256, 64, 32, 16, 8, 4, 2],
        'Streptomycin': [0.5, 0.25, 8, 1, 0.1, 0.2, 5, 1, 16, 32, 8, 4, 2, 1, 0.5, 0.25],
        'Neomycin': [1, 0.5, 4, 2, 0.2, 0.4, 2, 0.5, 8, 16, 4, 2, 1, 0.5, 0.25, 0.125]
    }
    df = pd.DataFrame(data)

    # Melt the DataFrame to a long format, which is ideal for Altair.
    # This creates 'Antibiotic' and 'MIC' columns from the individual antibiotic columns.
    # Updated id_vars to include 'Genus' as per the user's provided chart code
    df_melted = df.melt(
        id_vars=['Bacterial_Species', 'Gram_Staining', 'Genus'],
        value_vars=['Penicillin', 'Streptomycin', 'Neomycin'],
        var_name='Antibiotic',
        value_name='MIC'
    )
    return df_melted

df_mic = load_data()

# --- 2. Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Antibiotic Effectiveness Analysis")

st.title("🔬 Antibiotic Effectiveness Analysis")
st.markdown("""
This page visualizes the Minimum Inhibitory Concentration (MIC) of three antibiotics
(Penicillin, Streptomycin, Neomycin) against various bacterial species,
categorized by Gram staining. A lower MIC indicates higher effectiveness.
""")

# Display a snippet of the data
st.subheader("Raw Data Snippet")
st.dataframe(df_mic.head())

# --- 3. Altair Visualizations ---

st.subheader("Mean MIC of Antibiotics by Gram Staining")
st.markdown("""
This bar chart shows the average MIC for each antibiotic,
separated by Gram-positive and Gram-negative bacteria.
A lower bar indicates, on average, higher effectiveness.
""")

# Chart 1: Mean MIC Bar Chart
# Shows the average MIC for each antibiotic, broken down by Gram Staining.
mean_mic_chart = alt.Chart(df_mic).mark_bar().encode(
    # X-axis: Antibiotic type
    x=alt.X('Antibiotic:N', title='Antibiotic Type', axis=alt.Axis(labelAngle=-45)),
    # Y-axis: Mean MIC, with a logarithmic scale for better visualization of wide ranges
    y=alt.Y('mean(MIC):Q', title='Mean MIC (Log Scale)', scale=alt.Scale(type="log")),
    # Color bars by Gram Staining
    color=alt.Color('Gram_Staining:N', title='Gram Staining',
                    scale=alt.Scale(range=['#1f77b4', '#ff7f0e'])), # Custom colors for clarity
    # Tooltip to show details on hover
    tooltip=[
        alt.Tooltip('Antibiotic:N', title='Antibiotic'),
        alt.Tooltip('Gram_Staining:N', title='Gram Staining'),
        alt.Tooltip('mean(MIC):Q', title='Mean MIC', format='.2f') # Format mean MIC to 2 decimal places
    ]
).properties(
    title='Average Minimum Inhibitory Concentration (MIC) by Antibiotic and Gram Staining'
).interactive() # Enable zooming and panning

st.altair_chart(mean_mic_chart, use_container_width=True)


st.subheader("Individual MIC Values by Antibiotic and Gram Staining")
st.markdown("""
This scatter plot shows the MIC for each individual bacterial species.
Points are colored by antibiotic and shaped by Gram staining,
and the chart is faceted to compare Gram-positive and Gram-negative bacteria side-by-side.
""")

# Chart 2: Individual MIC Values Scatter Plot
# Shows each individual MIC value, faceted by Gram Staining.
individual_mic_chart = alt.Chart(df_mic).mark_point(filled=True, size=100, opacity=0.7).encode(
    # X-axis: Antibiotic type
    x=alt.X('Antibiotic:N', title='Antibiotic Type', axis=alt.Axis(labelAngle=-45)),
    # Y-axis: Individual MIC values, with a logarithmic scale
    y=alt.Y('MIC:Q', title='Minimum Inhibitory Concentration (MIC) (Log Scale)', scale=alt.Scale(type="log")),
    # Color points by Antibiotic
    color=alt.Color('Antibiotic:N', legend=alt.Legend(title="Antibiotic Type"),
                    scale=alt.Scale(range=['#e41a1c', '#377eb8', '#4daf4a'])), # Custom colors
    # Shape points by Gram Staining
    shape=alt.Shape('Gram_Staining:N', legend=alt.Legend(title="Gram Staining")),
    # Tooltip to show all relevant details on hover
    tooltip=['Bacterial_Species:N', 'Gram_Staining:N', 'Antibiotic:N', 'MIC:Q']
).properties(
    title='Individual MIC Values by Antibiotic and Gram Staining'
).facet(
    # Facet the chart by Gram Staining, creating separate columns for each category
    column=alt.Column('Gram_Staining:N', header=alt.Header(titleOrient="bottom", labelOrient="bottom"), title="Gram Staining")
).interactive() # Enable zooming and panning

st.altair_chart(individual_mic_chart, use_container_width=True)


st.subheader("MIC Distribution (Boxplot) by Antibiotic and Gram Staining")
st.markdown("""
This boxplot visualizes the distribution of MIC values for each antibiotic,
further broken down by Gram staining. The box represents the interquartile range (IQR),
the line inside is the median, and the whiskers extend to the min/max values within 1.5 IQR.
""")

# Chart 3: Boxplot of MIC values
# Using the melted_df (which is df_mic in this context)
mic_boxplot_chart = alt.Chart(df_mic).mark_boxplot(extent='min-max', size=30).encode(
    x=alt.X("Antibiotic:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL, log scale)"),
    color=alt.Color(
        "Gram_Staining:N",
        scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),
        legend=alt.Legend(title="Gram Staining")
    ),
    tooltip=["Antibiotic", "Gram_Staining", alt.Tooltip("median(MIC):Q", title="Median MIC")]
).properties(
    title='MIC Distribution by Antibiotic and Gram Staining'
).interactive() # Enable zooming and panning

# Annotation (optional, as provided by the user)
# Note: This annotation is specific to Penicillin and a very low MIC.
# It might not apply universally to all datasets or interpretations.
annotations = alt.Chart(pd.DataFrame({
    "Antibiotic": ["Penicillin"],
    "MIC": [0.001], # This MIC value is illustrative and might need adjustment based on real data
    "text": ["Gram-positive sensitive"]
})).mark_text(
    align="left", dx=5, dy=-10, fontSize=10, color="#ff7f0e"
).encode(
    x="Antibiotic:N",
    y="MIC:Q",
    text="text:N"
)

# Combine the boxplot with the annotation
final_boxplot_chart = mic_boxplot_chart + annotations

st.altair_chart(final_boxplot_chart, use_container_width=True)


st.subheader("Key Insights from the Data:")
st.markdown("""
Based on the sample data:
* **Penicillin** appears to be highly effective against most Gram-positive bacteria (low MICs), but significantly less effective against Gram-negative bacteria (very high MICs). The boxplot clearly shows the vast difference in MIC ranges for Penicillin between the two Gram staining categories.
* **Streptomycin** and **Neomycin** show a broader spectrum of activity compared to Penicillin, with varying effectiveness across both Gram-positive and Gram-negative species. However, their MICs against Gram-negative bacteria are generally higher than their effectiveness against Gram-positive ones, though not as stark as Penicillin.
* There are clear differences in MIC values even within the same Gram staining category, highlighting species-specific variations in antibiotic susceptibility. For instance, *Enterococcus faecalis* shows a high MIC for Penicillin even though it's Gram-positive. The boxplots help visualize the spread and outliers within each group.

**Narrative**: The data strongly suggests that **Gram staining is a critical factor in predicting antibiotic effectiveness, particularly for Penicillin.** While Penicillin is highly potent against Gram-positive bacteria, its utility against Gram-negative bacteria is severely limited. Streptomycin and Neomycin demonstrate a more balanced, albeit still varied, performance across both Gram categories. This underscores the importance of Gram staining in guiding initial antibiotic choices in clinical settings. The boxplots further emphasize the distribution and variability of MICs within these categories.
""")
