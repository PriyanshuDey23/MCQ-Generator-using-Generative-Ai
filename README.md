
# MCQ Generator using Generative AI

This project is a web-based application built using **Streamlit** to generate multiple-choice questions (MCQs) from text-based content like PDFs or TXT files. The application utilizes **Generative AI** for intelligent MCQ creation, making it easy to generate customized quizzes on various subjects.

## Features
- Upload PDF or Text files to extract content
- Generate MCQs based on the extracted text
- Customize MCQ generation with options like the number of questions, subject, and tone (complexity level)
- Real-time display of the generated quiz
- Option to download the quiz as a CSV file



```bash
pip install -r requirements.txt
```

Alternatively, you can install the package directly using:

```bash
pip install -e .
```

## Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/PriyanshuDey23/MCQ-Generator-using-Generative-Ai.git
    cd mcq-generator
    ```

2. **Create a Virtual Environment**:
    In the project directory, create a virtual environment. You can name it something like `env`:

    ```bash
    virtualenv env
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:
    - Create a `.env` file in the root of the project directory.
    - Add necessary API keys and configurations (e.g., OpenAI API keys, Google Cloud API credentials).

    Example `.env` file:
    ```env
    GOOGLE_API_KEY=your-google-api-key
    ```

5. Run the application:
    ```bash
    streamlit run app.py
    ```

This will start the app locally, and you can access it in your browser at `http://localhost:8080`.

## Usage

1. Upload a PDF or TXT file using the file uploader.
2. Input the desired number of MCQs, subject, and tone (complexity level).
3. Click "Generate MCQs" to generate the quiz based on the uploaded content.
4. The generated MCQs will be displayed in a table, and you can also see a review.
5. Optionally, download the quiz as a CSV file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses **Generative AI** technologies such as **OpenAI** and **Google Cloud** for text-based content generation.
- **Streamlit** is used to build the interactive frontend of the application.
- **LangChain** and **LangChain Community** are utilized for chain processing and integrating AI models.
