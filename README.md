# **LLM Based JS Code Generator**
## **Project description**
In this project I have developed a LangChain agent that generates Node.js code based on user description of a function. The agent can search google and stackoverflow for information in case the LLM can't generate the necessary code on its own. The interaction with the agent occurs through 2 endpoints.
## **API Endpoints**
### **GET**
- [/api/list_functions/](#get-apilist_functions)
### **POST**
- [/api/generate/](#post-apigenerate)
- [/api/test/](#post-apitest)
### **GET /api/list_functions/**
Lists all fucntion names and their ids present in the database. Doesn't accept any parameters.
#### **Example**
#### Response
```
[
    {
        "id": 1,
        "function_name": "concatenateStrings"
    },
    {
        "id": 2,
        "function_name": "sumTwoDigits"
    },
    {
        "id": 3,
        "function_name": "randomNumber"
    },
    {
        "id": 4,
        "function_name": "square"
    },
    {
        "id": 5,
        "function_name": "countCharacters"
    },
    {
        "id": 6,
        "function_name": "countNumInList"
    },
    {
        "id": 7,
        "function_name": "getZeroIndeces"
    }
]
```
### **POST /api/generate/**
Receives the description of a function from a user and test parameters if necessary to input into the generated function during its verification. If the function doesn't throw an error during execution, it gets saved and its id is returned in the response.
#### **Parameters**
|Name|Required|Type|Description|
|---|---|---|---|
|description|required|string|The description of the function that the agent will try to generate|
|test_parameters|required|list|list of test parameters that will be passed into the generated function for verification. If the function doesn't accept any input parameters then leave the list empty|
#### **Example**
#### Call parameters
```
{
    "description" : "Write a function that receives a list of numbers and outputs a list of indeces of zeros",
    "test_parameters" : [[1,2,0,4,5,0,1,2,3,1,0,1]]
}
```
#### Response
```
{
    "id": 7
}
```
### **POST /api/test/**
Receives the id of the function and parameters that will be passed into it. After the function is executed, its result will be returned in the response.
#### **Parameters**
|Name|Required|Type|Description|
|---|---|---|---|
|id|required|int|id of the function to call|
|parameters|required|list|parameters that will be passed into the function during its execution. If the function doesn't accept any inputs then leave the list empty
#### **Example**
#### Call parameters
```
{
    "id" : 7,
    "parameters" : [[1,2,0,4,5,0,1,2,0,1,0,1]]
}
```
#### Response
```
{
    "result": [
        2,
        5,
        8,
        10
    ]
}
```
## **How to run the project**
First download the project:
```
git clone https://github.com/Dmytro-Kovalyov/LLM-Based-JS-Code-Generator.git
```
### **Docker**
The easiest way to run the project is using Docker.

Input your api keys in ```docker-compose.yml``` file
```
environment:
    - "DEBUG=1"
    - "OPENAI_API_KEY=<OPENAI_API_KEY>"
    - "SERPAPI_API_KEY=<SERPAPI_API_KEY>"
    - "STACKOVERFLOW_API_KEY=<STACKOVERFLOW_API_KEY>"
```
Then build the image:
```
sudo docker-compose build
```
Now you can run it:
```
sudo docker-compose up -d
```
### **Running natively**
If you want to run this project natively there are several steps necessary to take:
- download [python](https://www.python.org/downloads/)
- download [nodejs](https://nodejs.org/en/download)
- create a virtual environment (for example using ```venv```):
    ```
    python -m venv env
    ```
- add OpenAI, SerpAPI and StackOverflow api keys to the ```env/Scripts/activate``` (or ```activate.bat``` on Windows) script to always have them in the virtual environment. Alternatively you can set them manually after activating the environment. In order to do it append this at the end of the file (on Windows use ```set``` instead of ```export```):
    ```
    export OPENAI_API_KEY=<OPENAI_API_KEY>
    export SERPAPI_API_KEY=<SERPAPI_API_KEY>
    export STACKOVERFLOW_API_KEY=<STACKOVERFLOW_API_KEY>"
    ```
- activate the environment by running the ```activate``` script:
    ```
    ./env/Scripts/activate
    ```
- install dependencies listed in ```requirements.txt```:
    ```
    pip install -r requirements.txt
    ```
- if you want to be able to access the admin panel you'll need to create a superuser:
    ```
    python manage.py createsuperuser
    ```
- now you can run the project:
    ```
    python.exe manage.py runserver
    ```

You should be able to access the API at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)