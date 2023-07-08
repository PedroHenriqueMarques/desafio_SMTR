# Challenge SMTR

This challenge consists in creating a data pipeline for occurrences mitigation. The data pipeline reads data from [API Dados Rio](https://api.dados.rio/docs/) and generates a csv file output with:
 * datetime: When the request was made;
 * tipo_ocorrencia: The type of occurrence that was created;
 * status_ocorrencia: The status of the occurrence when the request was made; and
 * quantidade_ocorrencia: How many occurrences of each type and status were observed.

The pipeline is as follows.
 * A HTTP request is made to get the open occurrences from the API;
 * For each occurrence id, another request is made to get the agencies involved with the occurence;
 * The data is merged, in order to compare what agencies are involved with the occurences;
 * The data is filtered to show only occurrences handled by CET-RIO;
 * A group by operation is done to count how many status there are for each occurrence type;
 * The request datetime is added to the report;
 * The report is exported as 'report.csv'.


## Installation

Clone this repo to your machine.
Then, go to the directory it was cloned to.
Open a terminal instance on the directory.

### Docker

If you have Docker installed, use:

```bash
docker build --no-cache -t smtr_challenge . 
```
If you are using an unix-based terminal:

```bash
docker run -v "$(pwd)":/app/exports smtr_challenge 
#or
docker run -v /path/to/file/docker_export:/app/exports smtr_challenge 
```
Or, in a windows:
```powershell
docker run -v ${PWD}:/app/exports smtr_challenge 
# or
docker run -v "C:\path\to\file\docker_export:/app/exports smtr_challenge 
```
### Virtual environment
If you only have a python installation:
 * Install virtualenv package

Unix:
```bash
python3 -m pip install --user virtualenv
virtualenv smtr_venv
source smtr_venv/bin/activate
python3 app.py
deactivate
```
Windows:
```powershell
python -m pip install --user virtualenv
virtualenv smtr_venv
.\smtr_venv\Scripts\activate
python app.py
deactivate
```
