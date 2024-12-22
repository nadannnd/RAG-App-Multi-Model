Usage
=====

The **RAG-App-Multi-Model** provides an intuitive interface for interacting with your PDF documents. Below are detailed steps on how to use the application.

Getting Started:
----------------

1. **Upload a PDF**:
   - On the sidebar, locate the **Upload Your PDF** section.
   - Click the "Choose File" button and upload your desired PDF.

2. **Select an AI Model**:
   - From the dropdown menu in the sidebar, select an AI model (e.g., `Llama2`, `Mistral`, or `Gemma`).
   - Each model has unique strengths—choose the one that fits your needs.

3. **Process the PDF**:
   - Click the **Process PDF** button.
   - The application will vectorize and process the uploaded document, preparing it for queries.

4. **Ask a Question**:
   - In the main interface, type a question related to the PDF content in the text input box.
   - Example: "What are the key findings in this document?"

5. **Review Responses**:
   - The AI model will generate a response based on your query.
   - If sources are available, expand the **View Sources** section to see which parts of the document were used.

Advanced Options:
-----------------

- **Custom Model Configuration**:
  - Modify the model's temperature or context size by adjusting the `OllamaLLM` settings in the code.

- **Inspect Vector Data**:
  - View how the document is split and stored by exploring the vectorized data in the backend.

Tips for Best Results:
----------------------

- Use specific and concise queries for better responses.
- Ensure the PDF is not password-protected or corrupted.
- Test different models to find the one most suited for your document type.

Next Steps:
-----------

Explore additional capabilities, such as:
- Integrating new AI models
- Enhancing the user interface
- Adding support for more file formats
