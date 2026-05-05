from Convertors import Resistor

def main():
    r = Resistor()
    band, results = r.Run()

    print(band, results, sep="\n")



if __name__ == "__main__":
    main()

