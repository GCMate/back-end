# Testing 

In order to test your code, you need to be running both the frontend and the backend of the project at the same time. As such, follow these instructions to run both repositories properly

## Backend 
1. Proceed to the root of the repository, `/backend`
2. Run the virtual environment, `venv`, by typing in the prompts below in your terminal/command prompt
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
4. Run `backend_app.py` by typing in the prompt below in your terminal/command prompt 
   -   Windows: `python backend_app.py`
   -   Mac: `python3 backend_app.py`    

## Frontend 
1. Proceed to the root of the repository, `/frontend`
2. Run `npm start`

## Reading Console Output in Frontend
In the frontend code, you will sometimes see `console.log()`, where something is being printed to the console. To view the contents of the console in terms of the frontend: 
1. Right-click on the screen with your mouse 
2. Click on "Inspect"
3. Click on the "Console" tab
4. Interact with the frontend to activate parts of the code you need to test 