import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv
import os
import pandas as pd
import re
from datetime import datetime as datetime2

class Grid:
    def __init__(self, parent):
        self.parent = parent
        parent.title("Calendario ")
        parent.geometry("1200x800+100+100")
        self.dia_semana=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        self.meses=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.create_grid()
        
    def create_grid(self):
        """Funcion que crea todo el grid de la aplicacion, define el dia de hoy e identifica el mes y el año.
           Crea la primera semana y los botones para cambiar de semana"""
        self.grid_frame = tk.Frame(self.parent)
        self.grid_frame2 = tk.Frame(self.parent, pady=30)
        self.grid_frame2.grid_rowconfigure(0, weight=1)
        self.grid_frame2.grid_columnconfigure(0, weight=1)
        self.grid_frame.pack()
        self.grid_frame2.pack()
        
        self.hoy=datetime.date.today()
        self.hoy=(self.hoy - datetime.timedelta(days=self.hoy.weekday()))
        self.mes=self.hoy.month
        self.año=self.hoy.year
        duracion_semana = datetime.timedelta(days=7)
        dias_semana = [self.hoy + datetime.timedelta(days=dia) for dia in range(7)]
        numeros_dias_semana = [dia.day for dia in dias_semana]
        definir_mes=[dias_semana[0].month, dias_semana[6].month ]
        self.semana_a_mes=True
        ttk.Button(self.grid_frame, text="<<", command=lambda: (self.semana_anterior(self.hoy, "<<"), self.tabla.destroy(), self.cargarcsv())).grid(row=0, column=0)
        ttk.Button(self.grid_frame, text=">>", command=lambda: (self.semana_anterior(self.hoy, ">>"), self.tabla.destroy(), self.cargarcsv())).grid(row=0, column=6)
        ttk.Button(self.grid_frame, text="Ver meses" if self.semana_a_mes else "Ver semanas", command=lambda: self.crear_meses(self.mes, self.año)).grid(row=0, column=7)
        
        if definir_mes[0]!=definir_mes[1]:
            label=tk.Label(self.grid_frame, text=f"{self.meses[definir_mes[0]-1]} - {self.meses[definir_mes[1]-1]}", borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
        else:
            label=tk.Label(self.grid_frame, text=self.meses[self.mes - 1], borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
        for row in range(1):
            for col in range(7):
                label = tk.Label(self.grid_frame, text=self.dia_semana[col], borderwidth=1, relief="solid", width=15)
                label.grid(row=row+1, column=col)
        self.crear_semana(numeros_dias_semana ,dias_semana, label)
        self.filtrado()
        self.cargarcsv()


    

    def filtrado(self):
        """La funcion esta atenta para cuando aprietas el enter en el Entry entrada,
           lo que activa el filtrado de recordatorios"""
        def cambios(event):
            self.tabla.destroy()
            self.cargarcsv()

        self.filtrar=tk.StringVar()
        entrada=ttk.Entry(self.grid_frame2, textvariable=self.filtrar)
        entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_frame2.columnconfigure(0, weight=1)
        entrada.bind("<Return>", cambios)

    def crear_meses(self, mes, año):
        """Funcion que crea los meses y los botones para navegar entre ellos"""
        self.semana_a_mes=False
        if self.tabla:
            self.tabla.destroy()
            self.cargarcsv()
        dias_mes=[]
        inicio=datetime.date(año, mes, 1)
        self.hoy=inicio
        inicio=(inicio - datetime.timedelta(days=inicio.weekday()))
        nuevo_mes= True
        index=0
        while nuevo_mes:
            dias_semana = [self.hoy + datetime.timedelta(days=dia) for dia in range(7)]
            numeros_dias_semana = [dia.day for dia in dias_semana]
            dias_mes.append([inicio + datetime.timedelta(days=dia) for dia in range(8)])
            definir_mes=[dias_mes[index][0].month, dias_mes[index][7].month ]
            if definir_mes[0]!=definir_mes[1]:
                label=tk.Label(self.grid_frame, text=f"{self.meses[self.mes - 1]}", borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
            else:
                label=tk.Label(self.grid_frame, text=self.meses[self.mes - 1], borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
            ttk.Button(self.grid_frame, text="<<", command=lambda: (self.mes_anterior(self.hoy, "<<"), self.tabla.destroy(), self.cargarcsv())).grid(row=0, column=0)
            ttk.Button(self.grid_frame, text=">>", command=lambda: (self.mes_anterior(self.hoy, ">>"), self.tabla.destroy(), self.cargarcsv())).grid(row=0, column=6)
            ttk.Button(self.grid_frame, text="Ver semanas", command=lambda: self.crear_semana(numeros_dias_semana, dias_semana, label)).grid(row=0, column=7)
            if (index!=0) & (definir_mes[0]!=definir_mes[1]) :
                nuevo_mes=False
            else:
                inicio=inicio + datetime.timedelta(days=7)
                index=index+1
        for row in range(len(dias_mes)):
            for col in range(7):
                label = tk.Label(self.grid_frame, text=dias_mes[row][col].day, bg="lightblue", borderwidth=1, relief="solid", width=15)
                label.grid(row=row+2, column=col)
                label.bind("<Button-1>", lambda event, arg=dias_mes[row][col]: self.crearEvento(event, arg))
                
    
    def crear_semana(self, numeros_dias_semana, dias_semana, label):
        "Funcion que crea las semanas"
        if self.semana_a_mes==False:
            self.semana_a_mes=True
            self.tabla.destroy()
            self.cargarcsv()
        
        self.hoy=(self.hoy - datetime.timedelta(days=self.hoy.weekday()))
        dias_semana = [self.hoy + datetime.timedelta(days=dia) for dia in range(7)]
        numeros_dias_semana = [dia.day for dia in dias_semana]
        for index in range(6):
            grids=self.grid_frame.grid_slaves(row=index+2)
            for grid in grids:
                grid.grid_forget()
        ttk.Button(self.grid_frame, text="<<", command=lambda: (self.semana_anterior(self.hoy, "<<"), self.tabla.destroy(), self.cargarcsv())).grid(row=0, column=0)
        ttk.Button(self.grid_frame, text=">>", command=lambda: (self.semana_anterior(self.hoy, ">>"), self.tabla.destroy(), self.cargarcsv())).grid(row=0, column=6)
        ttk.Button(self.grid_frame, text="Ver meses", command=lambda: self.crear_meses(self.mes, self.año)).grid(row=0, column=7)

        for row in range(1):
            for col in range(7):
                label = tk.Label(self.grid_frame, text=numeros_dias_semana[col], borderwidth=1, relief="solid", width=15)
                label.grid(row=row+2, column=col)
                label.bind("<Button-1>", lambda event, arg=dias_semana[col]: self.crearEvento(event, arg))

    def semana_anterior(self, dias, direccion):
        "Cambia entre semanas dependiendo de la direccion"
        self.semana_a_mes=True
        if direccion=="<<":
            self.hoy=dias - datetime.timedelta(days=7)
        else:
            self.hoy=dias + datetime.timedelta(days=7)
        self.mes=self.hoy.month
        dias_semana = [self.hoy + datetime.timedelta(days=dia) for dia in range(7)]
        numeros_dias_semana = [dia.day for dia in dias_semana]
        self.actualizar(dias_semana, numeros_dias_semana)
    
    def mes_anterior(self, dias, direccion):
        "Cambia entre mes dependiendo la direccion"
        if direccion=="<<":
            if self.hoy.month==1:
                self.hoy=self.hoy.replace(month=12)
                self.hoy=self.hoy.replace(year=self.hoy.year-1)
            else:
                self.hoy=self.hoy.replace(month=self.hoy.month-1)
            self.mes=self.hoy.month
            self.año=self.hoy.year
            self.crear_meses(self.mes, self.año)
        else:
            if self.hoy.month==12:
                self.hoy=self.hoy.replace(month=1)
                self.hoy=self.hoy.replace(year=self.hoy.year+1)
                self.mes=self.hoy.month
                self.año=self.hoy.year
                self.crear_meses(self.mes, self.año)
            else:
                self.hoy=self.hoy.replace(month=self.hoy.month+1)
                self.mes=self.hoy.month
                self.año=self.hoy.year
                self.crear_meses(self.mes, self.año)
  
    def actualizar(self, dias_semana, numeros_dias_semana):
        "Actualiza las semanas o meses cuando se cambia la fecha"
        definir_mes=[dias_semana[0].month -1 , dias_semana[6].month -1 ]
        if definir_mes[0]!=definir_mes[1]:
            label=tk.Label(self.grid_frame, text=f"{self.meses[definir_mes[0]]} - {self.meses[definir_mes[1]]}", borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
        else:
            label=tk.Label(self.grid_frame, text=self.meses[self.mes - 1], borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
        for row in range(1):
            for col in range(7):
                label = tk.Label(self.grid_frame, text=numeros_dias_semana[col], borderwidth=1, relief="solid", width=15)
                label.grid(row=row+2, column=col)
                label.bind("<Button-1>", lambda event, arg=dias_semana[col]: self.crearEvento(event, arg))
    
    def abrirEvento(self, event, arg):
        toplevel = tk.Toplevel(self.parent)
        VentanaEvento(toplevel, arg).grid()

    def crearEvento(self, event, arg):
        "Un formulario para la creacion de los recordatorios"
        horaactual=datetime.datetime.now().strftime("%H:%M:%S")
        self.toplevel = tk.Toplevel(self.parent)
        self.toplevel.title("Crear evento")
        self.titulo= tk.StringVar()
        self.hora= tk.StringVar(value=horaactual)
        self.duracion= tk.IntVar(value=1)
        self.descripcion= tk.StringVar()
        self.importancia= tk.StringVar(value="normal")
        self.etiquetas= tk.StringVar()
        self.fecha=arg

        ttk.Label(self.toplevel, text="Titulo", padding=3).grid(row=1, column=1)
        ttk.Entry(self.toplevel, textvariable=self.titulo).grid(row=1, column=2)
        ttk.Label(self.toplevel, text="Hora", padding=3).grid(row=2, column=1)
        ttk.Entry(self.toplevel, textvariable=self.hora).grid(row=2, column=2)
        ttk.Label(self.toplevel, text="Duracion", padding=3).grid(row=3, column=1)
        ttk.Entry(self.toplevel, textvariable=self.duracion).grid(row=3, column=2)
        ttk.Label(self.toplevel, text="Descripcion", padding=3).grid(row=4, column=1)
        ttk.Entry(self.toplevel, textvariable=self.descripcion).grid(row=4, column=2)
        ttk.Label(self.toplevel, text="Importancia", padding=3).grid(row=5, column=1)
        ttk.Combobox(self.toplevel, textvariable=self.importancia, values=["importante", "normal"], width=17).grid(row=5, column=2)
        ttk.Label(self.toplevel, text="Etiquetas", padding=3).grid(row=6, column=1)
        ttk.Entry(self.toplevel, textvariable=self.etiquetas).grid(row=6, column=2)
        
        btn_guardar = ttk.Button(self.toplevel, text="Guardar", padding=3, command=self.guardar)
        btn_guardar.grid(row=10, column=3)
        
    def evento_opciones(self, event2, info, row):
        "Añade a los recordatorios la opcion de eliminar y modificar"
        opciones=tk.Menu(self.parent)
        self.tabla.selection_clear()
        seleccion = self.tabla.identify_row(event2.y)
        if seleccion:
            self.tabla.selection_set(seleccion)
            opciones.add_command(label="Eliminar", command=lambda: self.eliminar_evento(info))
            opciones.add_command(label="Modificar", command=lambda: self.modificar_evento(row, info))
            opciones.post(event2.x_root, event2.y_root)

        
    def eliminar_evento(self, row):
        "Elimina los eventos"

        elemento= self.tabla.selection()[0]
        eliminar = [str(index) for index in self.tabla.item(elemento)["values"]]
        numero= re.search(r"I00(\d+)", elemento).group(1)
       

        with open("recordatorio.csv", newline="") as archivo:
            reader = csv.reader(archivo)
            datos=[row for row in reader]
        for fila in datos:
            if fila==eliminar:
                numero=datos.index(fila)
                print("ENCONTRADO")
        

        archivocsv=pd.read_csv("recordatorio.csv")
        print("225", archivocsv.iloc[int(numero)-1])

        archivocsv=archivocsv.drop(int(numero)-1)
        archivocsv=archivocsv.sort_values(by=['Fecha'])
        print(archivocsv)
        archivocsv.to_csv('recordatorio.csv', index=False)
        """ with open("recordatorio.csv", "w", newline="") as archivo:
            writer=csv.writer(archivo)
            writer.writerows(archivocsv) """
        self.tabla.destroy()
        self.cargarcsv()

    def modificar_evento(self, info, row):
        "Modifica el evento seleccionado"
        elemento= self.tabla.selection()[0]
        modificar = [str(index) for index in self.tabla.item(elemento)["values"]]
        numero= re.search(r"I00(\d+)", elemento).group(1)
        with open("recordatorio.csv", newline="") as archivo:
            reader = csv.reader(archivo)
            datos=[row for row in reader]
        for fila in datos:
            if fila==modificar:
                numero=datos.index(fila)
                print("ENCONTRADO")
        

        datos=datos[numero]
        print(datos)
        toplevel = tk.Toplevel(self.parent)
        self.titulo2= tk.StringVar(value=datos[0])
        self.hora2= tk.StringVar(value=datos[1])
        self.duracion2= tk.IntVar(value=datos[2])
        self.descripcion2= tk.StringVar(value=datos[3])
        self.importancia2= tk.StringVar(value=datos[4])
        self.etiquetas2= tk.StringVar(value=datos[5])
        self.fecha2=tk.StringVar(value=datos[6])

        ttk.Label(toplevel, text="Titulo", padding=3).grid(row=1, column=1)
        ttk.Entry(toplevel, textvariable=self.titulo2).grid(row=1, column=2)
        ttk.Label(toplevel, text="Hora", padding=3).grid(row=2, column=1)
        ttk.Entry(toplevel, textvariable=self.hora2).grid(row=2, column=2)
        ttk.Label(toplevel, text="Duracion", padding=3).grid(row=3, column=1)
        ttk.Entry(toplevel, textvariable=self.duracion2).grid(row=3, column=2)
        ttk.Label(toplevel, text="Descripcion", padding=3).grid(row=4, column=1)
        ttk.Entry(toplevel, textvariable=self.descripcion2).grid(row=4, column=2)
        ttk.Label(toplevel, text="Importancia", padding=3).grid(row=5, column=1)
        ttk.Entry(toplevel, textvariable=self.importancia2).grid(row=5, column=2)
        ttk.Label(toplevel, text="Etiquetas", padding=3).grid(row=6, column=1)
        ttk.Entry(toplevel, textvariable=self.etiquetas2).grid(row=6, column=2)
        ttk.Label(toplevel, text="Fechas", padding=3).grid(row=6, column=1)
        ttk.Entry(toplevel, textvariable=self.fecha2).grid(row=6, column=2)

        btn_guardar = ttk.Button(toplevel, text="Modificar", padding=3, command=lambda: self.guardar_modificar(datos, int(numero)))
        btn_guardar.grid(row=10, column=3)
        
        
        self.parent.bind('<Return>', lambda e: btn_guardar.invoke())

    def guardar_modificar(self, info, row2):
        "Guarda en el csv las modificaciones al evento"
        dato=(self.titulo2.get(), self.hora2.get(), self.duracion2.get(),self.descripcion2.get(),self.importancia2.get(), self.etiquetas2.get(), self.fecha2.get())
        
        with open("recordatorio.csv", "r") as archivo:
            lineas=csv.reader(archivo)
            datos=[row for row in lineas]
        
        datos[row2]=dato

        with open("recordatorio.csv", "w", newline="") as archivo:
            writer=csv.writer(archivo)

            for row in datos:
                writer.writerow(row)
        self.tabla.destroy()
        self.cargarcsv()

    def guardar(self):
        "Guarda el evento recien creado en un csv"
        if (os.path.isfile("recordatorio.csv")):
            comprobar=self.comprobarHora(self.fecha, self.hora.get(), self.duracion.get())
        else:
            comprobar="Libre"
        dato=(self.titulo.get(), self.hora.get(), self.duracion.get(),self.descripcion.get(),self.importancia.get(), self.etiquetas.get(), self.fecha)
        if comprobar=="Libre":

            if os.path.isfile("recordatorio.csv"):
                with open("recordatorio.csv", "a", newline="") as archivo_csv:
                    recordatorios = csv.writer(archivo_csv)
                    recordatorios.writerow(dato)
                self.tabla.destroy()
                self.cargarcsv()
            else:
                datos=[("Titulo", "Hora", "Duracion", "Descripcion", "Importancia", "Etiquetas", "Fecha")]
                datos.append(dato)
                with open("recordatorio.csv", "w", newline="") as archivo:
                    escritor = csv.writer(archivo, delimiter=",")
                    for contacto in datos:
                        escritor.writerow(contacto)
                self.cargarcsv() 
                
        else: 
            messagebox.showerror("Error", "Este horario esta ocupado por otro recordatorio")
            self.toplevel.lift()
               
    def comprobarHora(self, fecha, hora, duracion):
        "Funcion que evita que 2 eventos compartan el horario"
        
        with open("recordatorio.csv", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            hora2=str(hora).split(":")
            for Titulo, Hora, Duracion, Descripcion, Importancia, Etiquetas, Fecha in lector:
                comparar=str(Hora).split(":")
                if str(fecha) == str(Fecha):
                    if hora2 == comparar:
                        
                        return "Ocupado"
                    else:
                        horaaux = datetime.datetime.strptime(hora, "%H:%M:%S")
                        horaaux2=datetime.datetime.strptime(Hora, "%H:%M:%S")
                        aux=(horaaux + datetime.timedelta(hours=duracion))
                        aux2=(horaaux2 + datetime.timedelta(hours=duracion))
                        aux=datetime.datetime.strftime(aux, "%H:%M:%S").split(":")
                        aux2=datetime.datetime.strftime(aux2, "%H:%M:%S").split(":")
                        if (int(hora2[0])<=int(comparar[0]) and int(aux[0])<=int(comparar[0])) or (int(hora2[0])>=int(aux2[0]) and int(aux[0])>=int(aux2[0])):
                            print("Libre(horas)")
                        else:
                           
                            if (int(hora2[1])<int(Hora[1]) & int(aux[1])<int(comparar[1])) | (int(hora2[1])>int(comparar[1]) & int(aux[1])>int(comparar[1])):
                                print("Libre(minutos)")
                            else:
                                return "Ocupado"
                        print("Paso libre")
        return "Libre"

    def ordernar_fechas(self, fechas):
        "Funcion auxiliar para ordenar cronologicamente las fechas del csv"
        return fechas["Fecha"]

    def cargarcsv(self):
        """"Carga el csv y lo muestra en una tabla. Tambien tiene dentro un filtrado que depende de una variable 
            de la funcion filtrado"""
        if os.path.isfile("recordatorio.csv"):
            dias=[self.hoy + datetime.timedelta(days=dia) for dia in range(7)]

            archivocsv=pd.read_csv("recordatorio.csv")

            archivocsv=archivocsv.sort_values(by=['Fecha'])
            """ archivocsv = archivocsv.set_index('Titulo') """
            archivocsv=archivocsv.reset_index(drop=True)
            self.tabla=ttk.Treeview(self.grid_frame2, columns=list(archivocsv.columns), show="headings")
            self.tabla["columns"]=list(archivocsv.columns)
        
            for column in self.tabla["columns"]:
                self.tabla.column(column, width=100)
                self.tabla.heading(column, text=column)
                
        
            for index, row in archivocsv.iterrows():
                if self.semana_a_mes==True:
                    if row[6] >= str(dias[0]) and row[6]<= str(dias[6]):
                        print("ENTROOOOO")
                        if self.filtrar.get()!="":
                            if row["Titulo"].find(self.filtrar.get())!=(-1) or row["Etiquetas"].find(self.filtrar.get())!=(-1):
                                self.tabla.insert("", tk.END, values=list(row))
                                self.tabla.bind("<Double-Button-1>", lambda event, lista=index:self.evento_opciones(event, lista, row))
                            else:
                                print("No tiene resultados")
                        else:
                            self.tabla.tag_configure('importante', background='#dddddd')
                            if row[4]=="importante":
                                    print("IMPORTANTE")
                                    self.tabla.insert("", tk.END, values=list(row), tags=("importante"))
                            else:
                                    self.tabla.insert("", tk.END, values=list(row))    
                    
                            self.tabla.bind("<Double-Button-1>", lambda event, lista=index:self.evento_opciones(event, lista, row))
                    else:
                        print("NO ENTRO")
                else:
                    if datetime.datetime.strptime(row[6], "%Y-%m-%d").month==self.mes and datetime.datetime.strptime(row[6], "%Y-%m-%d").year==self.año:
                        print(row[4])
                        print(datetime.datetime.strptime(row[6], "%Y-%m-%d").month, self.mes)
                        if self.filtrar.get()!="":
                            if row["Titulo"].find(self.filtrar.get())!=(-1) or row["Etiquetas"].find(self.filtrar.get())!=(-1):
                                self.tabla.insert("", tk.END, values=list(row))
                                self.tabla.bind("<Double-Button-1>", lambda event, lista=index:self.evento_opciones(event, lista, row))
                            else:
                                print("No tiene resultados")
                        else:
                            self.tabla.tag_configure('importante', background='#dddddd')
                            if row[4]=="importante":
                                    print("IMPORTANTE")
                                    self.tabla.insert("", tk.END, values=list(row), tags=("importante"))
                            else:
                                    self.tabla.insert("", tk.END, values=list(row))    
                    
                            self.tabla.bind("<Double-Button-1>", lambda event, lista=index:self.evento_opciones(event, lista, row))
                    else:
                        print("NO ENTRO")                    

            self.tabla.grid()
        else:
            print()

class VentanaEvento(ttk.Frame):
    def __init__(self, parent, arg):
        super().__init__(parent, padding=(20))
        parent.title("Ventana Secundaria")
        parent.geometry("350x100+180+100")
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.resizable(False, False)         
        tk.Label(self, text="arg}", borderwidth=1, relief="solid", width=15).grid(row=0, column=3)
root = tk.Tk()
grid = Grid(root)
root.mainloop()