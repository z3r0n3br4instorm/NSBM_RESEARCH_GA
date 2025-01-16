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