from flask import Flask,render_template,url_for,request
from newsapi import NewsApiClient
from flask_mysqldb import MySQL
import os

app=Flask(__name__,template_folder='templates',static_folder='static')
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="users_db"

mysql=MySQL(app)



@app.route('/',methods=['GET','POST'])
def home():
    api_key = '1374a8edb5c3406db4666095b0a9017b'

    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources = 'bbc-news')
    all_articles = newsapi.get_everything(sources = 'bbc-news')


    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']


    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range(len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []
    url_all = []


    for j in range(len(a_articles)): 

        print(a_articles)
        a_article = a_articles[j]   

        news_all.append(a_article['title'])
        desc_all.append(a_article['description'])
        img_all.append(a_article['urlToImage'])
        p_date_all.append(a_article['publishedAt'])
        url_all.append(a_article['url'])


    contents = zip(news,desc,img,p_date,url)
    all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    if request.method=='POST':
        full_name=request.form['full_name']
        phone=request.form['phone']
        email=request.form['email']
        password=request.form['password']
        City_name=request.form['City_name']
        gender=request.form['gender']

        cur=mysql.connection()
        cur.execute("INSERT INTO register (user_id,name,phone_no,mail_id,password,city_name,gender) VALUES (%d,%s,%d,%s,%s,%s,%s)",(full_name,phone,email,password,City_name,gender))
        mysql.connection.commit()
        cur.close()
        return "Registered successfully"


    return render_template('home.html', contents=contents, all=all)



if __name__ == '__main__':
    app.run(debug=True)
