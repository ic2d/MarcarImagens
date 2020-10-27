# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:54:38 2020

@author: mathe
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QApplication, QLabel, QRadioButton, \
                            QButtonGroup, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QMessageBox, QShortcut, \
                            QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtGui import QPixmap, QFont, QIntValidator, QImage, QPainter, QPen, QBrush, QKeySequence
from PyQt5.QtCore import Qt, QLine
import cv2 as cv
import os  # funções para interarir com SO
import os.path
import json  # biblioteca para ler e guardar arquivos json

l_pontos = []

arquivo_base = "bufalo"  # pasta com imagens
f_list = os.listdir(arquivo_base)  # função retorna lista de arquivos da pasta
clean_f_list = [f for f in f_list if f[-3:] == 'jpg']
index = 0
lines = []
flag = False
flag_del = False
flag_draw1 = False

if os.path.isfile('Dados.txt'):
    with open('Dados.txt', 'r') as json_file:
        Dados = json.load(json_file)
        print("Carregou com Sucesso")
        for i in Dados["imagens"]:
            if len(Dados["imagens"][i]["pontos"])==0:
                break
            index+=1
                    
else :
    print("Arquivo não existe")
    Dados = {"versao": 1.0, "resolucao": (800, 600), "imagens": {}}
    # adiciona a clean_f_list aos index
    for i in clean_f_list:
        Dados["imagens"][i] = {"pontos": [], "numero":0, "qualidade": True}
                   

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0           

    def mousePressEvent(self,event):
        global index
        global flag
        global flag_del
        global l_pontos
        
        if len(Dados["imagens"][clean_f_list[index]]["pontos"])<1:
            flag = True
            self.x0 = event.x()
            self.y0 = event.y()
            l_pontos.append((self.x0, self.y0))
            
            if len(l_pontos)==3:
                l_pontos.sort()
                l_pontos[1],l_pontos[2] = l_pontos[2],l_pontos[1]
                Dados["imagens"][clean_f_list[index]]["pontos"].append(l_pontos.copy())
                l_pontos.clear()
                
            line1 =QLine(self.x0-5, self.y0-5, self.x0+5, self.y0+5)
            line2 =QLine(self.x0+5, self.y0-5, self.x0-5, self.y0+5)
            lines.append((line1,line2))
            self.update()
        
        if flag_del:
            flag = True
            l_pontos = Dados["imagens"][clean_f_list[index]]["pontos"][0].copy()
            self.x0 = event.x()
            self.y0 = event.y()
            l_pontos.append((self.x0, self.y0))
            
            for i in l_pontos:
                x, y = i
                line1 =QLine(x-5, y-5, x+5, y+5)
                line2 =QLine(x+5, y-5, x-5, y+5)
                lines.append((line1,line2))
                
            if len(l_pontos)==3:
                l_pontos.sort()
                l_pontos[1],l_pontos[2] = l_pontos[2],l_pontos[1]
                Dados["imagens"][clean_f_list[index]]["pontos"][0] = l_pontos.copy()
                l_pontos.clear()
            self.update()
            flag_del = False
   
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green,5,Qt.SolidLine))
        global index
        global flag
        
        if len(Dados["imagens"][clean_f_list[index]]["pontos"])==1 and flag:
            for list_i in Dados["imagens"][clean_f_list[index]]["pontos"]:
                for i in list_i:
                    x, y = i
                    line1 =QLine(x-5, y-5, x+5, y+5)
                    line2 =QLine(x+5, y-5, x-5, y+5)
                    lines.append((line1,line2))
                    
        if len(Dados["imagens"][clean_f_list[index]]["pontos"])<=1 and flag:
            for line in lines:
                line1, line2 = line
                painter.drawLine(line1)
                painter.drawLine(line2)
            
        flag = False


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global flag
        global index
        
        self.central_widget = QWidget()
        self.grid_layout = QGridLayout(self.central_widget)
        self.setMouseTracking(True)
        self.flag_draw = False
                
        print("Imagem: ", clean_f_list[index])
        
        
    
        original_img = cv.imread(os.path.join(arquivo_base, clean_f_list[index]))
            
        height, width, channel = original_img.shape
        bytesPerLine = 3 * width
        
        self.opencv_image = QImage(original_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # vai ser trocado pra janela do opencv
        self.image_test = QPixmap(QImage(self.opencv_image))
        self.image_resize = self.image_test.scaled(800,600)
        
        
        self.example_image = QPixmap("example.png")
        self.example_image = self.example_image.scaled(100,100)
        self.total_images = len(clean_f_list)
        
        
        # cria os labels
        # self.mode_label = QLabel('Modo')
        self.quality_label = QLabel('Qualidade da Imagem')
        self.number_label = QLabel('Número do Animal')
        self.editor_label = QLabel('Editar')
        self.count_label = QLabel('Imagem: ' + str(index+1) + '/' + str(self.total_images))
        self.image_label = ImageLabel()
        self.example_label = QLabel()
        
        
        # define a fonte e o tamanho
        # self.mode_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.quality_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.number_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.editor_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.count_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        
        # define o alinhamento dos labels
        # self.mode_label.setAlignment(Qt.AlignCenter)
        self.quality_label.setAlignment(Qt.AlignCenter)
        self.number_label.setAlignment(Qt.AlignCenter)
        self.editor_label.setAlignment(Qt.AlignCenter)
        self.count_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAlignment(Qt.AlignTop)
        
        # passa a imagem pro label
        self.image_label.setPixmap(self.image_resize)
        self.example_label.setPixmap(self.example_image)
                
        # cria os botões
        self.button_next = QPushButton('Próximo')
        self.button_previous = QPushButton('Anterior')
        self.button_del1 = QPushButton('Excluir 1')
        self.button_del2 = QPushButton('Excluir 2')
        self.button_del3 = QPushButton('Excluir 3')
        self.button_del4 = QPushButton('Excluir Todos')
        self.button_help = QPushButton('Atalhos')

        # cria as checkboxs
        # self.mode_groupe = QGroupBox()
        # self.mode_layout = QHBoxLayout()
        
        # self.mark_checkbox = QRadioButton("Marcação")
        # self.mark_checkbox.setChecked(True)
        # self.review_checkbox = QRadioButton("Revisão")
        # self.all_checkbox = QRadioButton("Tudo")
        
        # self.mode_layout.addWidget(self.mark_checkbox)
        # self.mode_layout.addWidget(self.review_checkbox)
        # self.mode_layout.addWidget(self.all_checkbox)
        
        # self.mode_groupe.setLayout(self.mode_layout)
        
        self.quality_groupe = QGroupBox()
        self.quality_layout = QHBoxLayout()
        
        self.good_checkbox = QRadioButton("BOM")
        self.bad_checkbox = QRadioButton("RUIM")
        
        if Dados["imagens"][clean_f_list[index]]["qualidade"] == True:
            self.good_checkbox.setChecked(True)
        else:
            self.bad_checkbox.setChecked(True)
        
        self.quality_layout.addWidget(self.good_checkbox)
        self.quality_layout.addWidget(self.bad_checkbox)
        
        self.quality_groupe.setLayout(self.quality_layout)
        
        # cria o campo para inserir o número
        self.number_input = QLineEdit()
        self.number_input.setValidator(QIntValidator())
        self.number_input.setAlignment(Qt.AlignRight)  
        self.number_input.setText(str(Dados["imagens"][clean_f_list[index]]["numero"]))
        
        # cria a tabela com as imagens
        self.table = QTableWidget(self.total_images, 2, self)
        self.table.setHorizontalHeaderLabels(('Status','Imagem'))
        
        for i in range(self.total_images):
            for j in range(2):
                if j == 1:
                    self.table.setItem(i,j,QTableWidgetItem(clean_f_list[i]))
                elif j == 0:
                    cell = QTableWidget()
                    checkbox = QtWidgets.QCheckBox()
                    checkbox.setEnabled(False)
                    if len(Dados["imagens"][clean_f_list[i]]["pontos"])==1:
                        checkbox.setChecked(True)
                        
                    layout_cell = QHBoxLayout(cell)
                    layout_cell.addWidget(checkbox)
                    layout_cell.setAlignment(Qt.AlignCenter)
                    layout_cell.setContentsMargins(0,0,0,0)
                    cell.setLayout(layout_cell)
                    self.table.setCellWidget(i,j,cell)
                            
        fnt = self.table.font()
        fnt.setPointSize(8)       
        self.table.setFont(fnt)
        self.table.setColumnWidth(0,50)
        self.table.setColumnWidth(1,300)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.scrollToItem(self.table.item(index,1))
        self.table.selectRow(index)
    
        # adiciona as labels ao grid
        self.grid_layout.addWidget(self.count_label, 0,0,1,1)
        self.grid_layout.addWidget(self.image_label, 1,0,22,1)
        self.grid_layout.addWidget(self.table, 1,1,9,8)
        self.grid_layout.addWidget(self.quality_label, 10,1,1,8)
        self.grid_layout.addWidget(self.number_label, 13,1,1,8)
        self.grid_layout.addWidget(self.editor_label, 16,1,1,8)
        self.grid_layout.addWidget(self.example_label, 17,1,2,2)
        
        # adiciona os botões ao grid
        self.grid_layout.addWidget(self.button_del1, 17,3,1,2)
        self.grid_layout.addWidget(self.button_del2, 17,6,1,2)
        self.grid_layout.addWidget(self.button_del3, 18,3,1,2)
        self.grid_layout.addWidget(self.button_del4, 18,6,1,2)
        self.grid_layout.addWidget(self.button_previous, 20,1,1,4)
        self.grid_layout.addWidget(self.button_next, 20,5,1,4)
        self.grid_layout.addWidget(self.button_help,0,7,1,1)
        
        # adiciona as checkboxs ao grid
        # self.grid_layout.addWidget(self.mode_groupe, 2,2,1,6)
        self.grid_layout.addWidget(self.quality_groupe, 11,2,1,6)
        
        # adiciona a input line ao grid
        self.grid_layout.addWidget(self.number_input, 14,4,1,2)
        
        # define a widget central
        self.setCentralWidget(self.central_widget)
        
        # Signals
        self.button_help.clicked.connect(self.show_popup)
        self.button_next.clicked.connect(self.next_image)
        self.button_previous.clicked.connect(self.previous_image)
        self.button_del1.clicked.connect(self.delete_1)
        self.button_del2.clicked.connect(self.delete_2)
        self.button_del3.clicked.connect(self.delete_3)
        self.button_del4.clicked.connect(self.delete_all)
        self.table.doubleClicked.connect(self.mouseDoubleClickEvent)
        self.number_input.returnPressed.connect(self.animal_number)
        self.good_checkbox.toggled.connect(lambda:self.checkbox_state(self.good_checkbox))
        self.bad_checkbox.toggled.connect(lambda:self.checkbox_state(self.bad_checkbox))
        
        # Criar os atalhos do teclado
        self.shortcut_next = QShortcut(QKeySequence('Space'),self)
        self.shortcut_next.activated.connect(self.next_image)
        self.shortcut_next = QShortcut(QKeySequence('Tab'),self)
        self.shortcut_next.activated.connect(self.previous_image)
        self.shortcut_next = QShortcut(QKeySequence('Esc'),self)
        self.shortcut_next.activated.connect(self.close)
        self.shortcut_delete_all = QShortcut(QKeySequence('Ctrl+A'),self)
        self.shortcut_delete_all.activated.connect(self.delete_all)
        self.shortcut_delete_all = QShortcut(QKeySequence('Ctrl+1'),self)
        self.shortcut_delete_all.activated.connect(self.delete_1)
        self.shortcut_delete_all = QShortcut(QKeySequence('Ctrl+2'),self)
        self.shortcut_delete_all.activated.connect(self.delete_2)
        self.shortcut_delete_all = QShortcut(QKeySequence('Ctrl+3'),self)
        self.shortcut_delete_all.activated.connect(self.delete_3)
        self.shortcut_focus = QShortcut(QKeySequence('N'),self)
        self.shortcut_focus.activated.connect(self.focus_line)
        self.shortcut_quality = QShortcut(QKeySequence('R'),self)
        self.shortcut_quality.activated.connect(self.change_quality)
        
        self.show()
                
    
    def show_popup(self):
        global flag
        QMessageBox.about(self,\
                          "Atalhos",\
                          "Space\t- \tAvançar Imagem\n\
Tab\t- \tVoltar Imagem\n\
N\t- \tSelecionar número\n\
Enter\t- \tConfirmar número\n\
R\t- \tMarcar imagem ruim\n\
Ctrl + 1\t- \tApagar ponto à esquerda\n\
Ctrl + 2\t- \tApagar ponto à direita\n\
Ctrl + 3\t- \tApagar ponto inferior\n\
Esc\t- \tSalvar e Fechar")

        flag = True
        self.image_label.update()
            
    def next_image(self):
        global index
        global flag
        
        if index < self.total_images-1:
            index+=1
            lines.clear()
            
            print(index)
            print("Imagem: ", clean_f_list[index])
        
            original_img = cv.imread(os.path.join(arquivo_base, clean_f_list[index]))
            
            height, width, channel = original_img.shape
            bytesPerLine = 3 * width
            
            self.opencv_image = QImage(original_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # vai ser trocado pra janela do opencv
            self.image_test = QPixmap(QImage(self.opencv_image))
            self.image_resize = self.image_test.scaled(800,600)
            self.image_label.setPixmap(self.image_resize)
            new_text = "Imagem: {}/{}".format(index+1, self.total_images)
            self.count_label.setText(new_text)
            self.number_input.setText(str(Dados["imagens"][clean_f_list[index]]["numero"]))
            if Dados["imagens"][clean_f_list[index]]["qualidade"] == False:
                self.bad_checkbox.setChecked(True)
            else:
                self.good_checkbox.setChecked(True)
                
            if len(Dados["imagens"][clean_f_list[index]]["pontos"])==1:
                flag = True

            self.save()
            arquivo = open("Dados.txt", "w")
            arquivo.write(json.dumps(Dados, indent=3))
                
    def previous_image(self):
        global index
        global flag
        
        if index > 0:
            index-=1
            lines.clear()
            
            print(index)
            print("Imagem: ", clean_f_list[index])
        
            original_img = cv.imread(os.path.join(arquivo_base, clean_f_list[index]))
                
            height, width, channel = original_img.shape
            bytesPerLine = 3 * width
            
            self.opencv_image = QImage(original_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # vai ser trocado pra janela do opencv
            self.image_test = QPixmap(QImage(self.opencv_image))
            self.image_resize = self.image_test.scaled(800,600)
            self.image_label.setPixmap(self.image_resize)
            new_text = "Imagem: {}/{}".format(index+1, self.total_images)
            self.count_label.setText(new_text)
            self.number_input.setText(str(Dados["imagens"][clean_f_list[index]]["numero"]))
            
            if Dados["imagens"][clean_f_list[index]]["qualidade"] == False:
                self.bad_checkbox.setChecked(True)
            else:
                self.good_checkbox.setChecked(True)
            
            if len(Dados["imagens"][clean_f_list[index]]["pontos"])==1:
                flag = True
            
            self.save()
            
    def save(self):
            arquivo = open("Dados.txt", "w")
            arquivo.write(json.dumps(Dados, indent=3))
            
            for i in range(self.total_images):
                cell = QTableWidget()
                checkbox = QtWidgets.QCheckBox()
                checkbox.setEnabled(False)
                if len(Dados["imagens"][clean_f_list[i]]["pontos"])==1:
                    checkbox.setChecked(True)
                    
                layout_cell = QHBoxLayout(cell)
                layout_cell.addWidget(checkbox)
                layout_cell.setAlignment(Qt.AlignCenter)
                layout_cell.setContentsMargins(0,0,0,0)
                cell.setLayout(layout_cell)
                self.table.setCellWidget(i,0,cell)
                    
            self.table.scrollToItem(self.table.item(index,1))
            self.table.selectRow(index)
            
    def focus_line(self):
        self.number_input.setFocus()
        self.number_input.selectAll()
        
    def animal_number(self):
        Dados["imagens"][clean_f_list[index]]["numero"] = self.number_input.text()
        self.number_input.clearFocus()
            
    def mouseDoubleClickEvent(self,event):
        global index
        for idx in self.table.selectionModel().selectedIndexes():
            index = idx.row() -1
            
        self.next_image()
    
    def change_quality(self):
        if Dados["imagens"][clean_f_list[index]]["qualidade"] == True:
            Dados["imagens"][clean_f_list[index]]["qualidade"] = False
            self.good_checkbox.setChecked(False)
            self.bad_checkbox.setChecked(True)
            self.save()
        else:
            Dados["imagens"][clean_f_list[index]]["qualidade"] = True
            self.good_checkbox.setChecked(True)
            self.bad_checkbox.setChecked(False)
            self.save()
            
    def checkbox_state(self,b):
        if b.text() == "BOM":
            if b.isChecked()==True:
                Dados["imagens"][clean_f_list[index]]["qualidade"] = True
                self.save()
                            
        if b.text() == "RUIM":
            if b.isChecked()==True:
                Dados["imagens"][clean_f_list[index]]["qualidade"] = False
                self.save()
    
    def delete_1(self):
        global flag
        global flag_del
        global index
        
        if Dados["imagens"][clean_f_list[index]]["pontos"]:
            print("Apagar ponto 1")
            list_delete = Dados["imagens"][clean_f_list[index]]["pontos"]
            if len(list_delete[0]) == 3:
                list_delete[0].pop(0)
                lines.clear()
                print(len(Dados["imagens"][clean_f_list[index]]["pontos"][0][0]))
                flag_del = True
                self.image_label.update()
                flag = True
            else:
                print("Não tem nada pra apaagr")
        else:
            print("Não tem nada pra apaagr")
            
    def delete_2(self):
        global flag
        global flag_del
        global index
        
        if Dados["imagens"][clean_f_list[index]]["pontos"]:
            print("Apagar ponto 2")
            list_delete = Dados["imagens"][clean_f_list[index]]["pontos"]
            if len(list_delete[0]) == 3:
                list_delete[0].pop(1)
                lines.clear()
                print(len(Dados["imagens"][clean_f_list[index]]["pontos"][0][0]))
                flag_del = True
                self.image_label.update()
                flag = True
            else:
                print("Não tem nada pra apaagr")
        else:
            print("Não tem nada pra apaagr")
            
    def delete_3(self):
        global flag
        global flag_del
        global index
        
        if Dados["imagens"][clean_f_list[index]]["pontos"]:
            print("Apagar ponto 3")
            list_delete = Dados["imagens"][clean_f_list[index]]["pontos"]
            if len(list_delete[0]) == 3:
                list_delete[0].pop(2)
                lines.clear()
                print(len(Dados["imagens"][clean_f_list[index]]["pontos"][0][0]))
                flag_del = True
                self.image_label.update()
                flag = True
            else:
                print("Não tem nada pra apaagr")
        else:
            print("Não tem nada pra apaagr")
        
    def delete_all(self):
        global flag
        global index
        
        if Dados["imagens"][clean_f_list[index]]["pontos"]:
            if len(Dados["imagens"][clean_f_list[index]]["pontos"][0]) == 3:
                print("Apagar Tudo")
                Dados["imagens"][clean_f_list[index]]["pontos"].clear()
                lines.clear()
                self.image_label.update()
                flag = True
            else:
                print("Não tem nada pra apaagr")
        else:
            print("Não tem nada pra apaagr")
        
    def closeEvent(self, event):
        self.save()
        event.accept()
 
if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.setWindowTitle('Marcar Imagens')
    window.show()
    app.exit(app.exec_())
        