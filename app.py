import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the home page and displays all the blog posts.
    Reads the blog posts from the JSON storage file and passes them to the
    'index.html' template for rendering. Displays the list of posts with
    options to add, update, delete, and like the posts.
    Returns:
        Rendered template of the home page with the list of blog posts.
    """
    with open("storage_file.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)
        return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Handles the creation of a new blog post.
    If the request method is POST, it collects the form data (author, title,
    and content), generates a new post ID, adds the new post to the list of
    blog posts, and saves the updated list back to the JSON storage file.
    Redirects back to the home page after successful post creation.
    Returns:
        Rendered template of the form to add a new blog post if the method
        is GET, or a redirect to the home page after a successful POST.
    """
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
            'content': new_content,
            'likes': 0
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
    """
    Handles the deletion of a blog post.
    This route removes the blog post with the specified post_id from the JSON
    storage file and redirects back to the home page.
    Args:
        post_id (int): The ID of the post to be deleted.
    Returns:
        A redirect to the home page after the post has been deleted.
    """
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
    """
    Fetches a blog post by its ID from the JSON storage file.
    This helper function retrieves a post and the full list of blog posts
    from the JSON file based on the given post_id.
    Args:
        post_id (int): The ID of the post to retrieve.
    Returns:
        tuple: A tuple containing the post (if found) and the full list of
               blog posts. If the post is not found, returns None and the
               full list of blog posts.
    """
    with open("storage_file.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    # Find the post by id
    for post in blog_posts:
        if post['id'] == post_id:
            return post, blog_posts  # Return the post and the whole blog_posts list
    return None, blog_posts  # Return None if not found, and the whole list


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """
    Handles the update of an existing blog post.
    If the request method is POST, the function updates the post's author,
    title, and content with the new values from the form and saves the updated
    post list to the JSON file. Redirects back to the home page after successful update.
    Args:
        post_id (int): The ID of the post to update.
    Returns:
        Rendered template for the update form if the method is GET, or a
        redirect to the home page after a successful POST.
    """
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


@app.route('/like/<int:post_id>', methods=['POST'])
def like_button(post_id):
    """
    Handles the liking of a blog post.
    This route increments the 'likes' count for the blog post with the
    specified post_id in the JSON storage file and redirects back to the home page.
    Args:
        post_id (int): The ID of the post to be liked.
    Returns:
        A redirect to the home page after the like count has been updated.
    """
    with open("storage_file.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    # Find the post by its ID and increment the 'likes' count
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    with open("storage_file.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
