from spyre import server
import pandas as pd
import urllib.request
import requests
import os
import datetime
import seaborn as sns
import matplotlib.pyplot as plt


def download_files():
    df_all = pd.DataFrame()
    for ids in range(1, 28):
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={ids}&year1=1981&year2=2024&type=Mean"
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists('vhi'):
                os.mkdir('vhi')
                print(f'The folder is created')
            date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            vhi_url = urllib.request.urlopen(url)
            file_name = fr'vhi\vhi_id_{ids}_{date_now}.csv'
            out = open(file_name, 'wb')
            out.write(vhi_url.read())
            out.close()
            print(f"VHI from id {ids} was downloaded at {date_now}")
            headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
            df = pd.read_csv(file_name, header=1, names=headers, skiprows=1)[:-1]
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df['area'] = int(file_name.split("_")[2])
            df = df.drop(columns=['empty'])
            df_all = pd.concat([df_all, df]).drop_duplicates().reset_index(drop=True)
        else:
            print('An error occurred')
            break
    df_all.to_csv(r'vhi\df_all.csv', index=False)

#read df
def read_csv_data(file_name):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'area']
    df_all = pd.read_csv(file_name, header=1, names=headers, delimiter=',')
    df_all['Year'] = df_all['Year'].astype(int)
    df_all['Week'] = df_all['Week'].astype(int)
    df_all['area'] = df_all['area'].astype(int)
    return df_all


class StockExample(server.App):
    title = "NOAA data vizualization"
    inputs = [{
        'type': 'dropdown',
        'label': 'NOAA data dropdown',
        'options': [
            {'label': 'VCI', 'value': 'VCI'},
            {'label': 'TCI', 'value': 'TCI'},
            {'label': 'VHI', 'value': 'VHI'}
        ],
        'value': 'VCI',
        'key': 'noaa',
        'action_id': 'update_data'
    },
        {
            'type': 'dropdown',
            'label': 'Regions of Ukraine',
            'options': [
                {'label': 'Cherkasy', 'value': '1'},
                {'label': 'Chernihiv', 'value': '2'},
                {'label': 'Chernivtsi', 'value': '3'},
                {'label': 'Crimea', 'value': '4'},
                {'label': 'Dnipropetrovs\'k', 'value': '5'},
                {'label': 'Donets\'k', 'value': '6'},
                {'label': 'Ivano-Frankivsk', 'value': '7'},
                {'label': 'Kharkiv', 'value': '8'},
                {'label': 'Kherson', 'value': '9'},
                {'label': 'Khmel\'nyts`kyy', 'value': '10'},
                {'label': 'Kiev', 'value': '11'},
                {'label': 'Kiev City', 'value': '12'},
                {'label': 'Kirovohrad', 'value': '13'},
                {'label': 'Luhans\'k', 'value': '14'},
                {'label': 'L\'viv', 'value': '15'},
                {'label': 'Mykolayiv', 'value': '16'},
                {'label': 'Odessa', 'value': '17'},
                {'label': 'Poltava', 'value': '18'},
                {'label': 'Rivne', 'value': '19'},
                {'label': 'Sevastopol\'', 'value': '20'},
                {'label': 'Sumy', 'value': '21'},
                {'label': 'Ternopil\'', 'value': '22'},
                {'label': 'Transcarpathia', 'value': '23'},
                {'label': 'Vinnytsya', 'value': '24'},
                {'label': 'Volyn', 'value': '25'},
                {'label': 'Zaporizhzhya', 'value': '26'},
                {'label': 'Zhytomyr', 'value': '27'}
            ],
            'value': '12',
            'key': 'regions',
            'action_id': 'update_data'
        },
        {
            'type': 'text',
            'label': 'Week range (1-52): '
                     '<br><small>It is necessary to indicate in the format through a hyphen without a space</small>',
            'value': '1-52',
            'key': 'range',
            'action_id': 'update_data'
        },
        {
            'type': 'text',
            'label': 'Year',
            'value': '2000',
            'key': 'year',
            'action_id': 'update_data'
        },
        {
            'type': 'dropdown',
            'label': 'Show numbers',
            'options': [
                {'label': 'Yes', 'value': 'yes'},
                {'label': 'No', 'value': 'no'},
            ],
            'value': 'no',
            'key': 'show_num',
            'action_id': 'update_data'
        }
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ['Plot', 'Table']

    outputs = [{
        'type': 'plot',
        'id': 'plot',
        'control_id': 'update_data',
        'tab': 'Plot'
    },
        {
            'type': 'table',
            'id': 'table_id',
            'control_id': 'update_data',
            'tab': 'Table',
            'on_page_load': True
        }]

    def __init__(self):
        self.data_plot = None

    def getData(self, params):
        selected_noaa = params['noaa']
        selected_region = int(params['regions'])
        selected_range = params['range']
        selected_year = int(params['year'])

        df_all = read_csv_data(r'vhi\df_all.csv')
        diapason_min, diapason_max = map(int, selected_range.split("-"))
        df = df_all[(df_all['area'] == selected_region) &
                    (df_all['Year'] == selected_year) &
                    (df_all['Week'] >= diapason_min) &
                    (df_all['Week'] <= diapason_max)][[selected_noaa, 'Year', 'Week', 'SMN', 'SMT']]
        return df

    def getPlot(self, params):
        selected_noaa = params['noaa']
        data = self.getData(params)
        df = data.drop(columns=['Year', 'SMN', 'SMT'], axis=1)

        sns.set_style("darkgrid")
        plt.figure(figsize=(14, 9))
        with sns.color_palette("Set2"):
            fig = sns.lineplot(data=df, x='Week', y=selected_noaa, zorder=1)

        plt.scatter(df['Week'], df[selected_noaa], marker='*', s=50, color=sns.color_palette("Set2")[1], zorder=2)

        if params['show_num'] == 'yes':
            for index, row in df.iterrows():
                plt.text(row['Week'], row[selected_noaa], str(row[selected_noaa]), ha='right', va='bottom')
        return fig


if __name__ == '__main__':
    if os.path.exists(r'vhi\df_all.csv'):
        app = StockExample()
        app.launch(port=5005)
    else:
        download_files()
        app = StockExample()
        app.launch(port=5005)
