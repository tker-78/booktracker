import configparser

conf = configparser.ConfigParser()
conf.read("./settings.ini")

secret_key = conf["auth"]["SECRET_KEY"]
algorithm = conf["auth"]["ALGORITHM"]
access_token_expire_minutes = int(conf["auth"]["ACCESS_TOKEN_EXPIRE_MINUTES"])


