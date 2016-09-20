from django.http import HttpResponse
from django.shortcuts import render
from bokeh.models.widgets import Button, RadioButtonGroup, Select
from bokeh.resources import CDN
from bokeh.embed import components

def search(request):
    return HttpResponse("file=%s, state=%s", file, state)

def hello_world(request):
    return render(request,'home.html')

from bokeh.plotting import figure
from bokeh.charts import Bar
import pandas as pd
import os

def hai_state(data,state):
    remove = ["HAI_1_CI_LOWER","HAI_1_CI_UPPER","HAI_1a_CI_LOWER","HAI_1a_CI_UPPER","HAI_2_CI_LOWER","HAI_2_CI_UPPER","HAI_2a_CI_LOWER","HAI_2a_CI_UPPER","HAI_3_CI_LOWER","HAI_3_CI_UPPER","HAI_4_CI_LOWER","HAI_4_CI_UPPER","HAI_5_CI_LOWER","HAI_5_CI_UPPER","HAI_6_CI_LOWER","HAI_6_CI_UPPER"]
    for rm in remove:
         data = data[data.Measure_ID != rm]
    return Bar(data, 'Measure_ID', values='Score', legend=False, title=' '.join(('Healthcare Associated Infections in',state)), xlabel = 'Measure', ylabel = 'Score', width=1000)

def interim(request,file):
    return render(request, "interim.html")

def simple_chart(request,file,state):
    import csv
    
#    file = request.GET.get('file','')
#    state = request.GET.get('state','')
    state = state.upper()
    directory = "/Users/andrewmcconnell/Desktop/HealthcareApp/Hospital_Revised_Flatfiles"
    with open(os.path.join(directory, "file_directory.csv"),'r') as f:
        d = [row for row in csv.reader(f.read().splitlines())]
    info = []
    for item in d:
        if item[0] == file:
            info = item

    csv = info[4]
    f = open(os.path.join(directory, csv), "r")
    data = pd.read_csv(f)
    data = data[data.State == state]
    p = globals()[info[5]](data,state)
    
    script, div = components(p, CDN)

    return render(request, "simple_chart.html", {"tab": info[1], "title": info[2],"state": state, "desc": info[3], "the_script": script, "the_div": div})
