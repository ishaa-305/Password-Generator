from flask import Flask, render_template, request
import secrets
import string
import re

app = Flask(__name__)

def generate_password(length, numbers, symbols):

    characters = string.ascii_letters

    if numbers:
        characters += string.digits

    if symbols:
        characters += "!@#$%^&*()_+-=[]{}<>?/"

    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase)
    ]

    if numbers:
        password.append(secrets.choice(string.digits))

    if symbols:
        password.append(
            secrets.choice("!@#$%^&*()_+-=[]{}<>?/")
        )

    while len(password) < length:
        password.append(secrets.choice(characters))

    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def check_strength(password):

    score = 0

    if len(password) >= 12:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*()_+\-=\[\]{}<>?/]", password):
        score += 1

    if score == 5:
        return "Very Strong"
    elif score == 4:
        return "Strong"
    elif score == 3:
        return "Medium"
    else:
        return "Weak"


@app.route("/", methods=["GET", "POST"])
def home():

    password = ""
    strength = ""
    length = ""

    numbers = False
    symbols = False

    if request.method == "POST":

        length = int(request.form["length"])

        numbers = "numbers" in request.form
        symbols = "symbols" in request.form

        password = generate_password(
            length,
            numbers,
            symbols
        )

        strength = check_strength(password)

    return render_template(
        "index.html",
        password=password,
        strength=strength,
        length=length,
        numbers=numbers,
        symbols=symbols
    )

if __name__ == "__main__":
    app.run(debug=True)