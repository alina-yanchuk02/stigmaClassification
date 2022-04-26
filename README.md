## Classification of stigmatizing articles of mental illness in portuguese online newspapers, with machine learning and natural language processing

This project consists of the automatic classification of articles stigmatizing mental illness in portuguese online newspapers, and the automatic detection of topics present in them. The official data source is the Arquivo.pt public repository.

Author: Alina Yanchuk - alinyanchuk@ua.pt - University of Aveiro

### Data Collection program

This program collects data (web pages referring to portuguese articles that portray the mental disorders of schizophrenia and psychosis) from public repository Arquivo.pt and performs web scraping. The result is a CSV file (data.csv) with structured relevant data. 
To execute, run: 

    pip install -r requirements.txt

    python3 collect_from_api.py 

### 1. Preprocessing

The Preprocessing stage is organized in a Jupyter Notebook, with the relevant steps described in the same. The data file used is the file returned in the Data Collection step (needs manual class annotation). Returns a data file for the Classification task and the Topic Modeling task and a data file for the final Exploratory Data Analysis task.
 
 Note: the data file in the directory (data_labeled.csv) is already manually labeled and also got some manual processing (after being returned in the Data Collection stage) to fully prepare it for the next steps.

### 2. Classification

The Classification stage is organized in 2 Jupyter Notebooks, with the relevant steps described in the same. The data file used is the file with the cleaned data returned in the Preprocessing step. The first Notebook has 5 traditional Machine Learning algorithms and 3 Deep Learning algorithms, their hyper-parameters tuning and evaluation metrics. The second Notebook has the implemention of BERT (BERTimbau - PT BERT) algorithm (placed in a separate Notebook due to organizational issues and differences in some steps).

Models implemented:

   - Logistic Regression
   - Linear SVC
   - Multinomial Naive Bayes
   - K-Nearest Neighbors
   - Random Forest
   - Convolutional Neural Network (with GloVe PT 300D)
   - Long Short-Term Memory (LSTM) (with GloVe PT 300D)
   - Bidirectional Long Short-Term Memory (Bi-LSTM) (with GloVe PT 300D)

   - BERTimbau

### 3. Topic Modeling

The Topic Modeling stage is organized in a Jupyter Notebook, with the relevant steps described in the same. The data file used is the file with the cleaned data returned in the Preprocessing step. 

### 4. Exploratory Data Analysis

The Exploratory Data Analysis stage is organized in a Jupyter Notebook, with the relevant steps described in the same. The data file used is the file with the cleaned and prepared (for EDA) data returned in the Preprocessing step. This step was done to obtain final insights about the data after automatic Classification and Topic Modeling. Can be adapated to other needs.


About Jupyter Notebooks: https://docs.jupyter.org/en/latest/
Arquivo.pt: https://arquivo.pt/