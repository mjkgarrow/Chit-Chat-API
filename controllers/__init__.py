from controllers.index_controller import index
from controllers.chats_controller import chats
from controllers.auth_controller import auth
from controllers.user_controller import users
from controllers.reset_all import reset


registerable_controllers = [
    index,
    chats,
    auth,
    users,
    reset
]
