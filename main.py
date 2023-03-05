from flask import Flask, render_template, request
import smtplib
import requests


app = Flask(__name__)
posts = requests.get("https://api.npoint.io/4d4fe2242ec3b9506cc7").json()
EMAIL = "kfan7793@gmail.com"
PASSWORD = "fujpiprfpakbqxtp"

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(EMAIL, EMAIL, email_message)

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)



@app.route('/about.html')
def about_page():
    return render_template("about.html")

@app.route('/contact.html', methods=["POST", "GET"])
def contact_page():
    if request.method == "POST":
        send_email(request.form['name'], request.form['email'], request.form['phone'], request.form['message'])
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['phone'])
        print(request.form['message'])
        return render_template("contact.html", posted=True)
    else:
        return render_template("contact.html", posted=False)

@app.route('/post.html')
def post_page():
    return render_template("post.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("my_posts.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
