from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QStyledItemDelegate, QMessageBox
from Interface import Ui_MainWindow  # importing our generated file
from PyQt5 import QtCore, QtWidgets
import sys
import itertools as iter
import numpy as np
from Game import Game
from Player import Player
import qdarkstyle
from PyQt5.Qt import QFont
import re


class CenterDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QStyledItemDelegate.createEditor(self, parent, option, index)
        editor.setAlignment(QtCore.Qt.AlignCenter)
        font = QFont("Century Gothic", 12)
        font.setBold(True)
        editor.setFont(font)
        return editor


def tupleToString(val):

    string = "("

    string2 = "("

    for c in val:

        string = string + str(c) + ","

        string2 += "  ,"

    return string[:-1] + ")", string2[:-1] + ")"


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mywindow, self).__init__()

        self.game = None

        self.strategies = []

        self.players = []

        self.selectedPlayer = 0

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.font = QFont("Century Gothic", 12)

        self.font.setBold(True)

        # INITIALISATION

        self.ui.playersCombo.hide()
        self.ui.label_2.hide()

        self.ui.strategiesTable.setItemDelegate(
            CenterDelegate())
        self.ui.profilesTable.setItemDelegate(
            CenterDelegate())

        self.setPlayers(self.ui.nbPlayers)

        self.createStratagiesTable(self.ui.strategiesTable)

        self.createProfilesTable(self.ui.profilesTable)

        # disable the radios
        self.ui.groupBox.setEnabled(False)

        # disable buttons

        self.ui.starterButton.setEnabled(False)

        # set my style sheet

        self.setFont(self.font)

        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # SIGNALS

        self.ui.generateButton.clicked.connect(self.generateProfiles)
        self.ui.starterButton.clicked.connect(self.lunchGame)
        self.ui.resetButton.clicked.connect(self.resetGame)
        self.ui.playersCombo.currentIndexChanged.connect(self.changePlayer)
        self.activateRadios()

        self.ui.strategiesTable.cellChanged.connect(
            lambda i, j: self.changeFont(i, j, self.ui.strategiesTable))

        self.ui.profilesTable.cellChanged.connect(
            lambda i, j: self.changeFont(i, j, self.ui.profilesTable))

    def changeFont(self, i, j, table):

        table.item(i, j).setFont(self.font)

    def alignTable(self, table):

        for i in range(0, table.rowCount()):

            for j in range(0, table.columnCount()):

                if(table.item(i, j)):

                    table.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)

    def activateRadios(self):

        self.ui.r1.toggled.connect(lambda: self.updateResults(self.ui.r1))
        self.ui.r2.toggled.connect(lambda: self.updateResults(self.ui.r2))
        self.ui.r3.toggled.connect(lambda: self.updateResults(self.ui.r3))
        self.ui.r4.toggled.connect(lambda: self.updateResults(self.ui.r4))
        self.ui.r5.toggled.connect(lambda: self.updateResults(self.ui.r5))
        self.ui.r6.toggled.connect(lambda: self.updateResults(self.ui.r6))
        self.ui.r7.toggled.connect(lambda: self.updateResults(self.ui.r7))

    def setPlayers(self, spinner):

        # minimum value == at least 2 players

        spinner.setMinimum(2)
        spinner.lineEdit().setReadOnly(True)
        spinner.valueChanged.connect(self.changeNbPlayers)

    def changeNbPlayers(self):

        spinner = self.ui.nbPlayers
        strTable = self.ui.strategiesTable

        value = spinner.value()

        if value > strTable.rowCount():

            strTable.setRowCount(value)

            strTable.setItem(
                value - 1, 0, QTableWidgetItem("Player" + str(value)))

            strTable.setItem(
                value - 1, 1, QTableWidgetItem(""))

            strTable.item(value - 1, 0).setFont(self.font)

        else:
            strTable.removeRow(strTable.rowCount() - 1)

        self.alignTable(strTable)

