from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pyrebase
import pandas as pd
import numpy as np
import json

from greenhouse.decorators import login_necessary
from configFiles.config import config
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

green_house_Id = 'greenhouse1'

@login_necessary()
def index(request, greenhouse):
    global green_house_Id
    green_house_Id = greenhouse
    return render(request, 'index.html')

@login_necessary()
def update_controller(request):
    if (request.method == 'GET'):
        fan_status = int(request.GET.get('Fan')) if request.GET.get('Fan') != None else None
        ac_status = int(request.GET.get('AC')) if request.GET.get('AC') != None else None
        if fan_status != None:
            database.child("Controller").child(green_house_Id).child("Fan").set(fan_status)
        if ac_status != None:
            database.child("Controller").child(green_house_Id).child("AC").set(ac_status)
    return HttpResponse("Accepted", content_type='text/plain') 


def retrieve_sensor_dataframe():
    all_data = database.child("Sensor").get()
    dataframe = pd.DataFrame.from_dict(all_data.val()).T
    dataframe.reset_index(inplace=True)
    dataframe.rename(columns={"index": "Date"}, inplace=True)
    dataframe["DateinNumbers"] = pd.to_datetime(dataframe["Date"])
    return dataframe


def retrieve_controller_dictionary():
    all_data = database.child("Controller").child(green_house_Id).get()
    return all_data.val()


def send_dashboard_data(request):
    fire_dataframe = retrieve_sensor_dataframe()

    chart_data, labels = get_data_from_dataframe(
        fire_dataframe, ["Temperature", "Humidity"], "Date")
    controller_data = retrieve_controller_dictionary()

    return JsonResponse({
        'title': f'chart',
        'data': {
            'labels': labels,
            'datasets': {
                'label': 'Temperature (C)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': {
                    'Temperature': chart_data[0],
                    'Humidity': chart_data[1]
                },
            }
        },
        'controllers': {
            'Fan': controller_data['Fan'],
            'AC': controller_data['AC']
        },
    })


def get_data_from_dataframe(df, chart_data, labels, aggfunc=np.sum, round_values=0, fill_value=0):
    pivot = pd.pivot_table(
        df,
        values=chart_data,
        columns=labels,
        aggfunc=aggfunc,
        fill_value=0
    )
    
    pivot = pivot.round(round_values)

    values = pivot.values.tolist()
    labels = pivot.columns.tolist()

    return values, labels
