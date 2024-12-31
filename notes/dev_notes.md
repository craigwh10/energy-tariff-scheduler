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

## mkdocs

```sh
mkdocs new [dir-name] - Create a new project.
mkdocs serve - Start the live-reloading docs server.
mkdocs build - Build the documentation site.
mkdocs -h - Print help message and exit
```

## schedule library < apschedule

I had a fair few issues using `schedule` library, such as:

- Things you schedule at an exact time dont run the job at that time
- You have to set up a blocking timer and control the clock speed on it which was a pain with testing
- It doesn't cover CRON format and passing in exact dates, only HH:MM format
- It doesn't clear historic jobs (likely due to above)

apschedule resolved all of these for me.

## Misc

Be wary of circular dependencies in classes.
