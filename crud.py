# Importar bilbiotecas 
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Desarrollo de la interfaz grafica
root = Tk()
root.config(bg = '#12233D')
root.title("Aplicacion CRUD con base de datos")
root.geometry("600x360")



# Creamos las variables que manejaremos
miID = StringVar()
miNombre = StringVar()
miCargo = StringVar()
miSalario = StringVar()

# Tabla grafica
tree = ttk.Treeview(height=10, columns=('#0','#1','#2','#3'))    # Tamaño y forma de la tabla
tree.place(x = 0, y = 130)                                       # posicion de la tabla
tree.column('#0',width=100)                                      # Configurar tamaño de columnas
tree.heading('#0', text="ID", anchor="center")                   # Configurar encabezado
tree.heading('#1', text="Nombre del ampleado", anchor="center")  # Configurar encabezado
tree.heading('#2', text="Cargo", anchor="center")                # Configurar encabezado
tree.column('#3',width=100)                                      # Configurar tamaño de columnas
tree.heading('#3', text="Salario", anchor="center")              # Configurar encabezado

def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)

    miID.set(tree.item(item, 'text'))
    print(miID.get())
    miNombre.set(tree.item(item, "values")[0])
    miCargo.set(tree.item(item, "values")[1])
    miSalario.set(tree.item(item, "values")[2])

tree.bind("<Double-1>", seleccionarUsandoClick) # Correr seleccionarUsandoClick con doble clock

# Conexion con la base de datos
def conexionBBDD():
    conexion = sqlite3.connect("base.db")
    cursor = conexion.cursor()

    # Para controlar la generacion de assepciones
    try:
        cursor.execute("""
            CREATE TABLE empleados (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50),
                CARGO VARCHAR(50),
                SALARIO INTEGER NOT NULL
            )
        """)
        messagebox.showinfo("Conexion","Base de Datos creada Exitosamente!")
    except:
        messagebox.showinfo("Conexion","Coneccion exitosa con la base de datos")
    finally:
        conexion.commit()
        conexion.close()

def eliminarBBDD():
    conexion = sqlite3.connect("base.db")
    cursor = conexion.cursor()

    # Consulta si esta seguro
    if messagebox.askyesno(message= "Los datos se perderan definitivamente, desea continuar?",title="Advertencia"):
        try:
            cursor.execute("DROP TABLE empleados")
        finally:
            conexion.commit()
            conexion.close()

def salirAplicacion():
    # Consultamos si estamos seguros de salir
    respuesta = messagebox.askquestion("Salir","Estas seguro que deseas salir?")
    if respuesta == "yes":
        root.destroy() # Para cerrar la ventana

def limpiarCampos():
    miID.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")

def mensaje():
    acerca = """
    Aplicacion CRUD
    Version 1.0
    Tecnología Python Tkinter
    """
    messagebox.showinfo(title="Acerca de la Aplicacion",message=acerca)

# ################################## Métodos CRUD ##################################

def crear():
    conexion = sqlite3.connect("base.db")
    cursor = conexion.cursor()

    try:
        # Insertamos los datos en la tabla
        cursor.execute(f"INSERT INTO empleados VALUES(NULL,'{miNombre.get()}','{miCargo.get()}','{miSalario.get()}')")
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrio un error al crear el registro")
    finally:
        conexion.commit()
        conexion.close()
        limpiarCampos()
        mostrar()

def mostrar():
    conexion = sqlite3.connect("base.db")
    cursor = conexion.cursor()

    # Para borrar los registros anteriores, y volverlos a cargar
    registros = tree.get_children()
    for i in registros:
        tree.delete(i)

    try:
        cursor.execute("SELECT * FROM empleados")
        for row in cursor:
            tree.insert("",0,text= row[0], values = (row[1], row[2], row[3]))
    except:
        print("error")

def actualizar():
    conexion = sqlite3.connect("base.db")
    cursor = conexion.cursor()

    try:
        # Insertamos los datos en la tabla
        cursor.execute(f'UPDATE empleados SET NOMBRE="{miNombre.get()}", CARGO="{miCargo.get()}", SALARIO="{miSalario.get()}" WHERE ID="{miID.get()}"')
        conexion.commit()
        conexion.close()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrio un error al actualizar el registro")    
    finally:
        limpiarCampos()
        mostrar()


def borrar():
    conexion = sqlite3.connect("base.db")
    cursor = conexion.cursor()

    try:
        if messagebox.askyesno(message="Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            cursor.execute(f'DELETE FROM empleados WHERE ID = "{miID.get()}"') 
        
        conexion.commit()
        conexion.close()
    except:
        messagebox.showwarning("ADVERTENCIA","Ocurrio un error al tratar de eliminar el registro")
    finally: 
        limpiarCampos()
        mostrar()


########################## Colocar elementos en la ventana ########################################

# Agregar barra de menus:
menubar = Menu(root)

menubasedat = Menu(menubar, tearoff =0)
menubasedat.add_command(label = "Crear/Conectar Base de Datos", command=conexionBBDD)
menubasedat.add_command(label = "Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label = "Salir", command=salirAplicacion)
menubar.add_cascade(label = "Inicio", menu=menubasedat)

menuayuda = Menu(menubar, tearoff=0)
menuayuda.add_command(label = "Limpiar Campos", command=limpiarCampos)
menuayuda.add_command(label = "Acerca", command=mensaje)
menubar.add_cascade(label = "Ayuda", menu=menuayuda)

# Agregar etiquetas y cajas de texto
e1 = Entry(root, textvariable = miID)

l2 = Label(root, text = "Nombre", bg = '#12233D', fg = 'white')
l2.place(x = 50, y = 10)
e2 = Entry(root, textvariable= miNombre, width = 50)
e2.place(x = 100, y = 10)

l3 = Label(root, text = "Cargo", bg = '#12233D', fg = 'white')
l3.place(x = 50, y = 40)
e3 = Entry(root, textvariable= miCargo)
e3.place(x = 100, y = 40)

l4 = Label(root, text = "Salario", bg = '#12233D', fg = 'white')
l4.place(x = 280, y = 40)
e4 = Entry(root, textvariable= miSalario, width = 10)
e4.place(x = 320, y = 40)
l5 = Label(root, text = "$",  bg = '#12233D', fg = 'white')
l5.place(x = 380, y = 40)

# Agregar botones
b1 = Button(root, text = "Crear Registro", bg = "#57708C", fg = 'white', command = crear)
b1.place(x = 50, y = 90)

b2 = Button(root, text = "Modificar Registro", bg = "#57708C", fg = 'white', command = actualizar)
b2.place(x = 180, y = 90)

b3 = Button(root, text = "Mostrar Lista", bg = "#57708C", fg = 'white', command = mostrar)
b3.place(x = 320, y = 90)

b4 = Button(root, text = "Eliminar Registro", bg = "#D95A51", fg = '#FFE2D7', command = borrar)
b4.place(x = 450, y = 90)

root.config(menu=menubar)
root.mainloop()
