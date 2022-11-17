# Backend Server Code
The backend serves as the server code for GCMate. It is written in [Python](https://www.python.org/) and utilizes [Flask](https://flask.palletsprojects.com/en/2.2.x/) to create APIs with the frontend. 

## Running the Server Code 
Follow these steps in order to run the backend: 
1. Open your terminal/command prompt 
2. Proceed to the root of the repository, `/backend`
3. Run the virtual environment, `venv`, by typing in the prompts below in your terminal/command prompt
   -   Windows: 
       ```
       python -m venv venv
       .\venv\Scripts\activate
       ```
   -   Mac:    
       ```
       python3 -m venv venv
       source venv/bin/activate
       ```
4. If this is the first time you are running the code, you must install Flask and Flask-CORS with these commands: 
   -   Windows: 
       ```
       pip install flask
       pip install -U flask-cors
       ```   
   -   Mac: 
       ```
       pip3 install flask
       pip3 install -U flask-cors
       ```  
5. Run `backend_app.py` by typing in the prompt below in your terminal/command prompt 
   -   Windows: `python backend_app_v2.py`
   -   Mac: `python3 backend_app_v2.py`    
     
