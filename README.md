# SkinNet (VERY MUCH A DRAFT, TRYING, PLAYING AROUND)

## Personal skincare accountability coach in the form of an AI expert system tracks your daily habits, identifies beneficial patterns, and sets reminders to optimize your skincare routine. This system analyzes your behaviors to determine the most effective skincare practices for you.

## Instructions for running the applicaiton:

- Create a [Python virtual environment](https://docs.python.org/3/library/venv.html)
- If you already have pyswip installed, uninstall it with `pip uninstall pyswip`
- Install the requirements with `pip install -r requirements.txt`
- Ensure that SWI-Prolog is installed and available in your PATH. You may need to add the following environment variables to your system:
  - `SWI_HOME_DIR` - The directory where SWI-Prolog is installed
  - `SWIPL` - The path to the SWI-Prolog executable
- Verify the pyswip version installed is from the github master. Running `pip freeze` should include

```
pyswip @ git+https://github.com/yuce/pyswip@59016e0841f56177d1b18ec08fd9b67792bd0a97
```
- Run `python main.py` from within the project directory.

The application uses [Textual](https://textual.textualize.io/), a Rapid Application Development framework for GUIs and TUIs in Python.
