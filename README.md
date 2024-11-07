# Masterblog ✨

This is a simple Flask-based blog application built as part of an assignment in the Software Engineer Bootcamp. The application allows users to add, update, delete, and "like" blog posts. It provides a basic demonstration of how to use Flask to manage dynamic web content and handle form submissions.

## Features 🛠️

- **Add Blog Post**: Users can create new blog posts by providing an author, title, and content.
- **Update Blog Post**: Existing blog posts can be updated by modifying the author, title, and content.
- **Delete Blog Post**: Blog posts can be deleted from the system.
- **Like Button**: Each blog post has a like button to allow users to interact with the posts. The like count is incremented each time the like button is pressed.
- **Responsive Layout**: The app is styled with CSS to ensure a clean, user-friendly interface.

## Installation ⚙️

```bash
# Clone the repository
git clone https://github.com/Ell-716/Masterblog.git

# Navigate into the project directory
cd Masterblog

# Install required dependencies
pip install -r requirements.txt

# Run the Flask application
http://localhost:5000
```
## Usage 📖

### Home Page 🏠

- When the app is run, users are directed to the home page (`/`), where they can view all blog posts.
- Each blog post displays the title, author, and content, along with options to **update**, **delete** or **like** the post.
- Users has also an option to **add a new post**.

### Add a New Post ✍️

- To add a new blog post, click the **Add a New Post** link at the top-left of the home page.
- Fill out the form with the author's name, title, and content for the new post.

### Update an Existing Post 🔄

- To update an existing post, click the **Update** button under the post you want to modify.
- The post's current details will be pre-filled in the update form, and you can edit them and save the changes.

### Delete a Post 🗑️

- To delete a post, click the **Delete** button under the post.
- This will permanently remove the post from the app.

## Technologies Used 💻

- **Flask**: Web framework used to create the server-side logic and handle routing.
- **Jinja2**: Templating engine used to render dynamic content in HTML pages.
- **HTML/CSS**: For designing the user interface.
- **JSON**: Used for storing the blog posts locally.

## Project Requirements 📦

- Python 3.x
- Flask 3.0.3
- Jinja2 3.1.4

## Contributions 🤝

If you'd like to contribute to this project, feel free to submit a pull request. Contributions are welcome in the form of bug fixes, new features, or general improvements to the project. Please ensure that your code is properly tested and follows the style guidelines before submitting.
