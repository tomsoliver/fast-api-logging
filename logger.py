from starlette_context import context


def log(key: str, value):
    if "diagnostics" not in context:
        context["diagnostics"] = {}

    context["diagnostics"][key] = value


def log_message(message: str):
    if "diagnostics" not in context:
        context["diagnostics"] = {}

    if "messages" not in context["diagnostics"]:
        context["diagnostics"]["messages"] = []

    context["diagnostics"]["messages"].append(message)
