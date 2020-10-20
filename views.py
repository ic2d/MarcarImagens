# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:54:38 2020

@author: mathe
"""

# from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QApplication, QLabel, QCheckBox
# from PyQt5.QtGui import QPixmap, QFont
# from PyQt5.QtCore import Qt

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QApplication,\
                            QLabel, QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.central_widget = QWidget()
        self.grid_layout = QGridLayout(self.central_widget)
        self.image_test = QPixmap("IMG_20190403_090909185_BURST002.jpg")
        self.image_resize = self.image_test.scaled(800,600)
        
        # cria os labels
        self.mode_label = QLabel('Modo')
        self.quality_label = QLabel('Qualidade da Imagem')
        self.number_label = QLabel('Número do Animal')
        self.editor_label = QLabel('Editar')
        self.image_label = QLabel()
        
        # define a fonte e o tamanho
        self.mode_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.quality_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.number_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        self.editor_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        
        # define o alinhamento dos labels
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.quality_label.setAlignment(Qt.AlignCenter)
        self.number_label.setAlignment(Qt.AlignCenter)
        self.editor_label.setAlignment(Qt.AlignCenter)
        
        # passa a imagem pro label
        self.image_label.setPixmap(self.image_resize)
        
        # cria os botões
        self.button_next = QPushButton('Próximo')
        self.button_previous = QPushButton('Anterior')

        # cria as checkboxs
        self.mode_groupe = QGroupBox()
        self.mode_layout = QHBoxLayout()
        
        self.mark_checkbox = QRadioButton("Marcação")
        self.mark_checkbox.setChecked(True)
        self.review_checkbox = QRadioButton("Revisão")
        self.all_checkbox = QRadioButton("Tudo")
        
        self.mode_layout.addWidget(self.mark_checkbox)
        self.mode_layout.addWidget(self.review_checkbox)
        self.mode_layout.addWidget(self.all_checkbox)
        
        self.mode_groupe.setLayout(self.mode_layout)
        
        self.quality_groupe = QGroupBox()
        self.quality_layout = QHBoxLayout()
        
        self.good_checkbox = QRadioButton("BOM")
        self.good_checkbox.setChecked(True)
        self.bad_checkbox = QRadioButton("RUIM")
        
        self.quality_layout.addWidget(self.good_checkbox)
        self.quality_layout.addWidget(self.bad_checkbox)
        
        self.quality_groupe.setLayout(self.quality_layout)
    
        # adiciona as labels ao grid
        self.grid_layout.addWidget(self.image_label, 0,0,22,1)
        self.grid_layout.addWidget(self.mode_label, 0,1,1,8)
        self.grid_layout.addWidget(self.quality_label, 5,1,1,8)
        self.grid_layout.addWidget(self.number_label, 10,1,1,8)
        self.grid_layout.addWidget(self.editor_label, 15,1,1,8)
        
        # adiciona os botões ao grid
        self.grid_layout.addWidget(self.button_previous, 21,1,1,4)
        self.grid_layout.addWidget(self.button_next, 21,5,1,4)
        
        # adiciona as checkboxs ao grid
        self.grid_layout.addWidget(self.mode_groupe, 2,2,1,6)
        self.grid_layout.addWidget(self.quality_groupe, 7,2,1,6)
        
        # define a widget central
        self.setCentralWidget(self.central_widget)

        
if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.setWindowTitle('Marcar Imagens')
    window.show()
    app.exit(app.exec_())
        