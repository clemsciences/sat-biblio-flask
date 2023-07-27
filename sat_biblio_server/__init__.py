"""

"""

import os

from flask import Flask, url_for, redirect, request, Blueprint
from flask_babel import Babel
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_mail import Mail
from wtforms.validators import ValidationError
from wtforms import StringField, PasswordField
import wtforms
from werkzeug.security import check_password_hash
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from sat_biblio_server.database.db_manager import db
from sat_biblio_server.database.books import EmpruntLivreDB, EnregistrementDB, AuthorDB, ReferenceBibliographiqueLivreDB
from sat_biblio_server.database.books_2023 import EmpruntLivre2023DB, Enregistrement2023DB, \
    Author2023DB, ReferenceBibliographiqueLivre2023DB, HelperAuthorBook2023
from sat_biblio_server.database.users import UserDB
from sat_biblio_server.database.events import LogEventDB
from sat_biblio_server.database.imports import ImportDB, ImportedItemsDB
from sat_biblio_server.utils import json_result


PACKDIR = os.path.abspath(os.path.dirname(__file__))


babel = Babel()
lm = LoginManager()
# lm.login_view = 'main.index'

csrf = CSRFProtect()
mail = Mail()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()


# region admin
class SatAdminModelView(ModelView):
    page_size = 50  # the number of entries to display on the list view
    column_exclude_list = ['password', ]

    def is_accessible(self):
        # print(current_user.is_active)
        # print(current_user.is_authenticated)

        # return True
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if hasattr(current_user, "is_admin"):
            # if current_user.is_admin or current_user.email == "clem@clementbesnier.fr":
            if current_user.is_admin:
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class AdminLoginForm(wtforms.form.Form):
    email = StringField(validators=[wtforms.validators.required()])
    password = PasswordField(validators=[wtforms.validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(UserDB).filter_by(email=self.email.data).first()


class RegistrationForm(wtforms.form.Form):
    login = wtforms.fields.StringField(validators=[wtforms.validators.required()])
    email = wtforms.fields.StringField()
    password = wtforms.fields.PasswordField(validators=[wtforms.validators.required()])

    def validate_login(self, field):
        if db.session.query(UserDB).filter_by(email=self.login.data).count() > 0:
            raise wtforms.validators.ValidationError('Duplicate username')


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = AdminLoginForm(request.form)
        # print('login viw')
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)
            # print('validat')

        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        # print(form)
        self._template_args['form'] = form
        # link = "<p>Don't have an account? <a href=\"" + url_for('.register_view') + "\">Click here to register.</a></p>"
        # self._template_args['link'] = link
        # print('login ntr')
        # return render_template('gestion/index.html')
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('admin.index'))
# endregion


sat_biblio = Blueprint('sat_biblio', __name__)


def create_app(config):
    """Create an application instance."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    @app.errorhandler(404)
    def page_not_found(e):
        return json_result(False, message="404"), 404  # ("page_inconnue.html"), 400

    @app.errorhandler(500)
    def internal_server_error(e):
        return json_result(False, message="500"), 500  # "500.html"), 500

    @app.errorhandler(CSRFError)
    def csrf_error(reason):
        return json_result(False, message="Problème de CSRF - 400")

    @app.route("/bad_request")
    def bad_json_request():
        return json_result(False)

    # @app.after_request
    # def add_cors_headers(response):
    #     r = request.referrer
    #     logging.error("cors bizarre")
    #     response.headers.add('Access-Control-Allow-Origin', "*")
    #     # if r is not None:
    #     #     response.headers.add('Access-Control-Allow-Origin', "*")
    #     # response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', 'http://127.0.0.1:5000'))
    #     return response

    # initialize extensions
    db.init_app(app)

    # login manager for admin
    lm.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # admin page
    admin = Admin(app, "Administration",
                  base_template="admin/index.html",
                  index_view=MyAdminIndexView(),
                  template_mode="bootstrap3")
    admin.add_view(SatAdminModelView(UserDB, db.session))
    admin.add_view(SatAdminModelView(AuthorDB, db.session))
    admin.add_view(SatAdminModelView(Author2023DB, db.session))
    admin.add_view(SatAdminModelView(EnregistrementDB, db.session))
    admin.add_view(SatAdminModelView(Enregistrement2023DB, db.session))
    # admin.add_view(SatAdminModelView(ReferenceBibliographiqueArticleDB, db.session))
    admin.add_view(SatAdminModelView(ReferenceBibliographiqueLivreDB, db.session))
    admin.add_view(SatAdminModelView(ReferenceBibliographiqueLivre2023DB, db.session))
    admin.add_view(SatAdminModelView(EmpruntLivre2023DB, db.session))
    admin.add_view(SatAdminModelView(ImportDB, db.session))
    admin.add_view(SatAdminModelView(ImportedItemsDB, db.session))

    # migration
    migrate.init_app(app, db)

    @lm.user_loader
    def load_user(user_id):
        return UserDB.query.get(user_id)

    # import blueprints
    from sat_biblio_server.routes import sat_biblio
    sat_biblio.config = config

    # @sat_biblio.after_request
    # def after_request(response):
    # if config.ENV == "production":
    # response.headers.add("Access-Control-Allow-Origin", "https://satbiblio.clementbesnier.eu")
    # else:
    # response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000")
    # #header["Access-Control-Allow-Credentials'"] = "Origin, X-Requested-With, Content-Type, Accept"
    # response.headers.add("Access-Control-Allow-Credentials", "true")
    # response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    # response.headers.add("Access-Control-Allow-Headers", "x-csrf-token")
    # response.headers.add("Access-Control-Allow-Methods", "GET,POST,DELETE,PUT,OPTIONS")
    # return response

    app.register_blueprint(sat_biblio)
    # print("application lancée")
    # app.secret_key = "Essai"
    # for i in app.url_map.iter_rules():
    #     print(i)
    return app
