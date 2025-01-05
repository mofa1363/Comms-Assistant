import streamlit as st
from openai import ChatCompletion

# OpenAI API Key
openai_api_key = st.secrets["openai_api_key"]

# Function to interact with GPT
@st.cache(allow_output_mutation=True)
def interact_with_gpt(prompt):
    completion = ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return completion['choices'][0]['message']['content']

# App Layout
st.title("Notification Assistant")
st.write("This assistant will help you determine who to notify when a person is appointed to a new role in your company.")

# Step 1: Business Unit (BU)
bu = st.selectbox("What is the Business Unit (BU) for this role?", ["Finance", "Sales", "CT", "Corporate", "Shipping", "HR"])

# Step 2: Level of Communication BU-wise
bu_level = st.selectbox(
    "What is the level of communication BU-wise?",
    ["Inter-Team", "BU", "Inter-BU", "Company-wide"]
)

if bu_level == "Inter-Team":
    teams = st.text_input("Which teams inside the BU should be informed? (comma-separated)")

if bu_level == "Inter-BU":
    bus_to_notify = st.text_input("Which BUs should be informed? (comma-separated)")

# Step 3: Role Location
location = st.selectbox(
    "What is the role's location?",
    ["HC (Headquarters)", "UAE", "India", "China", "Singapore", "R (Rest of the world)"]
)

# Step 4: Domain of Communication Based on Location
location_domain = st.selectbox(
    "What is the domain of communication based on location?",
    ["Inside Employee's Location", "Inter-Location", "Global"]
)

if location_domain == "Inter-Location":
    locations_to_notify = st.text_input("Which other locations should be informed? (comma-separated)")

# Step 5: Entity
entity = st.text_input("What is the name of the company or entity for this role?")

# Step 6: Level of Communication Entity-wise
entity_level = st.selectbox(
    "What is the level of communication entity-wise?",
    ["Inside Employee's Entity", "Inter-Entity", "All Entities"]
)

if entity_level == "Inter-Entity":
    entities_to_notify = st.text_input("Which other entities should be informed? (comma-separated)")

# Generate Notification Guide
if st.button("Generate Notification Guide"):
    prompt = f"You should notify {bu} BU of {entity} in {location}, along with: \n"
    prompt += "- HRBP for All BUs\n"
    prompt += "- All HR Managers across all locations\n"
    prompt += "- All HRSS teams across all locations\n"
    prompt += "- CHRO\n"
    prompt += f"- VP of {bu}"

    if bu_level == "Company-wide":
        prompt = f"You should notify Everyone of {entity} in {location}, along with:\n"
        prompt += "- HRBP for All BUs\n"
        prompt += "- All HR Managers across all locations\n"
        prompt += "- All HRSS teams across all locations\n"
        prompt += "- CHRO\n"
        prompt += "- VP of All BUs"

    if entity_level == "All Entities":
        prompt = prompt.replace(f"of {entity}", "")

    result = interact_with_gpt(prompt)
    st.write("### Final Notification Guide:")
    st.write(result)
