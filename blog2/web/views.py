from operator import or_

from flask import Blueprint, render_template, request, redirect, url_for

from back.models import Article, ArticleType, db, Comment

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/')
def index():
    types = ArticleType.query.all()
    articles = Article.query.limit(5).all()
    return render_template('web/index.html', articles=articles, types=types)


@web_blue.route('/article/<int:id>',methods=['GET', 'POST'])
def article(id):
    if request.method == 'GET':
        types = ArticleType.query.all()
        article = Article.query.get(id)
        articles = Article.query.all()
        arts = []
        for article1 in articles:
            arts.append(article1)
        pr_art = ''
        next_art = ''
        for index in range(len(arts)):
            if id == arts[index].id:
                if index == 0:
                    pr_art = ''
                    if index == len(arts)-1:
                        next_art = ''
                        break
                    else:
                        next_art = arts[index + 1]
                        break
                elif index == len(arts)-1:
                    next_art = ''
                    if index == 0:
                        pr_art = ''
                        break
                    else:
                        pr_art = arts[index - 1]
                        break
                else:
                    pr_art = arts[index - 1]
                    next_art = arts[index + 1]
                    break
        article.count += 1
        db.session.add(article)
        db.session.commit()
        coms = article.a_c
        count = len(coms)
        return render_template('web/article.html', article=article,
                               types=types, pr_art=pr_art, next_art=next_art,
                               coms=coms, count=count)
    if request.method == 'POST':
        article = Article.query.get(id)
        com = request.form.get('comm')
        comment = Comment()
        comment.article = id
        comment.content = com
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('web.article', id=id))


@web_blue.route('/about/')
def about():
    types = ArticleType.query.all()
    return render_template('web/about.html', types=types)


@web_blue.route('/art_list/<int:b>/',methods=['GET', 'POST'])
def art_list(b):
    if request.method == 'GET':
        articles = Article.query.all()
        num = len(articles)
        if num % 5 == 0:
            num = num // 5
        num = num // 5 + 1
        articles1 = Article.query.offset(b - 1).limit(5).all()
        types = ArticleType.query.all()
        return render_template('web/art_list.html',articles1=articles1, types=types, num=num)


@web_blue.route('/type_list/<int:id>')
def type_list(id):
    types = ArticleType.query.all()
    articles = Article.query.filter(Article.type == id).all()
    num = len(articles)
    if num % 5:
        num = num // 5 + 2
    num = num // 5 + 1
    return render_template('web/type_list.html', articles=articles, types=types, num=num)


@web_blue.route('/add_good/<int:id>/',methods=['GET'])
def add_good(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        good_num = article.good_num
        good_num = good_num + 1
        article.good_num = good_num
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('web.article', id=article.id))


@web_blue.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':
        str = request.form.get('keyboard')
        types = ArticleType.query.all()
        articles = Article.query.filter(or_(Article.title.contains(str),
                                            Article.content.contains(str))).all()
        return render_template('web/sea_art_list.html', articles=articles,
                               types=types)

