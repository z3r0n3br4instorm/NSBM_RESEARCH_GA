# NSBM_RESEARCH_GA

## Setting up

> Setting up ollama
Install ollama

For Linux :
```
curl -fsSL https://ollama.com/install.sh | sh
```
For Windows :
Visit this site and download the latest version
https://ollama.com/download/windows

An NVIDIA CUDA or AMD ROCm Capable GPU with <4GB VRAM is recommended for optimal performance.
For NVIDIA Cards, Download CUDA toolkit from here
https://developer.nvidia.com/cuda-toolkit

For AMD Cards, ROCm tookit can be found in here
https://www.amd.com/en/products/software/rocm.html


> Setting up and running the Project

1. Install all the requirements
```
pip install -r requirements.txt
```
2. Install the spacy model
```
python -m spacy download en_core_web_sm
```
3. Create Local Database
```
python createLocalDemoDB.py
```
4. Run the program
```
python main.py
```

## Usage

System is currently capable of answering questions related to the following topics accurately using RAG:
```python
topics = [
        "distributed_systems",
        "networking",
        "cloud_computing",
        "databases",
        "nsbm",
    ]
```
To clear session's context, type `clear` and press enter.
To do a websearch with RAG, type `/search <your search query>`
