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