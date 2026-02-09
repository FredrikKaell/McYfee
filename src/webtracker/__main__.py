from webtracker.main import run


if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        print(f'Application was stopped with keyboard interrupt.')

    except Exception as err:
        print(f'Application stopped with following: {err}')