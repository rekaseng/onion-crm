### Installation
Install poetry on your machine. Then run "poetry install" on this folder.

Next set the python path before running the app or upgrade db. see below on setting python path

To add new library run poetry add
```poetry add pyserial```

### DB Migration

Create a model in models folder (as user.py)

1) Import new model in alembic/env.py

Use the following command to create a new migration file in alembic-migration/versions folder. 
This command needs to be run on root folder:

WINDOWS
$env:PYTHONPATH="src"
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
alembic revision  --autogenerate --rev-id=$timestamp -m "add_user"

LINUX
alembic revision  --autogenerate --rev-id=$(date +%Y%m%d%H%M%S) -m "add_user"

(Note: the env should not have "asyncpg" in the connection string. "asyncpg" is for when the app runs)

Then use the following command to update the new migration file to db:
```alembic upgrade head```

If need to undo use the following command to revert the current migration file in db(check alembic_version table to see current migration file is updating in the db):
```alembic downgrade -1```

To delete migration file. manually delete it from alembic-migration/versions folder.

### To run
create .env file from sample and put credentials in it.

set PYTHONPATH=src
poetry shell
uvicorn main:app --reload

### Testing
set path on windows cmd:
set PYTHONPATH=src

set path on windows powershell:
$env:PYTHONPATH="src"

set path on linux:
export PYTHONPATH=/apps/fridge-app/src

### IDE
if using pycharm, need to add "src" folder to be "Sources Root"
right click on the "src" and choose "Mark Directory As" then "Sources Root"