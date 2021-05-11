import pandas as pd

def ler_excel():
    df = pd.read_excel('c:/Users/Alan/Documents/magic/Magic_ML.xlsx')
    return df

if __name__ == "__main__":
    print(ler_excel())
