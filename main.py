# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from FiebreFormMejoradoFinal import Ui_Dialog
from kanren import run, var, Relation, facts

class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setupUi(self)
        
        #Boton es presionado
        self.EnviarBTN.pressed.connect(lambda: self.inferencia() )

        #Grafica Pantalla
        self.show()

    def inferencia(self):
        #Predicados
        Transmision = Relation()
        Lugar = Relation()
        Sintoma = Relation()
        Enfermedad = Relation()
        #Variables
        zikaCont=0
        fiebreAmarillaCont=0
        respuestas=[]
        flag1=False
        flag2=False
        Causa=self.CausasCMB.currentText()
        Pais=self.PaisCMB.currentText()
        Sintomas=[]
        for sintoma in self.SintomasLW.selectedItems():
            Sintomas.append(sintoma.text())
        X=var()
        Y=var()
        Z=var()
        W=var()
        #Conexiones
        facts(Transmision,
            ("He tenido relaciones sexuales","Zika"),
            ("He sido picado por un zancudo","Zika"),
            ("He sido picado por un zancudo","Fiebre Amarilla"),
            ("Me han donado sangre","Zika"))

        facts(Lugar,
            ("Zika","America Sur"),
            ("Zika","Africa"),
            ("Zika","America Norte"),
            ("Zika","America Central"),
            ("Fiebre Amarilla","America Central"),
            ("Fiebre Amarilla","America Sur"),
            ("Fiebre Amarilla","Africa"))

        facts(Sintoma,
            ("Enfermedad leve","Fiebre"),
            ("Enfermedad leve","Dolor Muscular"),
            ("Enfermedad leve","Perdida de apetito"),
            ("Enfermedad media","Vomitos"),
            ("Enfermedad grave","Ictericia"),
            ("Enfermedad grave","Sangrado"),
            ("Enfermedad grave","Arritmia"),
            ("Enfermedad media","Conjuntivitis"),
            ("Enfermedad leve","Cansancio"))

        facts(Enfermedad,
            ("Enfermedad media", "Zika"),
            ("Enfermedad grave","Fiebre Amarilla"),
            ("Enfermedad leve","No posee enfermedad tropical!"))

        #Motor de inferencias
        for sintoma in Sintomas:
            if "No posee enfermedad tropical!" != run(0,X,Sintoma(Y,sintoma),Enfermedad(Y,X))[0]:
                respuesta1 = run(0,X,Sintoma(Z,sintoma),Enfermedad(Z,Y),Lugar(Y,X))
                respuesta2 = run(0,X,Sintoma(Z,sintoma),Enfermedad(Z,Y),Transmision(X,Y))
                for resp in respuesta1:
                    if Pais==resp:
                        flag1=True
                for resp in respuesta2:
                    if Causa==resp:
                        flag2=True
                if flag1 and flag2:
                    respuesta=run(0,W,Sintoma(Z,sintoma),Enfermedad(Z,W))
                    respuestas.append(respuesta[0])
                else:
                    continue

                print(flag1)
                print(flag2)
                        
                print(sintoma)
                print(respuesta1)
                print(respuesta2)

            else:
                continue
                
        #Mide el numero de respuestas por enfermedad
        for respuesta in respuestas:
            if respuesta == "Zika":
                zikaCont+=1
            if respuesta == "Fiebre Amarilla":
                fiebreAmarillaCont += 1
        
        #Compara los resultados y decide
        if zikaCont > fiebreAmarillaCont:
            self.RespuestaLBL.setText("El usuario probablemente tenga Zika")
        elif fiebreAmarillaCont > zikaCont:
            self.RespuestaLBL.setText("El usuario probablemente tenga Fiebre Amarilla")
        else:
            self.RespuestaLBL.setText("El usuario no presenta sintomas que determinen una enfermedad tropical")

        respuesta=[]

       

    


        
        





















if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    
    app.exec_()
