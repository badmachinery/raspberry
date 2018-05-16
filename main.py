import logging

import actions
import scripts

def main():
    logging.basicConfig(level=logging.DEBUG, filemode="w")
    actions.main_cycle()
    '''
    try:
        actions.main_cycle()
    except Exception:
        print(str(Exception))
        scripts.do_break()
    '''

if __name__ == "__main__":
    main()
