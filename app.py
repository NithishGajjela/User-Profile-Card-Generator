from urllib.parse import urlsplit

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MAX_NAME_LENGTH = 80
MAX_BIO_LENGTH = 300
MAX_ROLE_LENGTH = 80
MAX_IMAGE_URL_LENGTH = 2048
MAX_SKILLS_LENGTH = 300
MAX_SKILLS_COUNT = 12
MAX_SKILL_LENGTH = 30


def _text_field(data, field, label, maximum, required=False):
    value = data.get(field, "")
    if not isinstance(value, str):
        return None, f"{label} must be text."

    value = " ".join(value.split())
    if required and not value:
        return None, f"{label} is required."
    if len(value) > maximum:
        return None, f"{label} must be {maximum} characters or fewer."
    return value, None


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate-profile")
def generate_profile():
    if not request.is_json:
        return jsonify(error="Request body must be JSON."), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be a valid JSON object."), 400

    errors = {}
    profile = {}
    for field, label, maximum, required in (
        ("name", "Full name", MAX_NAME_LENGTH, True),
        ("bio", "Bio", MAX_BIO_LENGTH, True),
        ("role", "Role", MAX_ROLE_LENGTH, False),
    ):
        value, error = _text_field(data, field, label, maximum, required)
        if error:
            errors[field] = error
        else:
            profile[field] = value

    image_url, error = _text_field(
        data, "image_url", "Profile image URL", MAX_IMAGE_URL_LENGTH
    )
    if error:
        errors["image_url"] = error
    elif image_url:
        try:
            parsed_url = urlsplit(image_url)
            valid_url = (
                parsed_url.scheme.lower() in ("http", "https")
                and parsed_url.hostname is not None
                and parsed_url.username is None
                and parsed_url.password is None
            )
            parsed_url.port
        except ValueError:
            valid_url = False
        if not valid_url:
            errors["image_url"] = (
                "Profile image URL must be a valid HTTP or HTTPS URL."
            )
        else:
            profile["image_url"] = image_url
    else:
        profile["image_url"] = ""

    skills_input, error = _text_field(
        data, "skills", "Skills", MAX_SKILLS_LENGTH
    )
    if error:
        errors["skills"] = error
    else:
        skills = [" ".join(skill.split()) for skill in skills_input.split(",")]
        skills = [skill for skill in skills if skill]
        if len(skills) > MAX_SKILLS_COUNT:
            errors["skills"] = f"Enter no more than {MAX_SKILLS_COUNT} skills."
        elif any(len(skill) > MAX_SKILL_LENGTH for skill in skills):
            errors["skills"] = (
                f"Each skill must be {MAX_SKILL_LENGTH} characters or fewer."
            )
        else:
            profile["skills"] = skills

    if errors:
        return jsonify(error="Please correct the highlighted fields.", fields=errors), 400

    return jsonify(profile=profile), 200


if __name__ == "__main__":
    app.run(debug=True)
