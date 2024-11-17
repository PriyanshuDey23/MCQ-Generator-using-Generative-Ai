import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from MCQ_Generator.utils import *
from MCQ_Generator.logger import logging
from MCQ_Generator.MCQGenerator import generate_evaluate_chain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader



# Loading Response json file
with open('Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

# Creating title for the app
st.title("MCQ Generator")

# Create a form 
with st.form('User_Input'):

    # File Upload
    uploaded_file=st.file_uploader("Upload a PDF or text file")

    # Input Fields
    mcq_count=st.number_input("Number of MCQs",min_value=3,max_value=50)

    # Subjects
    subject=st.text_input("Insert Subjects",max_chars=50)

    # Quiz Tone
    tone=st.text_input("Complexility level of Questions", max_chars=20,placeholder="Simple")

    # Add Button
    button=st.form_submit_button("Generate MCQs")

    # Check if the button is clicked and all filds have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text=read_file(uploaded_file)
                # Count Token and the cost of API Call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")

                if isinstance(response,dict):  # isinstance:- Returns true

                    # Extract Quiz from response
                    quiz=response.get("quiz",None)

                    # Remove the leading and trailing Markdown code block formatting (```json and ```)
                    quiz = quiz.strip().replace('```json', '').replace('```', '')

                    if quiz is not None:
                        table_data=get_table_data(quiz)

                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1 # Adjust index starting from 1
                            st.table(df) # Display the table in Streamlit

                            # Save the DataFrame to CSV file
                            csv_path = "data/quiz.csv"
                            df.to_csv(csv_path, index=False)  # Save to CSV without index
                            st.success(f"Quiz saved as {csv_path}")

                            
                            # Display the review in a text box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in table data")

                else:
                    st.write(response)









