import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    with open("storage_file.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)
        return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_author = request.form.get("author")
        new_title = request.form.get("title")
        new_content = request.form.get("content")

        # Load current blog posts from JSON
        with open("storage_file.json", "r", encoding="utf-8") as file:
            blog_posts = json.load(file)

        # Generate a new ID for the new post
        new_id = blog_posts[-1]['id'] + 1 if blog_posts else 1

        # Create a new blog post dictionary
        new_post = {
            'id': new_id,
            'author': new_author,
            'title': new_title,
            'content': new_content
        }

        # Append the new post to the list
        blog_posts.append(new_post)

        # Save the updated blog posts list back to the JSON file
        with open("storage_file.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect back to the home page
        return redirect(url_for('index'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
