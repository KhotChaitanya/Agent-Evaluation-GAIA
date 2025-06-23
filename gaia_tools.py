from smolagents import PythonInterpreterTool, tool
import requests

@tool
def reverse_string_tool(input_text: str) -> str:
    """
    Takes an input string and returns its reverse.

    Args:
        input_text (str): The original string to be flipped.

    Returns:
        str: The flipped (reversed) version of the input string.
    """
    return input_text[::-1]


@tool
def execute_script_file(path_to_file: str) -> str:
    """
    Executes a Python script stored at a specific file path using the Python interpreter.

    Args:
        path_to_file (str): Absolute path to the Python script file.

    Returns:
        str: Result of script execution, or an error message.
    """
    try:
        with open(path_to_file, "r") as code_file:
            code = code_file.read()
        interpreter = PythonInterpreterTool()
        result = interpreter.run({"code": code})
        return result.get("output", "No output from script.")
    except Exception as exc:
        return f"Script execution error: {exc}"


@tool
def download_from_link(file_url: str, destination: str) -> str:
    """
    Downloads content from a specified URL and saves it locally.

    Args:
        file_url (str): URL of the file to be downloaded.
        destination (str): Local path where the file should be saved.

    Returns:
        str: Download result message.
    """
    try:
        response = requests.get(file_url, timeout=30)
        response.raise_for_status()
        with open(destination, "wb") as out_file:
            out_file.write(response.content)
        return f"File successfully saved to {destination}"
    except Exception as exc:
        return f"Download failed: {exc}"
