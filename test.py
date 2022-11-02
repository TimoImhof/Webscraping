import pandas as pd
import os

directory = os.path.join(os.getcwd() + '/AP_News_archive')  # get current directory
csv_path = directory + '/' + 'test'

new_article_frame = pd.DataFrame({'time': 'a-time', 'headline': 'a-headline', 'text': 'the-text'}, index=[0])
new_article_frame.to_csv(csv_path, index=False, header=True)

existing_csv = pd.read_csv(csv_path)

print(existing_csv.get('time').values)


new_row = pd.DataFrame({'time': 'a-untz', 'headline': 'h-untz', 'text': 'the-untz'}, index=[0])
new_row.to_csv(csv_path, mode='a', index=False, header=False)

'''
data = {'date': 'test', 'topline': 'test', 'headline': 'test', 'content': 'test'}
text = pd.DataFrame(data, index = [0])
text.to_csv(csv_path, mode = 'a', index=False, header=False)
print(frame)
print(type(frame.get('date')))
print(type(frame.get('date').values))
print('31.03.2006 20:32 Uhr' in frame.get('date').values)
print(pd.read_csv(csv_path))'''

