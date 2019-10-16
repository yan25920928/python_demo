import logging
logging.basicConfig(level=logging.DEBUG)

def foo(s):
    n= int(s)
    logging.debug("n=%d"%n)
    return 10/n

def main():
    foo('2')

if __name__ == '__main__':
    main()
