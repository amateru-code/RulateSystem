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
    cfg = get_cfg()
    liker = RulateLiker(cfg.get('login'), cfg.get('password'), cfg.get('book'), cfg.get('webdriver'), headless=True)
    # TODO: add function: left comment at the book page 'liked all chapter. add me some karma pls'
    # TODO: add multiprocessing


if __name__ == "__main__":
    main()
