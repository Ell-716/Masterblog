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


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load current blog posts from JSON
    with open("storage_file.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    # Find the post with the given ID and remove it from the list
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated blog posts list back to the JSON file
    with open("storage_file.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, indent=4)

    # Redirect back to the home page
    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    with open("storage_file.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    # Find the post by id
    for post in blog_posts:
        if post['id'] == post_id:
            return post, blog_posts  # Return the post and the whole blog_posts list
    return None, blog_posts  # Return None if not found, and the whole list


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    post, blog_posts = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with new values
        new_author = request.form.get("author")
        new_title = request.form.get("title")
        new_content = request.form.get("content")

        # Update the post fields
        post['author'] = new_author
        post['title'] = new_title
        post['content'] = new_content

        # Save the updated blog posts list back to the JSON file
        with open("storage_file.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect back to the home page
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
