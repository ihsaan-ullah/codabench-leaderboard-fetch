import json
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
from config import (
    PROCESSED_RESULT_JSON_FILE,
    HTML_TEMPLATE_FILE,
    HTML_OUTPUT_FILE
)


def main():
    """
    Generates an HTML file from processed results using a Jinja template.
    Loads the JSON data, renders it into the template, and saves the output HTML.
    """
    # Load data
    with open(PROCESSED_RESULT_JSON_FILE, "r") as f:
        data = json.load(f)

    # Create a readable timestamp
    last_updated = datetime.now(timezone.utc).strftime("%B %d, %Y at %I:%M %p UTC")

    # Setup Jinja environment (load from current directory)
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(HTML_TEMPLATE_FILE)

    # Render template
    html_content = template.render(results=data, last_updated=last_updated)

    # Save to file
    with open(HTML_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Generated {HTML_OUTPUT_FILE} with {len(data)} results")


if __name__ == "__main__":
    main()
