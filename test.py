import pandas as pd
import os

directory = os.path.join(os.getcwd() + '/Tagesschau_archive')  # get current directory
csv_path = directory + '/' + '2006-03-01_Tagesschau.csv'

frame = pd.read_csv(csv_path)
print(frame.index.values.max())
data = {'date': 'test', 'topline': 'test', 'headline': 'test', 'content': 'test'}
text = pd.DataFrame(data, index = [0])
text.to_csv(csv_path, mode = 'a', index=False, header=False)
print(frame)
print(type(frame.get('date')))
print(type(frame.get('date').values))
print('31.03.2006 20:32 Uhr' in frame.get('date').values)
print(pd.read_csv(csv_path))

