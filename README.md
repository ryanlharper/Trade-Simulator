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
2. Build a Docker image:
	- docker build -t trade-simulator:1.0 .
3. Start containers: 
	- docker compose up -d
4. Migrate database: 
	- docker-compose exec web python manage.py migrate
5. Create database superuser: 
	- docker compose exec web python manage.py createsuperuser
6. Run program:
	- navigate browser to localhost:8000

### Google Cloud Installation Instructions
1. Replace the settings.py contents with gcloud_settings.txt contents
2. Remove files & folders:
	- Files: Dockerfile, docker-compose.yml, .gitignore and README.md 
	- Folders: .vscode and data
3. Create a new Google Cloud project in Google Cloud Console
4. Open Google Cloud Shell and set variables
	- REGION= 
	- PGSERVER=
	- DBNAME= 
	- REPO= 
	- IMAGE= 
	- PROJECT_ID=$(gcloud config get-value project)
	- PROJECT_NUM=$(gcloud projects describe $PROJECT_ID --format 'value(projectNumber)')
5. Enable cloud APIs
6. Set up Google Cloud SQL and Google Storage Bucket
	- Create Postgres database
	- Create Postgres user account and password
	- Allow Cloud Build to access Postgres
	- Set up Google Storage Bucket for static files
7. Store configuration and allow Cloud Build and Cloud Run access
8. Set up Django and Docker files
	- Transfer program files to server 
	- Create Dockerfile with contents of gcloud_Dockerfile.txt
9. Build and push image to Artifact Registry
10. Run migrations and collect static files
	- Create cloudmigrate.yml with contents of gcloud_cloudmigrate_yaml.txt
	- Execute migrations to Postgres server
11. Deploy and test 