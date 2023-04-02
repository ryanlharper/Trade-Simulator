# Trade Simulator
Trade Simulator is a Python-based Trade Simulation program that is built with Python, Django, SQL, and PostgreSQL. The program allows users to make transactions of any security available in yFinance's library. Transactions are implemented in real-time and portfolio values are displayed on the homepage. All positions and transactions are publicly viewable, making Trade Simulator a place for investment fanatics to compare portfolio performance in an open forum. 

## Features and Functionality
- Simulate security transactions in real-time
- Monitor individual security and portfolio performance
- Monitor other users' transactions, positions and performance

## Technologies Used
- Django
- Python
- SQL and PostgreSQL
- HTML
- CSS
- Docker
- VS Code
- Git
- Google Cloud

### Future Development
##### Front-End 
- Further develop front-end for Trade Simulator making it user-firendly
##### Features
- Add sell feature directly to a user's postions to make trading more simple
- Add comments sections allowing for discussions of trades and positions
- Add groups to allow for challenges among selected users
- Add user profiles and images or avatars
##### Testing and Quality Assurance
- Develop automated tests to ensure that Trade Simulator functions as expected and to catch bugs early
- Conduct regular testing to ensure that Trade Simulator is user-friendly and free of defects

### Local Installation Instructions
1. Clone the repository: 
	- git clone https://github.com/ryanlharper/Trade-Simulator.git
2. Create a virtual environment:
	- python -m venv venv
3. Build a Docker image:
	- docker build -t trade-simulator:1.0 .
4. Start containers: 
	- docker compose up -d
5. Migrate database: 
	- docker-compose exec web python manage.py migrate
6. Create database superuser: 
	- docker compose exec web python manage.py createsuperuser
7. Run program:
	- navigate browser to localhost:8000

### Screenshots:
| Home Page | Positions |
|---------|---------|
| ![Alt text](screenshots/home.png?raw=true "Home Page") | ![Alt text](screenshots/positions.png?raw=true "Positions") |
| Recent Transactions | Create Transaction |
| ![Alt text](screenshots/recent_transactions.png?raw=true "Recent Transactions") | ![Alt text](screenshots/transaction.png?raw=true "Create Transaction") |

