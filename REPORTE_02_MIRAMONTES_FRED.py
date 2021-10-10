# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 19:32:07 2021

@author: lilol
"""
#se importa la clase csv para utilizar sus metodos, asi como pandas con el alias pd.
import csv
import pandas as pd

#se crea una lista vacia para almacenar los datos del csv
data_list = []
#se abre el csv para su lectura con un alias
with open("synergy_logistics_database.csv", "r") as synergy:
    synergy_reader = csv.reader(synergy)
    #se vacia el csv a la lista previamente creada
    for synergy_data in synergy_reader:
        data_list.append(synergy_data)

#se crea un metodo que se le envia direction como parametro "Imports/Exports"
def imports_exports(direction):
    #se crea un contador
    count = 0
    #se crean las listas  
    imports_exports_count = []
    imports_exports = []
    #se recorren los datos de data_list  
    for route in data_list:
        #si route[1](direction del csv) es igual a direction(parametro)
        if route[1] == direction:
            #se almacena el origin y destiny
            imports_exports_route = [route[2],route[3]]
            #si las rutas no se encuentran en la lista
            if imports_exports_route not in imports_exports:
                #se recorren los datos del data list
                for data_imports_exports in data_list:
                    #si la ruta se encuentra en data_imports_exports
                    if imports_exports_route == [data_imports_exports[2],data_imports_exports[3]]:
                        #el contador incrementa en 1
                        count += 1
                #se almacena la ruta en la lista imports_exports
                imports_exports.append(imports_exports_route)
                #se almacenan las rutas y el contador en imports_exports_count
                imports_exports_count.append([route[2],route[3],count])
                #el contador se resetea a 0 para la siguiente vuelta
                count = 0
    #al finalizar el ciclo for se ordenan los datos de la lista imports_exports_count 
    imports_exports_count.sort(reverse = True, key = lambda x:x[2])
    #se crea un dataframe con pandas y se renombran las columnas
    df_imports_exports=pd.DataFrame(imports_exports_count[:10], columns =["Origin","Destiny","Total"])
    #se retorna el dataframe
    return df_imports_exports

#se crea un metodo que se le envia direction como parametro "Imports/Exports"
def transports_imports_exports(direction):
    #se crean las listas
    transports_imports_exports = []
    sea_transports = []
    air_transports = []
    rail_transports = []
    road_transports = []
    #se recorre la data_list
    for route in data_list:
        #si route[1](direction del csv) es igual a direction(parametro)
        if route[1] == direction:
            #se almacena transport_mode y total_value a la lista transports_imports_exports
            transports_imports_exports.append([route[7],int(route[9])])
    #se recorre la lista transports_imports_exports
    for transport in transports_imports_exports:
        #si transport[0](transport_mode del csv) es igual a x transporte se almacenara 
        #el transport[1](total_value del csv) en su respectiva lista
        if transport[0] == "Sea":
            sea_transports.append(transport[1])    
        elif transport[0] == "Air":
            air_transports.append(transport[1])
        elif transport[0] == "Rail":
            rail_transports.append(transport[1])        
        elif transport[0] == "Road":
            road_transports.append(transport[1])
    
    #se crea una variable total_x que almacenara la suma total de x transporte
    total_sea = sum(sea_transports)    
    total_air = sum(air_transports)
    total_rail = sum(rail_transports)
    total_road = sum(road_transports)

    #se crea una lista que almacena todos los datos procesados para x transporte          
    import_export_transports = [["Air",total_air],["Rail",total_rail],["Road",total_road],["Sea",total_sea]]
    #se ordenan los datos de la lista
    import_export_transports.sort(reverse = True, key = lambda x:x[1])
    #se crea un dataframe con pandas limitando la consulta a 
    #3 valores (los cuales se piden en el documento del reporte) renombrando las columnas
    df_transport =pd.DataFrame(import_export_transports[:3], columns = ["Transports","Total"])
    #se retorna el dataframe
    return df_transport

#se crea un metodo que se le envia direction como parametro "Imports/Exports"
def imports_exports_most_value(direction):
    #exports = 2, imports 3
    #se crea una variable que almacenara la posicion 2 si es "Exports" y 
    #3 si es "Imports" dependiendo del valor ingresado como parametro "direction"
    most_value_route = 0
    most_value_route = 2 if direction == "Exports" else most_value_route+3
    #se crean las listas
    countries = []
    imports_exports_most_value =[]
    country_imports_exports =[]
    country_value= []
    #se recorre la data_list
    for route in data_list:
        #si route[1](direction del csv) es igual a direction(parametro)      
        if route[1] == direction:
            #se almacenara el valor en la lista country_value
            country_value.append(int(route[9]))
            #se almacenara el origin/destination dependiendo de si es 2 "origin" o 3 "destination"
            #(para esto se utilizo la variable most_value_route que si el parametro ingresado era exports esta variable seria 2 caso contrario 3)
            #en la lista country_imports_exports
            country_imports_exports.append(route[most_value_route])
            #se recorren los datos de la lista country_imports_exports
            for country in country_imports_exports:
                #si el valor no se encuentra en la lista countries
                if country not in countries:
                    #se almacenara la ruta en countries
                    countries.append(route[most_value_route])
    #se almacenara la suma de los datos de la lista country_value en la variable total 
    total = sum(country_value)
    #se realizara un recorrido hasta el tamaño total de la lista countries
    for count_countries in range(len(countries)):
        #se inicializan el contador y la suma a 0
        country_count = 0
        country_sum = 0
        #se inicia un recorrido hasta el tamaño de la lista country_imports_exports
        for import_export_countries in range(len(country_imports_exports)):
            #si country_imports_exports en la posicion x es igual a countries en la posicion x
            if country_imports_exports[import_export_countries] == countries[count_countries]:
                #se incrementara el contador en 1 
                country_count = country_count + 1
                #se sumara el valor de country_value en la posicion x a la variable country_sum
                country_sum = country_sum + country_value[import_export_countries]
        #se agregaran los datos obtenidos en la lista imports_exports_most_value
        imports_exports_most_value.append([countries[count_countries],country_count, country_sum,((country_sum*100)/total)])
    #se ordenara la lista
    imports_exports_most_value.sort(reverse = True, key = lambda x:x[2])
    #se creara un dataframe con los valores renombrando las columnas dependiendo de si es import o export
    if(most_value_route == 2):
        df_total = pd.DataFrame(imports_exports_most_value[:8], columns = ["Country export","Count"," Value","Percent"])
    else:
        df_total = pd.DataFrame(imports_exports_most_value[:7], columns = ["Country import","Count"," Value","Percent"])
    #se retorna el dataframe
    return df_total

exit = 0
while(exit != 1):
    try:         
        option = int(input("--------Principal menu-------\n1 - Imports option\n2 - Exports option\n3 - Exit\nSelect your option:\n"))
        if option == 1:
            exit_import = 0
            while(exit_import != 1):
                try:
                    import_option = int(input("--------Imports menu-------\n1 - Top 10 import routes.\n2 - 3 most important transport for import\n3 - 80% most important countries for import\n4 - Exit\n"))
                    if(import_option == 4):
                        print("Going back to the previous menu...")
                        exit_import = 1
                    elif(import_option == 1):
                        print("Loading top 10 imports...")
                        print(imports_exports("Imports"))
                    elif(import_option == 2):
                        print("Loading most import transports...")
                        print(transports_imports_exports("Imports"))
                    elif(import_option == 3):
                        print("Loading 80% most important countries for import...")
                        print(imports_exports_most_value("Imports"))
                    else:
                        print("Error: only options 1 to 4 available")
                except:
                    print("Error: enter only numbers")
        elif option == 2:
            exit_export = 0
            while(exit_export != 1):
                try:
                    export_option = int(input("--------Exports menu-------\n1 - Top 10 export routes.\n2 - 3 most important transport for export\n3 - 80% most important countries for export\n4 - Exit\n"))
                    if(export_option == 4):
                        print("Going back to the previous menu...")
                        exit_export = 1
                    elif(export_option == 1):
                        print("Loading top 10 exports..")
                        print(imports_exports("Exports"))
                    elif(export_option == 2):
                        print("Loading most export transports...")
                        print(transports_imports_exports("Exports"))
                    elif(export_option == 3):
                        print("Loading 80% most important countries for export...")
                        print(imports_exports_most_value("Exports"))
                    else:
                        print("Error: only options 1 to 4 available")
                except:
                    print("Error: enter only numbers")
        elif option == 3:
            print("Goodbye!")
            exit = 1
        else:
            print("Error: options are from 1 to 3")
    except:
        print("Error: enter only numbers")
