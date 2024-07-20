from django.db import migrations
from csv import reader
#from todoapp.models import Region, Comuna

def add_region_data(apps, schema_editor):
    file = open("todoapp/regiones-chile.csv",'r',encoding = "utf-8")
    lista = reader(file,delimiter=';')
    # comunas = {}
    Comuna = apps.get_model("todoapp","Comuna")
    Region = apps.get_model("todoapp","Region")
    regiones = []
    
    for row in lista:
        reg = row[0]
        com = row[3]
        
        if(reg not in regiones):
            regi = Region(region = reg)
            regi.save()
            regiones.append(reg)
        nueva = Comuna( comuna = com)
        nueva.save()
        nueva.region.add(regi)

class Migration(migrations.Migration):

    dependencies = [
        ("todoapp","0002_comuna_region")
    ]
    operations=[
        migrations.RunPython(add_region_data),
    ]

