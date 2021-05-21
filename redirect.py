login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    pass # Add logic to redirect to Github OAuth flow when unauthenticated

@login_manager.user_loader
def load_user(user_id):
    return None

login_manager.init_app(app)