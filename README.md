# 🎌 Anime Recommender System

An AI-powered anime recommendation engine leveraging **Retrieval Augmented Generation (RAG)** to deliver highly personalized and accurate suggestions. Built with a modern tech stack including **FastAPI**, **Streamlit**, **LangChain**, and **Azure OpenAI**.

## 🏗️ End-to-End Architecture

The following diagram illustrates the complete system workflow, from data ingestion to user inference:

![End-to-End Architecture](images/architecture_diagram_e2e.svg)

## 🚀 Key Features

- **AI-Powered Recommendations**: Utilizes advanced LLMs to understand complex user preferences and nuances.
- **Semantic Search**: Goes beyond keyword matching to understand the intent and context of the user's request.
- **Modern UI**: A responsive and visually appealing interface built with Streamlit.
- **Scalable API**: High-performance FastAPI backend designed for production environments.
- **Containerized & Cloud-Ready**: Fully Dockerized and ready for deployment on Kubernetes (AKS).

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **Frontend**: Streamlit
- **Backend**: FastAPI, Uvicorn
- **AI/ML Framework**: LangChain
- **LLM Provider**: Azure OpenAI (GPT-4)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers
- **DevOps**: Docker, Kubernetes (AKS)

## 💡 Technical Architecture & Design Decisions

This project is built on a robust stack designed for scalability, maintainability, and AI performance. Here is the rationale behind our key technical choices:

### 1. Retrieval Augmented Generation (RAG) & Retrieval Chains

We utilize a **Retrieval Chain** architecture instead of a standard LLM call or fine-tuning for several critical reasons:

- **Reduced Hallucinations**: By grounding the LLM's responses in retrieved context (our anime dataset), we significantly reduce the risk of the model inventing non-existent anime or details.
- **Context Awareness**: The retrieval chain dynamically fetches the most relevant anime data based on the semantic meaning of the user's query, allowing for highly specific recommendations (e.g., "anime like Attack on Titan but with more comedy").
- **Extensibility**: The knowledge base can be updated simply by adding documents to the vector store without needing to retrain or fine-tune the model.

### 2. FastAPI Backend

- **Asynchronous Performance**: FastAPI's `async` capabilities allow for handling multiple concurrent requests efficiently, which is crucial when dealing with potentially long-running AI inference tasks.
- **Type Safety & Validation**: Pydantic models ensure that data flowing in and out of the API is strictly validated, reducing runtime errors.
- **Auto-Documentation**: Automatic generation of Swagger UI (OpenAPI) makes testing and integration seamless.

### 3. Streamlit Frontend

- **Rapid Development**: Streamlit allows for building a professional, interactive data-driven UI in pure Python without needing a separate frontend team.
- **Interactive Components**: Built-in support for chat interfaces and data visualization makes it perfect for AI demos.

### 4. ChromaDB (Vector Store)

- **Efficiency**: A lightweight, high-performance vector database optimized for storing and retrieving embeddings.
- **Flexibility**: Works excellently in both local development (embedded mode) and production server environments.

### 5. Azure OpenAI

- **Enterprise Reliability**: Provides the power of GPT-4 with the security, compliance, and SLA guarantees of the Azure cloud platform.

## 📡 API Schema

This section defines the API contract between the FastAPI backend and frontend applications. All API interactions follow these schemas for type safety and consistency.

### Request/Response Models

#### RecommendationRequest

```json
{
  "query": "string"
}
```

**Fields:**

- `query` (string, required): User's anime preference description in natural language

**Example:**

```json
{
  "query": "Saya suka anime action dengan cerita menarik seperti Attack on Titan"
}
```

#### RecommendationResponse

```json
{
  "query": "string",
  "recommendation": "string",
  "status": "success"
}
```

**Fields:**

- `query` (string): The original user query
- `recommendation` (string): AI-generated anime recommendations
- `status` (string): Response status (default: "success")

**Example:**

```json
{
  "query": "Saya suka anime action dengan cerita menarik seperti Attack on Titan",
  "recommendation": "Berdasarkan preferensi Anda, berikut adalah rekomendasi anime action dengan plot twist menarik:\n\n1. **Shingeki no Kyojin (Attack on Titan)**\n   - Ringkasan: Dalam dunia di mana manusia hidup di dalam tembok untuk melindungi diri dari raksasa pemakan manusia, Eren Yeager bergabung dengan pasukan penjelajah untuk membalas dendam.\n   - Alasan: Anime ini memiliki elemen action intens, cerita mendalam tentang perang dan politik, serta plot twist yang tak terduga, sesuai dengan preferensi Anda.\n\n2. **Fullmetal Alchemist: Brotherhood**\n   - Ringkasan: Dua saudara yang kehilangan tubuh dan lengan masing-masing dalam ritual alkimia yang gagal, mencari Batu Filsuf untuk memperbaiki kesalahan mereka.\n   - Alasan: Anime ini menawarkan action yang epik, cerita yang kompleks dengan tema pengorbanan dan moralitas, serta plot twist yang memukau.\n\n3. **Code Geass**\n   - Ringkasan: Lelaki muda mendapatkan kekuatan untuk memerintah orang lain, dan ia menggunakan kemampuan tersebut untuk memimpin pemberontakan melawan Kekaisaran Britannia.\n   - Alasan: Dengan kombinasi strategi militer, politik, dan plot twist yang cerdas, anime ini cocok untuk penggemar cerita action yang mendalam.",
  "status": "success"
}
```

### API Endpoints

#### 1. Root Endpoint

