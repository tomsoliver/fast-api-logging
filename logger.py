import traceback
from starlette_context import context


def log(key: str, value):
    if "diagnostics" not in context:
        context["diagnostics"] = {}

    context["diagnostics"][key] = value


def log_exception(exception: Exception):
    error_dict = vars(exception)

    message = str(exception)
    if message:
        error_dict["message"] = message

    error_dict["traceback"] = traceback.format_exc()
    log("error", error_dict)


def log_message(message: str):
    if "diagnostics" not in context:
        context["diagnostics"] = {}

    if "messages" not in context["diagnostics"]:
        context["diagnostics"]["messages"] = []

    context["diagnostics"]["messages"].append(message)
