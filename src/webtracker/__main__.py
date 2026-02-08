from webtracker.main import run


if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        log(f'Application was stopped with keyboard interrupt.')

    except Exception as err:
        error(f'Application stopped with following: {err}')