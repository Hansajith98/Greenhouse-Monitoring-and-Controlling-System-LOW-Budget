from numpy import rint
import pandas as pd

df = pd.read_csv('Crop_recommendation.csv')

df.sort_values(
    by = ['label'],
    axis = 0, 
    inplace=True
)

# df_apple = df[df['label'] == 'apple']
# df_banana = df[df['label'] == 'banana']
# df_blackgram = df[df['label'] == 'blackgram']
# df_chickpea = df[df['label'] == 'chickpea']
# df_coconut = df[df['label'] == 'coconut']
# df_coffee = df[df['label'] == 'coffee']
# df_grapes = df[df['label'] == 'grapes']
# df_cotton = df[df['label'] == 'cotton']
# df_jute = df[df['label'] == 'jute']
# df_kidneybeans = df[df['label'] == 'kidneybeans']
# df_lentil = df[df['label'] == 'lentil']
# df_maize = df[df['label'] == 'maize']
# df_mango = df[df['label'] == 'mango']
# df_mothbeans = df[df['label'] == 'mothbeans']
# df_mungbean = df[df['label'] == 'mungbean']
# df_muskmelon = df[df['label'] == 'muskmelon']
# df_orange = df[df['label'] == 'orange']
# df_papaya = df[df['label'] == 'papaya']
# df_pigeonpeas = df[df['label'] == 'pigeonpeas']
# df_pomegranate = df[df['label'] == 'pomegranate']
# df_rice = df[df['label'] == 'rice']
# df_watermelon = df[df['label'] == 'watermelon']


final_data = pd.DataFrame()


for label in df['label'].unique():
    final_data = pd.concat( [final_data, df[df['label'] == label].sample(n=10)] )


final_training_data = df.drop( final_data.index )
print(final_training_data.shape)
print( final_data.shape )

final_data.to_csv('final predicting data.csv', index=False)
final_training_data.to_csv('crop recommondation train data.csv', index=False)