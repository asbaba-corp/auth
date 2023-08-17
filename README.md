![alt text](https://github.com/asbaba-corp/auth/blob/main/auth_diagram.png?raw=true)

# Create venv

```
python -m venv venv
```

# Install requirements

```
pip install -r requirements.txt
```

# Install Pre-commit (Optional)

```
pre-commit install
```

# Run the project at root directory

```
uvicorn app.main:app
```

# If you want to do offline lambda testing:

```
serverless offline start
```

# Useful dev commands:

# Pytest

Pytest with logs:

```
 pytest -s -v
```

# Linter checking

To check pre-commit status:

```
 pre-commit run --all-files
```

# Freezing requirements with venv

Might change depending on the OS, but the idea is to freeze requirements starting from the pip inside venv folder:

```
 .\venv\Scripts\pip3 freeze > requirements.txt
```

# DEVOPS SECTION

# Deploy to AWS Lambdas

```

sls deploy --aws-profile default
```
