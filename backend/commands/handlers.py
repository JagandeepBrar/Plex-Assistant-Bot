import logging
import backend.api.telegram as telegram
from functools import wraps
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, Filters
from backend.commands.command import account, admin, notify
from backend import constants

def initialize():
    # Account-Related
    telegram.dispatcher.add_handler(ConversationHandler(
        entry_points = [
            CommandHandler("start", account.register),
            CommandHandler("register", account.register)
        ],
        fallbacks = [CommandHandler("cancel", account.registerCancel)],
        states = {
            constants.ACCOUNT_REGISTER_STATE_FREQ: [
                RegexHandler(constants.ACCOUNT_FREQUENCY_REGEX, account.registerFrequency)
            ],
            constants.ACCOUNT_REGISTER_STATE_OMBI: [
                MessageHandler(Filters.text, account.registerOmbi),
                CommandHandler("skip", account.registerOmbiSkip)
            ]
        }
    ))
    telegram.dispatcher.add_handler(ConversationHandler(
        entry_points = [
            CommandHandler("account", account.account)
        ],
        fallbacks = [CommandHandler("exit", account.accountExit)],
        states = {
            constants.ACCOUNT_STATE_OPTIONS: [
                RegexHandler(constants.ACCOUNT_OPTIONS_REGEX, account.accountOptions)
            ],
            constants.ACCOUNT_STATE_OMBI: [
                MessageHandler(Filters.text, account.accountUpdateOmbi),
                CommandHandler("skip", account.accountUpdateOmbiSkip)
            ],
            constants.ACCOUNT_STATE_FREQ: [
                RegexHandler(constants.ACCOUNT_FREQUENCY_REGEX, account.accountUpdateFrequency)
            ]
        }
    ))
    # Notification related
    telegram.dispatcher.add_handler(CommandHandler("notifyshow", notify.notifyShow, pass_args=True))
    telegram.dispatcher.add_handler(CommandHandler("notifymovie", notify.notifyMovie, pass_args=True))
    #Admin-Only
    telegram.dispatcher.add_handler(CommandHandler("getaccess", admin.getAccess))
    telegram.dispatcher.add_handler(CommandHandler("setaccess", admin.setAccess, pass_args=True))
    telegram.dispatcher.add_handler(CommandHandler("forceupdate", admin.forceUpdate, pass_args=True))
    #CallbackQuery Handlers
    telegram.dispatcher.add_handler(CallbackQueryHandler(admin.getAccessCallback, pattern="^"+constants.ADMIN_GETACCESS_CALLBACK))

    logging.getLogger(__name__).info("Telegram command handlers initialized")
