Installation
============

Follow these steps to set up the **RAG-App-Multi-Model** on your system.

Prerequisites:
--------------

- Python 3.8 or higher
- Pip (Python package manager)
- Streamlit
- Other dependencies listed in the `requirements.txt` file

Step 1: Clone the Repository
----------------------------

Start by cloning the project repository to your local machine. Use the following command:

.. code-block:: bash

    git clone https://github.com/nadannnd/RAG-App-Multi-Model.git

Navigate to the project directory:

.. code-block:: bash

    cd local-pdf-chat-assistant

Step 2: Install Dependencies
----------------------------

Install all the required dependencies using the `requirements.txt` file:

.. code-block:: bash

    pip install -r requirements.txt

This will install Streamlit, LangChain, and other necessary libraries.

Step 3: Run the Application
---------------------------

Start the Streamlit application by executing the following command:

.. code-block:: bash

    streamlit run app.py

The application will open in your default web browser at `http://localhost:8501`.

Step 4: Configure the AI Model
------------------------------

Ensure that the AI model (e.g., Llama2, Mistral) is correctly set up and accessible. This application connects to the AI models via the specified `base_url`.

Step 5: Upload Your PDF
-----------------------

Once the application is running, upload a PDF document and start querying its contents!

Troubleshooting:
----------------

- **Dependency Issues**: If you encounter errors during dependency installation, ensure you are using the correct Python version (3.8 or higher).
- **AI Model Configuration**: Verify that the AI model server is running and accessible at the `base_url`.
- **Firewall/Network Issues**: Ensure there are no restrictions on accessing `localhost`.

