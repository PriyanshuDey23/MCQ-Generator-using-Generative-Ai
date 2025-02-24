import os
import json
import pandas as pd
import traceback
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from MCQ_Generator.utils import read_file, get_table_data
from MCQ_Generator.MCQGenerator import generate_evaluate_chain




# Loading Response json file
with open('Response.json','r') as file:
    RESPONSE_JSON=json.load(file)




# Title & Description
st.set_page_config(page_title="MCQ Generator", layout="wide")
st.title("📝 MCQ Generator")
st.markdown("Generate multiple-choice questions from uploaded documents effortlessly.")

# Create a form with a modern layout
with st.form('User_Input'):
    
    # Create columns for better UI alignment
    col1, col2 = st.columns(2)

    # File Upload
    uploaded_file = st.file_uploader("📂 Upload a PDF or text file", type=["pdf", "txt"], help="Supported formats: PDF, TXT")

    # Input Fields in columns
    with col1:
        mcq_count = st.number_input("🔢 Number of MCQs", min_value=3, max_value=50, help="Select the number of MCQs to generate.")
        subject = st.text_input("📚 Subject", max_chars=50, placeholder="e.g., Mathematics, Science")
    
    with col2:
        tone = st.selectbox("🎯 Complexity Level", ["Simple", "Intermediate", "Advanced"], help="Choose the difficulty level.")

    # Generate Button
    button = st.form_submit_button("🚀 Generate MCQs")

# Check if button is clicked and required inputs are provided
if button:
    if uploaded_file is None:
        st.warning("⚠️ Please upload a file to proceed.")
    elif not subject:
        st.warning("⚠️ Please enter a subject.")
    else:
        with st.spinner("⏳ Generating MCQs... Please wait."):

            try:
                # Read uploaded file
                text = read_file(uploaded_file) 

                # Call OpenAI API
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

            except Exception as e:
                st.error("❌ An error occurred while generating MCQs.")
                st.error(f"Error Details: {str(e)}")
                traceback.print_exc()
            else:
                # Debugging logs
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", "").strip().replace('```json', '').replace('```', '')

                    if quiz:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1  # Start index from 1
                            
                            # Display the MCQs as a table
                            st.subheader("📊 Generated MCQs")
                            st.dataframe(df, use_container_width=True)

                            # Save as CSV
                            csv_path = "data/quiz.csv"
                            df.to_csv(csv_path, index=False)
                            st.success(f"✅ Quiz saved as `{csv_path}`")

                            # Expandable review section
                            with st.expander("📄 Review MCQs"):
                                st.text_area(label="Review", value=response.get("review", "No review available."), height=200)

                        else:
                            st.error("⚠️ Error processing table data.")
                    else:
                        st.warning("⚠️ No quiz data found.")
                else:
                    st.write(response)