# change the player in combo box
    def changePlayer(self):

        self.selectedPlayer = self.ui.playersCombo.currentIndex()

        if self.ui.r2.isChecked():
            self.updateResults(self.ui.r2)

        if self.ui.r3.isChecked():
            self.updateResults(self.ui.r3)

        if self.ui.r5.isChecked():
            self.updateResults(self.ui.r5)

    def createStratagiesTable(self, table):

        # setting shape

        table.setRowCount(2)

        table.setColumnCount(2)

        # those two lines are to make the columns fit the widget

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.horizontalHeader().setStretchLastSection(True)

        # insert horiz header

        table.setHorizontalHeaderLabels(["Player", "Strategies"])

        # set init items

        table.setItem(0, 0, QTableWidgetItem("Player1"))
        table.setItem(1, 0, QTableWidgetItem("Player2"))

        table.setItem(0, 1, QTableWidgetItem(""))
        table.setItem(1, 1, QTableWidgetItem(""))

        table.item(0, 0).setFont(self.font)
        table.item(1, 0).setFont(self.font)

        self.alignTable(table)

    def createProfilesTable(self, table):

        # setting shape

        table.setRowCount(0)

        table.setColumnCount(2)

        # those two lines are to make the columns fit the widget

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.horizontalHeader().setStretchLastSection(True)

        table.setHorizontalHeaderLabels(
            ["Profile", "Payoffs"])

        self.alignTable(table)

    def generateProfiles(self):

        if(self.correctStrategies()):

            # ofc gotta check if table is correctly filled

            strTable = self.ui.strategiesTable

            profilesTable = self.ui.profilesTable

            self.strategies = []

            players = []

            # put the strategies in a list and get the players to fill the comboBox

            for i in range(0, strTable.rowCount()):

                item = str(strTable.item(i, 1).text())

                players.append(str(strTable.item(i, 0).text()))

                item = item.replace(" ", "")

                self.strategies.append(item.split(','))

            profiles = list(iter.product(*self.strategies))

            # ajouter les profils crées

            profilesTable.setRowCount(len(profiles))

            for i in range(0, len(profiles)):

                # this is to get a string version of the row
                p, g = tupleToString(profiles[i])

                # this is to disable changes on profiles
                item = QTableWidgetItem(p)
                item.setFlags(QtCore.Qt.ItemIsEnabled)

                # we complete the payoff matrix
                profilesTable.setItem(
                    i, 0, item)

                profilesTable.item(i, 0).setFont(self.font)

                profilesTable.setItem(
                    i, 1, QTableWidgetItem(g))

                profilesTable.item(i, 1).setFont(self.font)

            # set players in the combo box

            self.ui.playersCombo.addItems(players)

            # disable strategies table
            self.disableTable(self.ui.strategiesTable, self.ui.generateButton)

            # make the spinner non selectable

            self.ui.nbPlayers.setEnabled(False)

            # make the starter button clickable
            self.ui.starterButton.setEnabled(True)

            self.alignTable(profilesTable)

    def correctStrategies(self):

        strTable = self.ui.strategiesTable

        for i in range(0, strTable.rowCount()):

            strategies = str(strTable.item(i, 1).text())
            strategies = strategies.replace(" ", "")

            regex = r'^[0-9a-zA-Z]+(,[0-9a-zA-Z]+)*$'

            if(not bool(re.match(regex, strategies))):

                QMessageBox.about(self, "Error detected",
                                  "Strategies should be separated by a comma.\nExemple : str1 , str2 , str3")

                return False

        return True

    def correctProfiles(self):

        proTable = self.ui.profilesTable

        for i in range(0, proTable.rowCount()):

            profile = str(proTable.item(i, 1).text())
            profile = profile.replace(" ", "")

            supposed_nb = self.ui.nbPlayers.value()-1

            nb_commas = profile.count(",")

            dec = r'[-+]?[0-9]+(\.[0-9]+)?'
            regex = r'^\(' + dec + r'(,'+dec+r')+\)$'

            if(not bool(re.match(regex, profile)) or nb_commas != supposed_nb):

                if(not bool(re.match(regex, profile))):

                    QMessageBox.about(self, "Error detected",
                                      "Syntax Error at row "+str(i+1))
                else:
                    QMessageBox.about(self, "Error detected",
                                      "Incorrect payoffs number at row "+str(i+1))
                return False

        return True

    def lunchGame(self):

        if(self.correctProfiles()):

            profile = []

            self.strategies = np.asarray(self.strategies)

            rows = self.strategies.shape[0]

            profilesTable = self.ui.profilesTable

            for i in range(0, rows):

                row = self.strategies[i]

                profile = []

                # gotta get the profile of a player and convert its values to int

                for j in range(0, profilesTable.rowCount()):

                    value = profilesTable.item(j, 1).text()

                    value = value.replace("(", "")
                    value = value.replace(")", "")
                    value = value.replace(" ", "")

                    inter_profile = value.split(",")

                    profile.append(float(inter_profile[i]))

                player = Player(row, profile)

                self.players.append(player)

            self.game = Game(self.players)

            # disable the profiles table + its button

            self.disableTable(self.ui.profilesTable, self.ui.starterButton)

            # make the radios selectable

            self.ui.groupBox.setEnabled(True)
            self.ui.r1.setChecked(True)
            # calculate nash equilibrium since it s already selected
            self.updateResults(self.ui.r1)

    def updateResults(self, radio):

        if radio.isChecked() == True:

            # hide the combo box
            self.ui.playersCombo.hide()
            self.ui.label_2.hide()

            # clear the results screen
            self.ui.results.clear()

            if radio.objectName() == "r1":

                nash = self.game.nashEquilibrium()

                if nash:

                    for element in nash:
                        self.ui.results.appendPlainText(
                            str(element) + "\n")
                else:
                    self.ui.results.appendPlainText(
                        "There's no Nash equilibrium\n")

            if radio.objectName() == "r2":

                # show the combo box
                self.ui.playersCombo.show()
                self.ui.label_2.show()

                p = self.ui.playersCombo.currentIndex()

                dominant = self.game.strictlyDominantStrategies(p)

                self.ui.results.appendPlainText(
                    self.ui.strategiesTable.item(p, 0).text() + " 's strictly dominant strategy : " + dominant)

            if radio.objectName() == "r3":

                self.ui.playersCombo.show()
                self.ui.label_2.show()
                p = self.ui.playersCombo.currentIndex()

                dominant = self.game.weaklyDominantStrategies(p)

                if dominant:
                    self.ui.results.appendPlainText(
                        self.ui.strategiesTable.item(p, 0).text() + " 's weakly dominant strategies :\n")

                    # display the result
                    for element in dominant:
                        self.ui.results.appendPlainText(str(element))
                else:
                    self.ui.results.appendPlainText(
                        "There is no weakly dominant strategy for this player")

            if radio.objectName() == "r4":

                pareto_opt, pareto_dominances = self.game.paretoOptimal()

                if pareto_dominances:

                    self.ui.results.appendPlainText(
                        "Pareto dominant profiles : \n")

                    for element in pareto_dominances:

                        self.ui.results.appendPlainText(
                            str(element[1]) + " is pareto dominated by " + str(element[0]) + "\n")

                else:

                    self.ui.results.appendPlainText(
                        "No pareto dominance.\n")

                self.ui.results.appendPlainText(
                    "Pareto optimums :\n")

                if(pareto_opt):

                    for element in pareto_opt:

                        self.ui.results.appendPlainText(str(element))
                else:

                    self.ui.results.appendPlainText("No profile")

            if radio.objectName() == "r5":

                self.ui.playersCombo.show()
                self.ui.label_2.show()

                p = self.ui.playersCombo.currentIndex()

                player = self.players[p]

                strategies_security, player_security = self.game.securityLevel(
                    p)

                for i in range(0, len(player.strategies)):

                    self.ui.results.appendPlainText(
                        player.strategies[i] + " 's security level : " + str(strategies_security[i]) + "\n")

                if(self.ui.strategiesTable.item(p, 0)):
                    self.ui.results.appendPlainText(
                        self.ui.strategiesTable.item(p, 0).text() + " 's security level : " + str(player_security) + "\n")

            if radio.objectName() == "r6":

                profiles, dominant_strategies = self.game.iteratedEliminationOfDominatedStrategies(
                    0)

                # print dominated strategies

                for element in dominant_strategies:
                    self.ui.results.appendPlainText(element + "\n")

                # print equilibriums
                self.ui.results.appendPlainText("Equilibriums: \n")

                for profile in profiles:

                    self.ui.results.appendPlainText(str(profile) + "\n")

            if radio.objectName() == "r7":

                profiles, dominant_strategies = self.game.iteratedEliminationOfDominatedStrategies(
                    1)

                # print dominated strategies

                for element in dominant_strategies:
                    self.ui.results.appendPlainText(element + "\n")

                # print equilibriums
                self.ui.results.appendPlainText("Equilibriums: \n")

                for profile in profiles:

                    self.ui.results.appendPlainText(str(profile) + "\n")

    def resetGame(self):

        # set players nb to 2
        self.ui.nbPlayers.setValue(2)

        # clear tables
        self.ui.strategiesTable.clear()
        self.ui.profilesTable.clear()

        self.createStratagiesTable(self.ui.strategiesTable)

        self.createProfilesTable(self.ui.profilesTable)

        # clear and hide combo box
        self.ui.playersCombo.hide()
        self.ui.playersCombo.clear()
        self.ui.label_2.hide()

        # clear plain text
        self.ui.results.clear()

        # reset game's options

        self.game = None
        self.players = []

        # enable the radios
        self.ui.groupBox.setEnabled(False)

        # enable generating and lunching button + spinner
        self.ui.generateButton.setEnabled(True)
        self.ui.starterButton.setEnabled(False)

        self.ui.nbPlayers.setEnabled(True)

    def disableTable(self, table, button):

        for i in range(0, table.rowCount()):

            for j in range(0, table.columnCount()):

                item = table.item(i, j)
                item.setFlags(QtCore.Qt.ItemIsEnabled)

        button.setEnabled(False)


app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())
