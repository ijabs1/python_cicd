# Jenkins CI/CD Python Demo Project

## Project Overview
This is a simple Flask application demonstrating a CI/CD pipeline with Jenkins.

## Local Development
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Run tests:
   ```
   pytest tests/
   ```

## Docker Build
```
docker build -t flask-jenkins-demo .
docker run -p 5009:5009 flask-jenkins-demo
```
#Just testing my multi branching pipeline