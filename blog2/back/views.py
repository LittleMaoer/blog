
from flask import Blueprint, render_template, request, redirect, url_for, session

from back.models import User, Article, ArticleType, db

from werkzeug.security import generate_password_hash, check_password_hash

from utils.functions import is_login

back_blue = Blueprint('back', __name__)


@back_blue.route('/index/')
@is_login
def index():
    return render_template('back/index.html')


@back_blue.route('/to_main_page/')
def to_main_page():
    return redirect(url_for('web.index'))


@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已注册，请更换其他账号'
                return render_template('back/register.html', error=error)
            else:
                if password != password2:
                    error = '两次密码填写不一致，请重新注册'
                    return render_template('back/register.html', error=error)
                else:
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    session['user_id'] = user.id
                    return redirect(url_for('back.login'))
        else:
            error = '请填写完整信息'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if user:
                if check_password_hash(user.password, password):
                    return redirect(url_for('back.index'))
                else:
                    error = '账号或密码不正确，请重新输入'
                    return render_template('back/login.html', error=error)
            else:
                error = '账号不存在，请重新输入'
                return render_template('back/login.html', error=error)
        else:
            error = '请输入完整信息'
            return render_template('back/login.html', error=error)


@back_blue.route('/logout/', methods=['GET'])
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


@back_blue.route('/user_inf/', methods=['GET', 'POST'])
def user_inf():
    if request.method == 'GET':
        return render_template('back/user_inf.html')
    if request.method == 'POST':
        pass


@back_blue.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)


@back_blue.route('/add_type/', methods=['GET', 'POST'])
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            type1 = ArticleType.query.filter(ArticleType.t_name == atype).first()
            if type1:
                error = '文章分类已存在，请重新输入'
                return render_template('back/category_add.html',error=error)
            else:
                art_type = ArticleType()
                art_type.t_name = atype
                db.session.add(art_type)
                db.session.commit()
                return redirect(url_for('back.a_type'))

        else:
            error = '请填写分类信息'
            return render_template('back/category_add.html', error=error)


@back_blue.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


@back_blue.route('/article_list/', methods=['GET'])
def article_list():
    articles = Article.query.all()
    return render_template('back/article_list.html', articles=articles)


@back_blue.route('/article_add/', methods=['GET', 'POST'])
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        print(title, desc, category, content)
        if title and desc and category and content:
            article = Article.query.filter(Article.title == title).first()
            if article:
                error = '文章标题已存在'
                return redirect(url_for('back.article_add', error=error))
            else:
                art = Article()
                art.title = title
                art.desc = desc
                art.type = category
                art.content = content
                db.session.add(art)
                db.session.commit()
                return redirect(url_for('back.article_list'))

        else:
            error = '请填写完整文章信息'
            return render_template('back/article_detail.html', error=error)


@back_blue.route('/article_del/<int:id>', methods=['GET'])
def article_del(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('back.article_list'))


@back_blue.route('/article_update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    if request.method == 'GET':
        types = ArticleType.query.all()
        article = Article.query.get(id)
        return render_template('back/article_update.html', article=article, types=types)
    if request.method == 'POST':

        title = request.form.get('name')
        desc = request.form.get('desc')
        content = request.form.get('content')
        article = Article.query.get(id)
        article.title = title
        article.desc = desc
        article.content = content
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('back.article_list'))


@back_blue.route('/user_list/')
def user_list():
    users = User.query.all()
    return render_template('back/user_list.html', users=users)


@back_blue.route('/add_user/', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('back/add_user.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        tel = request.form.get('tel')
        email = request.form.get('email')
        if username and password and tel and email:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '姓名已存在'
                return redirect(url_for('back.add_user', error=error))
            else:
                user = User()
                user.username = username
                user.password = password
                user.tel = tel
                user.email = email
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('back.user_list'))

        else:
            error = '请填写完整用户信息'
            return render_template('back/add_user.html', error=error)


@back_blue.route('/cha_user/<int:id>', methods=['GET', 'POST'])
def cha_user(id):
    if request.method == 'GET':
        user = User.query.get(id)

        return render_template('back/cha_user.html', user=user)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        tel = request.form.get('tel')
        email = request.form.get('email')
        user = User.query.get(id)
        user.username = username
        user.password = password
        user.tel = tel
        user.email = email
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('back.user_list'))


@back_blue.route('/del_user/<int:id>')
def del_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('back.user_list'))

#
# @back_blue.route('/search/', methods=['POST'])
# def search():
#     if request.method == 'POST':
#         str = request.form.get('search')
#         users = User.query.filter(or_(User.tel.contains(str),
#                                             User.email.contains(str))).all()
#         return render_template('web/sea_art_list.html', users=users)