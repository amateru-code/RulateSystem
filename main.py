import rulate_config
from RulateLiker import RulateLiker


def get_cfg():
    return {
        'login': f'{rulate_config.rulate_login}',
        'password': f'{rulate_config.rulate_psw}',
        'book': f'{rulate_config.book}',
        'webdriver': f'{rulate_config.webdriver_url}'
    }


def main():
    # added stars putting
    cfg = get_cfg()
    action_cfg ={
        'like': True,
        'thx': True,
        'thx_amount': 999999,
        'stars': True,
        'stars_value': 5
    }
    liker = RulateLiker(cfg.get('login'), cfg.get('password'), cfg.get('book'), cfg.get('webdriver'),
                        headless=False,
                        actions=action_cfg)


if __name__ == "__main__":
    main()


# TODO: add function: left comment at the book page 'liked all chapter. add me some karma pls'
# TODO: add multiprocessing
# TODO: maybe another project(create auto gmail creator and confirmation of creating rulate account with email)
# TODO: remake like counter to reload terminal just a new line instead of printing it above the last line
# TODO: add telegram bot to use this piece of shit with no IDE and all that shit i need to do every time
