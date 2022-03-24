from typing import final
import pandas as pd

df = pd.read_csv('Final Data csv beforre max and min.csv')


final_data = pd.DataFrame()

print( df['label'].unique() )

for label in df['label'].unique():
    single_crop_data = df[ df['label'] == label ]

    max = single_crop_data.drop(['label'], axis=1).max(axis=0)
    max = max.to_frame().T
    max['label'] = [label]
    max['type'] = ['max']

    min = single_crop_data.drop(['label'], axis=1).min(axis=0)
    min = min.to_frame().T
    min['label'] = [label]
    min['type'] = ['min']

    final_data = pd.concat( [final_data, max, min] )

final_data.reset_index(drop=True, inplace=True)
final_data.to_csv('min max threshoulders.csv', index=False)

print( final_data.head() )

