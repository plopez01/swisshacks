# swisshacks

## Useful links
[Challenge original repo](https://github.com/SwissHacks-2025/juliusbaer?tab=readme-ov-file)  
[API docs](https://hackathon-api.mlo.sehlat.io/docs)  
[Frontend](https://hackathon-frontend.mlo.sehlat.io/)  
[Leaderboard](https://hackathon-frontend.mlo.sehlat.io/leaderboard)
## Ideas
- Check for consistency betwen documents, but also compare documents with real world data, like city name with country, etc.

## Design considerations
We need a way to define how generic fields shall be compared toghether for consistency.
For it to be versatile, a function could be passed when constructing the field that specifies how it's
consistency score is calculated. This may just be a formula, or a call to a LLM for it to decide.

Scores may be grouped in consistency categories, for which different limits may be configured.
Like a maximum amount of detected typos, etc.

## How to Run the Program

### Step 1: Create a Python Virtual Environment
To create a virtual environment on Windows, open your command prompt and run the following command:

```bash
py -m venv SuizaEnv
```

### Step 2: Activate the Virtual Environment
Activate the virtual environment by running:

```bash
SuizaEnv\Scripts\activate
```

### Step 3: Install Dependencies
With the virtual environment activated, install the required dependencies using:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Program
Finally, execute the program by running:

```bash
python game_starter.py
```
