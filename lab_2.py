from spyre import server
import pandas as pd

# Завантаження даних VHI
vhi_data = pd.read_csv("vhi_data/vhi_data.csv")

class VhiAnalysisApp(server.App):
    title = "Аналіз VHI для областей України"

    inputs = [
        {
            "type": "dropdown",
            "label": "Часовий ряд",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": "vhi_type"
        },
        {
            "type": "dropdown",
            "label": "Область",
            "options": [
                {"label": region, "value": region} for region in vhi_data['Назва'].unique()
            ],
            "key": "region"
        },
        {
            "type": "slider",
            "label": "Інтервал тижнів",
            "key": "weeks_interval",
            "value": [1, 52],
            "min": 1,
            "max": 52
        }
    ]

    tabs = ["Таблиця", "Графік"]

    controls = [
        {
            "type": "button",
            "label": "Оновити",
            "id": "update-button"
        }
    ]

    outputs = [
        {
            "type": "table",
            "id": "table-output",
            "control_id": "update-button",
            "tab": "Таблиця",
        },
        {
            "type": "plot",
            "id": "plot-output",
            "control_id": "update-button",
            "tab": "Графік"
        }
    ]

    def getData(self, params):
        selected_region_data = vhi_data[(vhi_data['Назва'] == params['region'])]
        filtered_data = selected_region_data[
            (selected_region_data['Тиждень'] >= params['weeks_interval'][0]) &
            (selected_region_data['Тиждень'] <= params['weeks_interval'][1])
        ]
        return filtered_data

    def getPlot(self, params):
        df = self.getData(params)
        df = df[['Тиждень', params['vhi_type']]

        plt_obj = df.plot(x='Тиждень', y=params['vhi_type'], title=f"{params['vhi_type']} для {params['region']}")
        plt_obj.set_ylabel(params['vhi_type'])

        return plt_obj

app = VhiAnalysisApp()
app.launch()
