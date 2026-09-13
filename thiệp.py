from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)


def get_guest(name):
    with open("guests.csv", newline="", encoding="utf-8-sig") as file:
        guests = csv.DictReader(file)

        for guest in guests:
            if guest["name"].strip().lower() == name.strip().lower():
                return guest

    return None


@app.route("/")
def invitation():
    name = request.args.get("name", "Friend")

    guest = get_guest(name)

    if guest:
        name = guest["name"]

    return render_template("index.html", name=name)


@app.route("/rsvp", methods=["POST"])
def rsvp():

    name = request.form.get("name")
    response = request.form.get("response")
    message = request.form.get("message", "")

    file_exists = os.path.exists("responses.csv")

    with open(
        "responses.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "name",
                "response",
                "message"
            ])

        writer.writerow([
            name,
            response,
            message
        ])

    return render_template(
        "thankyou.html",
        name=name,
        response=response
    )


if __name__ == "__main__":
    app.run(debug=True)
