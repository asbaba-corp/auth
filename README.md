![alt text](https://github.com/asbaba-corp/auth/blob/main/auth_diagram.png?raw=true)

# DEVOPS SECTION

# Create venv

```
python -m venv venv
```

# Install requirements

```
pip install -r requirements.txt
```

# Deploy to AWS Lambdas

```

sls deploy --aws-profile default
```

# DEVELOPMENT SECTION

# Run the project

```
python main.py
```

or with uvicorn

```
uvicorn main:run_app
```

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

Might change depending on the OS, but find the pip inside venv folder:

```
 .\venv\Scripts\pip3 freeze > requirements.txt
```

# Commands used to generate pylintrc and pre-commit-config.yaml (Optional)

Generate pylintrc:

```
pylint --generate-rcfile | out-file -encoding utf8 .pylintrc
```

after configurating the .pre-commit-config.yaml

```
pre-commit install
```
