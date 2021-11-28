import pandas as pd

df = pd.read_csv('../data/raw/1_Combined_Player_Per90_Cleaned.csv')
df = df[['PlayerID','Player','Nation','Season','Squad','Gls','G-xG','SCA','Ast','xA','TklW','Int_x','Pressures: Succ','Clr','Won']].rename(columns={'Pressures: Succ': 'PressuresSucc', 'Int_x': 'Int', 'Won': 'AerialDuelsWon'})

for col in ['Gls','G-xG','SCA','Ast','xA','TklW','PressuresSucc','Int','AerialDuelsWon']:
    min_ = df[col].min()
    max_ = df[col].max()
    df[col] = (df[col] - min_) / (max_ - min_) * 100

df.to_csv('../data/output/Player_Per90_scaled.csv')