**GET /**

Health check and API information endpoint.

**Response:**

```json
{
  "message": "Selamat datang di Anime Recommender API!",
  "status": "active",
  "docs": "/docs"
}
```

#### 2. Health Check

**GET /health**

Check API and pipeline status.

**Response:**

```json
{
  "status": "healthy",
  "pipeline_loaded": true
}
```

#### 3. Get Recommendation

**POST /recommend**

Generate anime recommendations based on user preferences.

**Request Body:** `RecommendationRequest`

**Response:** `RecommendationResponse`

**Error Responses:**

- `503 Service Unavailable`: Pipeline not initialized
- `500 Internal Server Error`: Recommendation generation failed

**Example Request:**

```bash
curl -X POST "http://localhost:8000/recommend" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Anime action dengan plot twist menarik"
     }'
```

**Example Response:**

```json
{
  "query": "Anime action dengan plot twist menarik",
  "recommendation": "Berdasarkan preferensi Anda...",
  "status": "success"
}
```

### OpenAPI Specification

The complete API specification is automatically generated and available at `/docs` when the FastAPI server is running. This provides interactive documentation with the ability to test endpoints directly from the browser.

## 📦 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Azure OpenAI API Key & Endpoint
- Docker (optional, for containerization)

### 1. Local Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/username/anime-recommender.git
   cd anime-recommender
   ```
2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Configuration**
   Create a `.env` file in the root directory:

   ```env
   AZURE_OPENAI_APIKEY="your-api-key"
   AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
   ```
5. **Run the Application**

   *Terminal 1 (Backend):*

   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

   *Terminal 2 (Frontend):*

   ```bash
   streamlit run app/app.py
   ```

### 2. Running with Docker Compose

For a simplified local testing experience using containers:

```bash
docker-compose up --build
```

Access the application at `http://localhost:8501`.

### 3. Deployment to Azure Kubernetes Service (AKS)

Follow this end-to-end guide to deploy the application to the cloud.

#### Deployment Workflow

![Deployment Workflow](images/flow_deploy_azure.png)

#### Step-by-Step Deployment Guide

**Step 1: Prerequisites & Login**
Ensure you are logged into Azure CLI.

```bash
az login
```

**Step 2: Create Resources (One-time setup)**
Create a Resource Group and Container Registry.

```bash
# Create Resource Group
az group create --name azure_ai_apps --location southeastasia

# Create Azure Container Registry (ACR)
az acr create --resource-group azure_ai_apps --name airecommender01 --sku Basic --admin-enabled true
```

**Step 3: Build & Push Docker Image**
Build the image locally and push it to your private registry.

```bash
# Login to ACR
az acr login --name airecommender01

# Build Image (Replace 'v1' with your version tag)
docker build -t airecommender01.azurecr.io/anime-recommender:latest .

# Push Image to ACR
docker push airecommender01.azurecr.io/anime-recommender:latest
```

**Step 4: Create Kubernetes Cluster (AKS)**
Create a cluster and attach it to your ACR so it can pull images.

```bash
az aks create \
    --resource-group azure_ai_apps \
    --name AnimeCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr airecommender01

# Get cluster credentials
az aks get-credentials --resource-group azure_ai_apps --name AnimeCluster
```

**Step 5: Deploy Application**

1. **Update Manifests**: Open `k8s/backend.yaml` and `k8s/frontend.yaml` and replace the image name with your ACR image: `airecommender01.azurecr.io/anime-recommender:latest`.
2. **Configure Secrets**: Update `k8s/secrets.yaml` with your real Azure OpenAI keys.
3. **Apply Manifests**:
   ```bash
   kubectl apply -f k8s/secrets.yaml
   kubectl apply -f k8s/backend.yaml
   kubectl apply -f k8s/frontend.yaml
   ```

**Step 6: Verify Deployment**
Check if pods are running and get the external IP.

```bash
# Check Pod Status
kubectl get pods

# Get Frontend Public IP
kubectl get service anime-frontend-service --watch
```

Access the application using the `EXTERNAL-IP` provided by the service.

**Step 7: Setting up Monitoring (Prometheus & Grafana)**

We use a standard Kubernetes setup for monitoring without external dependencies.

1.  **Create Namespace**
    ```bash
    kubectl create namespace monitoring
    ```

2.  **Deploy Prometheus**
    ```bash
    kubectl apply -f monitoring/prometheus.yaml
    ```

3.  **Deploy Grafana**
    ```bash
    kubectl apply -f monitoring/grafana.yaml
    ```

4.  **Access Grafana Dashboard**
    ```bash
    # Get Grafana External IP
    kubectl get service grafana -n monitoring --watch
    ```
    - Open `http://<EXTERNAL-IP>:3000` in your browser.
    - Login with default credentials if configured, or setup data source pointing to `http://prometheus-service.monitoring.svc:8080`.

## 📂 Project Structure
    
```
.
├── api/                # FastAPI Backend Application
│   └── main.py         # API Endpoints and Logic
├── app/                # Streamlit Frontend Application
│   └── app.py          # UI Layout and Interactivity
├── config/             # Configuration Settings
├── k8s/                # Kubernetes Deployment Manifests
├── monitoring/         # Prometheus & Grafana Manifests
├── pipeline/           # LangChain Orchestration Pipeline
├── src/                # Core Logic (Recommender, Vector Store)
├── utils/              # Utility Functions (Logging, Exceptions)
├── .env                # Environment Variables (Not committed)
├── docker-compose.yaml # Docker Compose Configuration
├── Dockerfile          # Docker Build Instructions
└── requirements.txt    # Python Dependencies
```
