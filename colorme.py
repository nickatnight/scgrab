class ColorMe:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def color_text(cls, txt, status):
        if status == 'fail':
            print cls.FAIL + txt + cls.ENDC
        elif status == 'ok':
            print cls.OKGREEN + txt + cls.ENDC
