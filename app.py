import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


def load_posts():
    """
    Loads the blog posts from the JSON file.
    Returns:
        list: A list of blog post dictionaries from the JSON file.
    """
    try:
        with open("storage_file.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # Handle case if the file does not exist
        return []
    except json.JSONDecodeError:
        # Handle case if the JSON data is corrupted
        print("Error decoding JSON data.")
        return []


def save_posts(posts):
    """
    Saves the blog posts to the JSON file.
    Args:
        posts (list): A list of blog post dictionaries to save.
    """
    try:
        with open("storage_file.json", "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")


@app.route("/")
def index():
    """
    Renders the home page with all blog posts.
    Returns:
        Rendered template of the home page with the list of blog posts.
    """
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Handles the creation of a new blog post.
    Returns:
        Rendered template of the form to add a new blog post (GET),
        or a redirect to the home page (POST).
    """
    if request.method == "POST":
        new_author = request.form.get("author")
        new_title = request.form.get("title")
        new_content = request.form.get("content")

        blog_posts = load_posts()

        # Generate a new ID for the new post
        new_id = blog_posts[-1]['id'] + 1 if blog_posts else 1

        new_post = {
            'id': new_id,
            'author': new_author,
            'title': new_title,
            'content': new_content,
            'likes': 0
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template("add.html")


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Deletes a blog post by ID.
    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        A redirect to the home page after deletion.
    """
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_posts(blog_posts)
    return redirect(url_for('index'))


def fetch_post_by_id(post_id):
    """
    Fetches a single blog post by its ID.
    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        tuple: The post dictionary if found and the full list of posts;
               otherwise, None and the full list of posts.
    """
    blog_posts = load_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post, blog_posts
    return None, blog_posts


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """
    Updates an existing blog post.
    Args:
        post_id (int): The ID of the post to update.

    Returns:
        Rendered template of the update form (GET),
        or a redirect to the home page after updating (POST).
    """
    post, blog_posts = fetch_post_by_id(post_id)

    if post is None:
        abort(404, description="Post not found")

    if request.method == 'POST':
        post['author'] = request.form.get("author")
        post['title'] = request.form.get("title")
        post['content'] = request.form.get("content")

        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like_button(post_id):
    """
    Increments the 'likes' count for a blog post.
    Args:
        post_id (int): The ID of the post to like.

    Returns:
        A redirect to the home page after updating the like count.
    """
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break
    else:
        abort(404, description="Post not found")

    save_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
