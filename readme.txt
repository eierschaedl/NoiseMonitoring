Starting the project

1) move to backend/ directory
2) run "pip install -r requirements.txt"
3) run "python3 manage.py runserver"

if error stay in backend/ directory and do the following:

Find virtual environment (venv)
if not create it by running "python3 -m venv venv"

Activate Virtual Environment:
macOS/linux run:
source venv/bin/activate

Windows run:
venv\Scripts\activate

Install Required Packages:
pip install -r requirements.txt

now run "python3 manage.py runserver" again and open http://127.0.0.1:8000/ in your browser