from modules.data import DATA_LIST


def main():
    for show in DATA_LIST:
        print(show.show_name, show.remote_dir, show.timings)

if __name__ == '__main__':
    main()
