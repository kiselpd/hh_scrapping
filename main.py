from source.hh_scrapping import HH
from pprint import pprint

def main():
    api = HH()

    json_vacancy = api.get_vacancy(areas=[1, 2], text="Python Django Flask")

    with open("vacancy.json", "w") as my_file:
        my_file.write(json_vacancy)


if __name__ == "__main__":
    main()