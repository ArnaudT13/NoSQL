#!/usr/bin/python3.7

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import call_center as cc


""" 
Table model du tableview central

""" 
class MyTableModel(QAbstractTableModel):

    def __init__(self, datain, headerdata, parent=None): 
        QAbstractTableModel.__init__(self, parent) 
        self.arraydata = datain
        self.headerdata = headerdata
        self._tab = 0
   
    def rowCount(self, parent):
        return len(self.arraydata)
    
    def columnCount(self, parent):
        return len(self.arraydata[0])
    
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.EditRole:
            print( "edit mode" )
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.arraydata[index.row()][index.column()]

    def setTab(self, tab):
        self._tab = tab

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if(self._tab == 1):
                    return (cc.get_operators_keys())[section]
                else:
                    return (cc.get_calls_keys())[section]
        
            if orientation == Qt.Vertical:
                return ([str(counter) for counter in range(1,len(self.arraydata)+1)])[section]
                # if(self._tab == 1):
                #     return (cc.get_all_id_of_table('operators'))[section]
                # else:
                #     return (cc.get_all_id_of_table('calls'))[section]
                #return (cc.get_all_id_of_table('calls'))[section]


""" 
Fenetre graphique (Pop-up) utilisée en cas d'erreurs (oublie de paramètres, entrées vides, ...)
""" 
class MessageBox(QMessageBox):
    def __init__(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Veuillez remplir tous les champs")
        msg.exec()

""" 
Fenetre graphique principale 

""" 
class Ui_MainWindow(object):

    """ 
    Permet de mettre à jour les axes du tableau central

    :return: returns nothing 
    """ 
    def update_axis(self):
        #GET ALL KEYS !
        for i in range(0,len(self.arraydata[0])):
            print(self.arraydata[i])
            #self.setHeaderData(i, Qt.Horizontal, self.arraydata[i])


    """ 
    Affiche tous les appels en actualisant le model du tableau central

    :return: returns nothing 
    """ 
    def display_all_calls(self):
        header = []
        calls_views_model = MyTableModel(cc.get_all_calls(), header, self)
        calls_views_model.setTab(0)
        self.view_calls.setModel(calls_views_model)
        print(bcolors.OKGREEN+ "Query \"display_all_calls\" : SUCCESS" + bcolors.ENDC) 


    """ 
    Permet d'ajouter graphiquement un opérateur dans le base redis

    :return: returns nothing 
    """ 
    def add_operator(self):
        if((self.edit_lastname.text() != '' ) & (self.edit_firstname.text() != '' ) & (self.edit_birthdate.text() != '' ) & (self.edit_income.text() != '')):
            cc.add_operator(self.edit_id_operator.text(), self.edit_lastname.text(), self.edit_firstname.text(), self.edit_birthdate.text(), self.edit_income.text())
            self.update_operator_combo()
            self.display_all_operators()
            print(bcolors.OKGREEN + "Query \"add_operator\" : SUCCESS" + bcolors.ENDC )
        else:
            msg = MessageBox()
            print(bcolors.FAIL + "Query \"add_operator\" : FAILED" + bcolors.ENDC)

    """ 
    Permet d'ajouter graphiquement un appel dans le base redis

    :return: returns nothing 
    """ 
    def add_call(self):
        if((self.edit_id_call.text() != '' ) & (self.edit_hours.text() != '' ) & (self.edit_length.text() != '' ) & (self.edit_num.text() != '') ):
            #add_call(id, call_hour, origin_phone_number, call_duration, operator_id, description):
            cc.add_call(self.edit_id_call.text(), self.edit_hours.text(), self.edit_num.text(), self.edit_length.text(), self.combo_operator_call.currentIndex(), self.combo_state_call.currentIndex()) 
            self.display_all_calls()
            print(bcolors.OKGREEN + "Query \"add_call\" : SUCCESS" + bcolors.ENDC)
        else:
            msg = MessageBox()
            print(bcolors.FAIL + "Query : \"add_call\" : FAILED" + bcolors.ENDC)


    """ 
    Permet de mettre à jour les opérateurs de la base redis disponibles dans les combo-boxs, i.e menus déroulants 

    :return: returns nothing 
    """ 
    def update_operator_combo(self):
        # Combo in call windows 
        self.combo_operator_call.clear()

        # Combo in all views
        self.combo_operator.clear()
        self.combo_operator.addItem("Tous")
        for operator_name in cc.get_all_operators_names():
            self.combo_operator_call.addItem(operator_name)
            self.combo_operator.addItem(operator_name)

    
    """ 
    Affiche tous les opérateurs en actualisant le model du tableau central

    :return: returns nothing 
    """
    def display_all_operators(self):
        header = []
        calls_views_model = MyTableModel(cc.get_all_operators(), header, self)
        calls_views_model.setTab(1)
        self.view_calls.setModel(calls_views_model)
        print(bcolors.OKGREEN + "Query \"display_all_operators\" : SUCCESS " + bcolors.ENDC)
    
    def display_all_calls_with_filter(self):
        header = []

        calls_views_model = MyTableModel(cc.filter(self.combo_state.currentIndex()), header, self)
        calls_views_model.setTab(2)
        self.view_calls.setModel(calls_views_model)
        print(bcolors.OKGREEN+ "Query \"display_all_calls_with_filter\" : SUCCESS" + bcolors.ENDC) 

    
    """ 
    Adapte le model du tableau suivant la tab selectionné.

    Pour les tab 1,3 on affiche des appels. Pour le tab 2 on affiche les opérateurs.

    :return: returns nothing 
    """
    def onChangedTab(self):

        if(self.table_management.currentIndex() == 1):
            self.display_all_operators()
        else:
            self.display_all_calls()

    """ 
    Gestion des elements graphiques

    Declaration, mise en place et connections de tous les éléments. CERTAINS ELEMENTS SONT GENERES AUTOMATIQUEMENT
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(813, 582)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.view_calls = QtWidgets.QTableView(self.centralwidget)
        self.view_calls.setGeometry(QtCore.QRect(10, 180, 791, 391))
        self.view_calls.setObjectName("view_calls")

        tablemodel = MyTableModel(my_array, self)
        self.view_calls.setModel(tablemodel)

        self.table_management = QtWidgets.QTabWidget(self.centralwidget)
        self.table_management.setGeometry(QtCore.QRect(10, 10, 791, 161))
        self.table_management.setObjectName("table_management")

        self.table_management.currentChanged.connect(self.onChangedTab)

        self.widget_calls_management = QtWidgets.QWidget()
        self.widget_calls_management.setObjectName("widget_calls_management")
        self.label_id_call = QtWidgets.QLabel(self.widget_calls_management)
        self.label_id_call.setGeometry(QtCore.QRect(50, 10, 101, 16))
        self.label_id_call.setObjectName("label_id_call")

        self.label_hours = QtWidgets.QLabel(self.widget_calls_management)
        self.label_hours.setGeometry(QtCore.QRect(50, 70, 101, 16))
        self.label_hours.setObjectName("label_hours")
        self.label_num = QtWidgets.QLabel(self.widget_calls_management)
        self.label_num.setGeometry(QtCore.QRect(220, 10, 101, 16))
        self.label_num.setObjectName("label_num")
        self.label_length_call = QtWidgets.QLabel(self.widget_calls_management)
        self.label_length_call.setGeometry(QtCore.QRect(220, 70, 101, 16))
        self.label_length_call.setObjectName("label_length_call")
        self.label_5 = QtWidgets.QLabel(self.widget_calls_management)
        self.label_5.setGeometry(QtCore.QRect(390, 10, 101, 16))
        self.label_5.setObjectName("label_5")
        self.combo_state_call = QtWidgets.QComboBox(self.widget_calls_management)
        self.combo_state_call.setGeometry(QtCore.QRect(390, 30, 121, 22))

        self.combo_state_call.setObjectName("combo_state_call")
        self.combo_state_call.addItem("inprogress")
        self.combo_state_call.addItem("finished")
        self.combo_state_call.addItem("ignored")
        self.combo_state_call.addItem("unaffected")

        self.combo_operator_call = QtWidgets.QComboBox(self.widget_calls_management)
        self.combo_operator_call.setGeometry(QtCore.QRect(540, 30, 181, 22))
        self.combo_operator_call.setObjectName("combo_operator_call")

        for operator_name in operator_list:
            self.combo_operator_call.addItem(operator_name)

        self.label_operator_name_call = QtWidgets.QLabel(self.widget_calls_management)
        self.label_operator_name_call.setGeometry(QtCore.QRect(540, 10, 101, 16))
        self.label_operator_name_call.setObjectName("label_operator_name_call")
        self.edit_id_call = QtWidgets.QLineEdit(self.widget_calls_management)
        self.edit_id_call.setGeometry(QtCore.QRect(50, 30, 113, 20))
        self.edit_id_call.setObjectName("edit_id_call")
        self.edit_num = QtWidgets.QLineEdit(self.widget_calls_management)
        self.edit_num.setGeometry(QtCore.QRect(220, 30, 113, 20))
        self.edit_num.setObjectName("edit_num")
        self.edit_hours = QtWidgets.QLineEdit(self.widget_calls_management)
        self.edit_hours.setGeometry(QtCore.QRect(50, 90, 113, 20))
        self.edit_hours.setObjectName("edit_hours")
        self.edit_length = QtWidgets.QLineEdit(self.widget_calls_management)
        self.edit_length.setGeometry(QtCore.QRect(220, 90, 113, 20))
        self.edit_length.setObjectName("edit_length")
        self.button_add_call = QtWidgets.QPushButton(self.widget_calls_management)
        self.button_add_call.setGeometry(QtCore.QRect(390, 90, 331, 25))
        self.button_add_call.setObjectName("button_add_call")
        self.button_add_call.clicked.connect(self.add_call) 

        self.table_management.addTab(self.widget_calls_management, "")
        self.widget_operators_management = QtWidgets.QWidget()
        self.widget_operators_management.setObjectName("widget_operators_management")
        self.label_id_operator = QtWidgets.QLabel(self.widget_operators_management)
        self.label_id_operator.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.label_id_operator.setObjectName("label_id_operator")
        self.label_firstname = QtWidgets.QLabel(self.widget_operators_management)
        self.label_firstname.setGeometry(QtCore.QRect(140, 20, 101, 16))
        self.label_firstname.setObjectName("label_firstname")
        self.edit_id_operator = QtWidgets.QLineEdit(self.widget_operators_management)
        self.edit_id_operator.setGeometry(QtCore.QRect(10, 40, 113, 20))
        self.edit_id_operator.setObjectName("edit_id_operator")
        self.edit_firstname = QtWidgets.QLineEdit(self.widget_operators_management)
        self.edit_firstname.setGeometry(QtCore.QRect(140, 40, 113, 20))
        self.edit_firstname.setObjectName("edit_firstname")
        self.edit_lastname = QtWidgets.QLineEdit(self.widget_operators_management)
        self.edit_lastname.setGeometry(QtCore.QRect(270, 40, 113, 20))
        self.edit_lastname.setText("")
        self.edit_lastname.setObjectName("edit_lastname")
        self.label_name = QtWidgets.QLabel(self.widget_operators_management)
        self.label_name.setGeometry(QtCore.QRect(270, 20, 101, 16))
        self.label_name.setObjectName("label_name")
        self.label_birthdate = QtWidgets.QLabel(self.widget_operators_management)
        self.label_birthdate.setGeometry(QtCore.QRect(400, 20, 101, 16))
        self.label_birthdate.setObjectName("label_birthdate")
        self.edit_birthdate = QtWidgets.QLineEdit(self.widget_operators_management)
        self.edit_birthdate.setGeometry(QtCore.QRect(400, 40, 113, 20))
        self.edit_birthdate.setText("")
        self.edit_birthdate.setObjectName("edit_birthdate")
        self.label_income = QtWidgets.QLabel(self.widget_operators_management)
        self.label_income.setGeometry(QtCore.QRect(530, 20, 101, 16))
        self.label_income.setObjectName("label_income")
        self.edit_income = QtWidgets.QLineEdit(self.widget_operators_management)
        self.edit_income.setGeometry(QtCore.QRect(530, 40, 113, 20))
        self.edit_income.setText("")
        self.edit_income.setObjectName("edit_income")

        self.button_add_operator = QtWidgets.QPushButton(self.widget_operators_management)
        self.button_add_operator.setGeometry(QtCore.QRect(10, 70, 761, 25))
        self.button_add_operator.setObjectName("button_add_operator")

        # on connecte le signal "clicked" a la methode appui_bouton
        self.button_add_operator.clicked.connect(self.add_operator) 

        self.table_management.addTab(self.widget_operators_management, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.combo_state = QtWidgets.QComboBox(self.tab)
        self.combo_state.setGeometry(QtCore.QRect(10, 60, 121, 22))
        self.combo_state.setObjectName("combo_state")
        self.combo_state.addItem("*")
        self.combo_state.addItem("inprogress")
        self.combo_state.addItem("finished")
        self.combo_state.addItem("ignored")
        self.combo_state.addItem("unaffected")

        self.label_filter = QtWidgets.QLabel(self.tab)
        self.label_filter.setGeometry(QtCore.QRect(10, 10, 211, 16))
        self.label_filter.setObjectName("label_filter")
        self.combo_operator = QtWidgets.QComboBox(self.tab)
        self.combo_operator.setGeometry(QtCore.QRect(170, 60, 121, 22))

        self.combo_operator.setObjectName("combo_operator")
        self.combo_operator.addItem("Tous")
        for operator_name in operator_list:
            self.combo_operator.addItem(operator_name)

        self.label_state = QtWidgets.QLabel(self.tab)
        self.label_state.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.label_state.setObjectName("label_state")
        self.label_operator = QtWidgets.QLabel(self.tab)
        self.label_operator.setGeometry(QtCore.QRect(170, 40, 61, 16))
        self.label_operator.setObjectName("label_operator")
        self.button_rechercher = QtWidgets.QPushButton(self.tab)
        self.button_rechercher.setGeometry(QtCore.QRect(530, 100, 251, 25))
        self.button_rechercher.setObjectName("button_rechercher")
        self.button_rechercher.clicked.connect(self.display_all_calls_with_filter) 

        self.table_management.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.table_management.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    """ 
    Gestion des textes dans l'UI
    """
    def retranslateUi(self, MainWindow): 
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Call center"))
        self.label_id_call.setText(_translate("MainWindow", "ID"))
        self.label_hours.setText(_translate("MainWindow", "Heure (hh:mm:ss)"))
        self.label_num.setText(_translate("MainWindow", "Numero"))
        self.label_length_call.setText(_translate("MainWindow", "Duree (s)"))
        self.label_5.setText(_translate("MainWindow", "Statut"))

        self.combo_state_call.setItemText(0, _translate("MainWindow", "En cours"))
        self.combo_state_call.setItemText(1, _translate("MainWindow", "Fini"))
        self.combo_state_call.setItemText(2, _translate("MainWindow", "Igoré"))
        self.combo_state_call.setItemText(3, _translate("MainWindow", "Non-affecté"))

        self.combo_state.setItemText(0, _translate("MainWindow", "Tous"))
        self.combo_state.setItemText(1, _translate("MainWindow", "En cours"))
        self.combo_state.setItemText(2, _translate("MainWindow", "Fini"))
        self.combo_state.setItemText(3, _translate("MainWindow", "Igoré"))
        self.combo_state.setItemText(4, _translate("MainWindow", "Non-affecté"))

        self.label_operator_name_call.setText(_translate("MainWindow", "Operateur"))
        self.button_add_call.setText(_translate("MainWindow", "Ajouter l\'appel"))

        self.table_management.setTabText(self.table_management.indexOf(self.widget_calls_management), _translate("MainWindow", "Appels"))
        self.label_id_operator.setText(_translate("MainWindow", "ID"))
        self.label_firstname.setText(_translate("MainWindow", "Prénom"))
        self.label_name.setText(_translate("MainWindow", "Nom"))
        self.label_birthdate.setText(_translate("MainWindow", "Date de naissance"))
        self.label_income.setText(_translate("MainWindow", "Date d\'arrivée"))
        self.button_add_operator.setText(_translate("MainWindow", "Ajouter l\'opérateur"))
        self.table_management.setTabText(self.table_management.indexOf(self.widget_operators_management), _translate("MainWindow", "Operateurs"))
    
        self.label_filter.setText(_translate("MainWindow", "Filtres"))
        self.combo_operator.setItemText(0, _translate("MainWindow", "Tous"))


        for i, operator_name in enumerate(operator_list):
            print(operator_name + " : " + str(i))
            self.combo_operator.setItemText(i+1, _translate("MainWindow", operator_name))

        self.label_state.setText(_translate("MainWindow", "Etat"))
        self.label_operator.setText(_translate("MainWindow", "Opérateur"))
        self.button_rechercher.setText(_translate("MainWindow", "Rechercher"))
        self.table_management.setTabText(self.table_management.indexOf(self.tab), _translate("MainWindow", "Filtres"))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__" :
    app = QtWidgets.QApplication( sys.argv )

    #my_array = cc.get_calls_with_state('unaffected')
    my_array = cc.get_all_calls()
    operator_list = cc.get_all_operators_names()

    myWindow =MainWindow()
    myWindow.show()
    
    #app.exec()
    sys.exit( app.exec_() )

