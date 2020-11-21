from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100) , nullable=False)
    content = db.Column(db.Text,nullable = True)
    author = db.Column(db.String,nullable = False,default="Deep")
    date_posted = db.Column(db.DateTime,nullable  = False,default = datetime.utcnow())

    def __repr(self):
        return 'blog_post' + self.id


@app.route("/posts",methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title = post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    if request.method == 'GET': 
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('post.html',posts = all_posts)

if __name__ == "__main__":
    app.run(debug=True)