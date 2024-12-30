# Dev notes

Some random notes of things I keep randomly forgetting about.

## Installing packages on local venv

```sh
python .venv/bin/pip install time-machine 
```

## Pytest loglevel

```sh
pytest --log-cli-level=DEBUG 
```

## Local venv python run

```sh
.venv/bin/python ./python/__tests__/run.py
```

## Misc

Be wary of circular dependencies in classes.
