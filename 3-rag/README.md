# RAG (Retrieval-Augmented Generation) Workshop

## How to Run

1. Create a virtual environment in the `3-rag` folder:

   ```bash
   cd 3-rag
   ```

   ```bash
   python -m venv venv
   ```

   or

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys (we'll add MongoDB URI later):

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URI=your_mongodb_connection_string_here
   #OPTIONAL
   #SLACK_WEBHOOK=your-slack-webhook
   ```

5. Run the basic assistant with a simple logging tool:
   ```bash
   python assistant.py
   ```
   Type 'quit', 'exit', or 'bye' to stop the assistant.

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that combines:

- **Retrieval**: Finding relevant information from a knowledge base
- **Generation**: Using that information to create informed, contextual responses

Instead of relying solely on an AI model's training data (which can be outdated), RAG allows your AI to access and reason over current, domain-specific information stored in databases.

**Why RAG?**

- 🎯 **Accuracy**: Responses based on your actual data
- 🔄 **Up-to-date**: Information is as current as your database
- 📚 **Domain-specific**: Perfect for specialized knowledge bases
- 🔍 **Transparent**: You can see what sources were used

## Workshop Tasks

In this tutorial we will give our AI Assistant the ability to search our content, which is multiple police logs in Norway.

### Task 1: Set Up MongoDB Atlas and Load Police Data

Time to give your AI memory! We'll set up a free MongoDB Atlas database and load Norwegian police logs. 🗄️

**Your Mission:**
Create a MongoDB Atlas account, set up a database, and load the police log data.

**Steps:**

1. **Create MongoDB Atlas Account**

   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas) and sign up (free tier)
   - Follow all steps until you reach the dashboard
   - Create a new cluster (choose the FREE M0 option, all other fields can be left as is)
   - Wait for cluster creation to finish

2. **Set Up Access**

   - **Database Access**: Create a database user, copy and save the password for Step 3.
   - **Network Access**: Your current IP address should be automatically added, but if you want to access the database from any network you can change this in **Database and Network** access later.

3. **Get Connection String**

   - Click "Connect" → "Drivers" → "Python"
   - Copy the connection string to your .env file for the `MONGODB_URI`
   - If you see <password> in the string, replace it with the database user password you saved.

4. **Create Database and Collection**

   - In your Project Overview you should see your Cluster and a way to add data or browse collection, press on either one of those options.
   - You now want to create a new database. Select `Create Database on Atlas` or any button that says `Create dataabase`.
   - Database name: `whatever-name-you-want`, e.g. `my-db`
   - Collection name: The name of the collection, this is where we will add all our logs from "politiloggen". You can just call it `logs` or whatever you prefer.

5. **Load the Data**
   This tutorial includes a quick way to add the `politiloggen.json` data to your db. Since MongoDB is NoSQL document database, you can just drop in the whole JSON file within the atlas UI, but if you want to do this programatically you can use the the script provided.

   Open `db.py` and change the fields `<DATABASE_NAME>` and `COLLECTION_NAME` to config your database connection:

   ```python
   db = client['<DATABASE_NAME>']
   collection = db['<COLLECTION_NAME>']
   ```

   Now you can load in the politiloggen data to MongoDB using this script. It will call the `_add_documents_from_json()` function:

   ```bash
   python3 db.py
   ```

   You should see this this in the logs to confirm it works. Now you can refresh the Atlas UI

   ```
   Document added with ID: 68f6859efe9a45ff8ac21559
   Document added with ID: 68f6859efe9a45ff8ac2155a
   Document added with ID: 68f6859efe9a45ff8ac2155b
   Documents added from politiloggen.json
   ```

**Success Check:** You should now see all the policelog messages in your db! 🚓

**Resources:** [MongoDB Atlas Getting Started](https://www.mongodb.com/docs/atlas/getting-started/)

### Task 2: Create Text Embeddings

Now that you have police data in MongoDB, let's convert text into meaning! We'll convert text into numerical vectors (embeddings) that capture semantic meaning. 🧮

**Your Mission:**
Implement the `create_embedding()` function to transform text into embeddings using OpenAI's embedding model.

**What are Embeddings?**
Embeddings are lists of numbers that represent the meaning of text. Similar texts have similar embeddings, enabling "semantic search" - finding content by meaning rather than exact keywords.

**Steps:**

1. **Open the embedding.py file**
   You'll see a function that needs to be completed:

   ```python
   def create_embedding(text: str) -> list[float]:
       """Returns the embedding from the OpenAI API"""
       pass
   ```

2. **Implement the Function**
   Use OpenAI's `text-embedding-3-small` model to create embeddings. You'll find the docs for this (here)[https://platform.openai.com/docs/guides/embeddings].

3. **Test Your Function**
   The `embedding.py` file includes a quick test to print out the first 5 numbers in the vector by running:

   ```
   python3 embedding.py
   ```

**Success Check:** You should see:

- Embedding length: 1536
- First 5 values: [0.123, -0.456, 0.789, ...]

**Resources:** [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

### Task 3: Add Embeddings and Enable Vector Search

Time to make the data searchable by meaning! We'll add embeddings to documents and enable vector search. 🔍

**Your Mission:**
Add embeddings to each documents bases on the text in the messages and set up vector search capabilities.

**Steps:**

1. **Add Embeddings to Documents**
   Run the embedding function that's implemented in `db.py`, replace the `_add_documents_from_json` with `_add_embeddings_to_documents`.

   ```python
   _add_embeddings_to_documents()
   ```

   This will add embedding vectors to your documents (takes a few minutes).

2. **Set Up Vector Search Index**
   In MongoDB Atlas:
   - Go to your cluster → "Search" tab → "Create Search Index"
   - Use this configuration:
   ```json
   {
     "fields": [
       {
         "type": "vector",
         "path": "embedding",
         "numDimensions": 1536,
         "similarity": "cosine"
       }
     ]
   }
   ```
   - Name it `vector_index` and wait for it to become "Active"

**Success Check:** Documents now have `embedding` fields and your search index is active!

**Key Concept:** Each police log is now a 1536-dimensional vector. Similar incidents have similar vectors, enabling semantic search by meaning rather than keywords.

### Task 4: Implement Semantic Search

Now for the magic! Implement semantic search to find relevant police logs by meaning. 🔍

**Your Mission:**
Complete the `semantic_search()` function in `db.py`.

**Steps:**

1. **Implement the Function**

   ```python
   def semantic_search(query: str, limit: int = 5):
       """Search for relevant documents using vector search"""
       # TODO:
       # 1. Create embedding for the query
       # 2. Use MongoDB $vectorSearch to find similar documents
       # 3. Return the results
       pass
   ```

2. **Test Your Search**
   ```python
   # Test with: "Hva skjedde i Hamar sentrum?"
   results = semantic_search("Hva skjedde i Hamar sentrum?")
   ```

**Success Check:** Your search finds relevant documents even with different words than the original text!

### Task 5: Connect Search to Your AI Assistant

Now let's give your AI assistant the power to search through police logs! 🤖

**Your Mission:**
Add the semantic search function to your AI assistant so it can find relevant police data when needed.

**Steps:**

1. **Create the Search Tool Function**
   In `assistant.py`, replace the `print_to_console` function with the semantic_search function or rename it if want to.

2. **Update the Tool Configuration**
   Replace the existing tool with:

   ```python
   {
       "type": "function",
       "name": "semantic_search",
       "description": "Search through Norwegian police logs to find relevant incidents, crimes, or events. Use this when users ask about specific locations, types of incidents, or want information from police reports.",
       "parameters": {
           "type": "object",
           "properties": {
               "query": {
                   "type": "string",
                   "description": "The search query in Norwegian (e.g., 'trafikkulykker i Oslo', 'innbrudd i Gjøvik', 'Brann på Hamar')"
               }
           },
           "required": ["query"],
           "additionalProperties": False,
       },
       "strict": True,
   }
   ```

3. **Update the Tool Lookup**

   ```python
   tool_lookup = {
       "semantic_search": semantic_search
   }
   ```

4. **Test Your RAG Assistant**
   Try asking:
   - "Hva skjedde i Kristiansand i dag?"
   - "Tell me about traffic accidents"
   - "Any incidents in city centers?"

**Success Check:** Your AI assistant now searches police logs and provides relevant information based on the data!

## Congratulations! 🎉

This is a basic RAG solution with functions. RAG has many techniques and optimizations we can implement to make it even better, but you now understand the core concepts of Retrieval-Augmented Generation, and giving your AI Assistant the option to use it when it needs to!
