from controllers.index_controller import index
from controllers.auth_controller import auth
from controllers.user_controller import users
from controllers.reset_all import reset
# from controllers.chat_controller import chats


registerable_controllers = [
    index,
    auth,
    users,
    reset
]
