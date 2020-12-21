from utils.parser import Parser

if __name__ == "__main__":
    data_path = "../assets/"
    parser = Parser(data_path).getInstance()
    parking_container = parser.read_parking_container()