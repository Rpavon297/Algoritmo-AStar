
# coding: utf-8

# In[2]:


import math, time, random, sys
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QMessageBox
from PyQt5 import uic, QtGui



#ROBERTO PAVON BENITEZ
class Node:
    def __init__(self, parent = None, position = None, value = 0):
        self.parent = parent
        self.position = position
        self.value = value
        
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __eq__(self, other):
        return self.position == other.position

def dist(start,end):
    return math.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
    
def astar(matrix, start, end):
    dirs = [[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1],[1,-1],[-1,1]]
    nodo_origen = Node(None,start,0)
    nodo_destino = Node(None,end,0)
    
    nodo_origen.g=nodo_origen.h=nodo_origen.f=0
    nodo_destino.g=nodo_destino.h=nodo_destino.f=0
    
    labierta = []
    lcerrada = []
    path = []
    
    flag = False
    
    labierta.append(nodo_origen)
    
    while len(labierta) > 0:
        nodo_actual = labierta[0]
        indice = 0
        
        for index, item in enumerate(labierta):
            if(item.f < nodo_actual.f):
                nodo_actual = item
                indice = index
        
        lcerrada.append(nodo_actual)
        labierta.pop(indice)
        
        if nodo_actual == nodo_destino:
            path = []
            actual = nodo_actual
            while actual is not None:
                path.append(actual.position)
                actual = actual.parent
            return path[::-1]
        
        else:
            for dir in dirs:
                nx = nodo_actual.position[0] + dir[0]
                ny = nodo_actual.position[1] + dir[1]
                
                if len(matrix[0]) > nx >= 0 <= ny < len(matrix):
                    if matrix[nx][ny] != -3:
                        nuevo_nodo = Node(nodo_actual,[nx, ny], matrix[nx][ny])
                        nuevo_nodo.g = nodo_origen.g + 1
                        nuevo_nodo.h = dist(nuevo_nodo.position, nodo_destino.position) + matrix[nx][ny]
                        nuevo_nodo.f = nuevo_nodo.g + nuevo_nodo.h

                        if nuevo_nodo not in labierta and nuevo_nodo not in lcerrada:
                            labierta.append(nuevo_nodo)

                        elif nuevo_nodo in labierta:
                            i = labierta.index(nuevo_nodo)
                            if nuevo_nodo.g > labierta[i].g:
                                labierta.pop(i)
                                labierta.append(nuevo_nodo)
                            
qtCreatorFile = "GUIastar.ui" 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.createButton.clicked.connect(self.createBoard)
        self.ui.loadButton.clicked.connect(self.loadBoard)
        self.ui.randomizeButton.clicked.connect(self.randomize)
        self.ui.goButton.clicked.connect(self.go)
        
        self.createBoard()
         
    def randomize(self):
        rows = len(self.board) - 1
        columns = len(self.board[0]) - 1
        nobs = self.ui.nobst.value()
        
        for i in range(nobs):
            x = random.randint(0,rows)
            y = random.randint(0,columns)
                
            while self.board[x][y] != 0:
                x = random.randint(0,rows)
                y = random.randint(0,columns)
            self.board[x][y] = self.ui.alt_obst.value()
        self.showBoard()
            
    def createBoard(self):
        rows = self.ui.nrows.value()
        columns = self.ui.ncolumns.value()
        
        self.board = np.zeros((rows,columns))
        self.waypoints = []
        self.riesgo = np.zeros((rows,columns))
        self.origen = []
        self.meta = []
        
        self.showBoard()
    
    def loadBoard(self):
        nrows = self.ui.boardMatrix.rowCount()
        ncol = self.ui.boardMatrix.columnCount()
        
        for i in range(nrows):
            for j in range(ncol):
                cell = self.ui.boardMatrix.item(i,j).text()
                if cell == "w" or "W" in cell or "WAYPOINT" in cell:
                    self.board[i][j] = -5
                    if [i,j] not in self.waypoints:
                        self.waypoints.append([i,j])
                elif "RIESGO" in cell or "r" in cell or "R" in cell:
                    self.riesgo[i][j] = int(cell[-1:])
                    self.board[i][j] = -6
                elif "M" in cell or "m" in cell or "M" in cell:
                    self.board[i][j] = -1
                    if([i,j] not in self.meta):
                        self.meta.append([i,j])
                elif "O" in cell or "o" in cell or "O" in cell:
                    self.board[i][j] = -2
                    if[i,j] not in self.origen:
                        self.origen.append([i,j])
                elif cell == "":
                    self.board[i][j] = 0
                elif cell != "X" and cell != "T":
                    try:
                        num = int(cell)
                        if num >= 1 and num <= 10:
                            self.board[i][j] = num
                        elif num > 10:
                            self.board[i][j] = 10
                        else:
                            self.board[i][j] = 0
                    except ValueError:
                        self.board[i][j] = 0
                        
        for w in self.waypoints:
            if self.board[w[0]][w[1]] != -5 : self.waypoints.remove(w)
        for o in self.origen:
            if self.board[o[0]][o[1]] != -2 : self.origen.remove(o)
        for m in self.meta:
            if self.board[m[0]][m[1]] != -1 : self.meta.remove(m)
        self.showBoard()                
                    
    def showBoard(self):
        self.ui.boardMatrix.setRowCount(len(self.board))
        self.ui.boardMatrix.setColumnCount(len(self.board[0]))                            
        
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell >= 1 and cell <=10:
                    cadena = str(int(cell))
                    self.ui.boardMatrix.setItem(i,j, QTableWidgetItem(cadena))
                    self.ui.boardMatrix.item(i, j).setBackground(QtGui.QColor(115,140-(20*(int(cell))),0))
                    self.ui.boardMatrix.item(i, j).setForeground(QtGui.QColor(255,255,255))
                elif cell == -1:
                    self.ui.boardMatrix.setItem(i,j, QTableWidgetItem("M " + str(self.meta.index([i,j]))))
                    self.ui.boardMatrix.item(i, j).setBackground(QtGui.QColor(150,115,0))
                    self.ui.boardMatrix.item(i, j).setForeground(QtGui.QColor(255,255,255))
                elif cell == -5:
                    self.ui.boardMatrix.setItem(i,j, QTableWidgetItem("W " + str(self.waypoints.index([i,j]) + 1)))
                    self.ui.boardMatrix.item(i, j).setBackground(QtGui.QColor(165,125,0))
                    self.ui.boardMatrix.item(i, j).setForeground(QtGui.QColor(255,255,255))
                elif cell == -6:
                    self.ui.boardMatrix.setItem(i,j, QTableWidgetItem("R " + str(int(self.riesgo[i][j]))))
                    self.ui.boardMatrix.item(i, j).setBackground(QtGui.QColor(200,0,0))
                    self.ui.boardMatrix.item(i, j).setForeground(QtGui.QColor(225,190,0))
                elif cell == -2:
                    self.ui.boardMatrix.setItem(i,j, QTableWidgetItem("O " + str(self.origen.index([i,j]))))
                    self.ui.boardMatrix.item(i, j).setBackground(QtGui.QColor(150,115,0))
                    self.ui.boardMatrix.item(i, j).setForeground(QtGui.QColor(255,255,255))
                elif cell == 0:
                    self.ui.boardMatrix.setItem(i,j, QTableWidgetItem(""))
                    self.ui.boardMatrix.item(i, j).setBackground(QtGui.QColor(80,155,0))
                    self.ui.boardMatrix.item(i, j).setForeground(QtGui.QColor(255,255,255))
                    
        self.ui.boardMatrix.resizeColumnsToContents()
    
    def findpath(self, pos_start, pos_end):
        self.board[pos_start[0]][pos_start[1]] = 0
        self.board[pos_end[0]][pos_end[1]] = 0
        
                
        path = astar(self.board, pos_start,pos_end)
                
                
                
        if not path:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("No existe ningún camino entre ()" + str(pos_start[0] + 1 ) + ", " + str(pos_start[1] + 1) + " y " + str(pos_end[0] + 1) + ", " + str(pos_end[1] + 1))
            msg.setWindowTitle("Inaccesible")
            msg.setStandardButtons(QMessageBox.Ok)
            val = msg.exec_()
            app.processEvents()
            return None
                        
                
        path.remove(pos_start)
        #path.remove(pos_end)
        
        return path
    def findpaths(self, vehiculos):
        path = []
        for j in range(len(vehiculos)-1):
            w_start = vehiculos[j]
            w_end = vehiculos[j+1]
                    
            npath = self.findpath(w_start,w_end)
            if not npath: return None
            else: path.extend(npath)
                
        
        return path
    
    def shownode(self, node, past_node, param): 
        self.ui.boardMatrix.setItem(node[0],node[1], QTableWidgetItem("O"))
        self.ui.boardMatrix.setItem(past_node[0],past_node[1], QTableWidgetItem("X"))
            
        if self.save_board[node[0], node[1]] != 0:
            self.ui.boardMatrix.item(node[0], node[1]).setBackground(QtGui.QColor(115,140-(20*self.save_board[node[0]][node[1]]),0))
        else:
            self.ui.boardMatrix.item(node[0],node[1]).setBackground(QtGui.QColor(80,155,0))
            
        if self.save_board[past_node[0], past_node[1]] != 0:
            self.ui.boardMatrix.item(past_node[0], past_node[1]).setBackground(QtGui.QColor(115,140-(20*self.save_board[past_node[0]][past_node[1]]),0))
        else:                  
            self.ui.boardMatrix.item(past_node[0],past_node[1]).setBackground(QtGui.QColor(80,155,0))
                
        self.ui.boardMatrix.item(node[0], node[1]).setForeground(QtGui.QColor(80,0,0))
        self.ui.boardMatrix.item(past_node[0], past_node[1]).setForeground(QtGui.QColor(0 + (200/(param+1)), 0, 255 - (255/(param+1))))
        if node in self.waypoints:
            self.ui.boardMatrix.setItem(node[0], node[1], QTableWidgetItem("W " + str(self.waypoints.index([node[0], node[1]]) + 1)))
            self.ui.boardMatrix.item(node[0], node[1]).setBackground(QtGui.QColor(165, 125, 0))
            self.ui.boardMatrix.item(node[0], node[1]).setForeground(QtGui.QColor(255, 255, 255))
        if past_node in self.waypoints:
            self.ui.boardMatrix.setItem(past_node[0], past_node[1], QTableWidgetItem("W " + str(self.waypoints.index([past_node[0], past_node[1]]) + 1)))
            self.ui.boardMatrix.item(past_node[0], past_node[1]).setBackground(QtGui.QColor(165, 125, 0))
            self.ui.boardMatrix.item(past_node[0], past_node[1]).setForeground(QtGui.QColor(255, 255, 255))


    def tormenta(self, pos_storm, node, past_node, step, pos_end):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Ha aparecido una tormenta en " + str(pos_storm[0] + 1) + ", " + str(pos_storm[1] + 1))
        msg.setWindowTitle("Atención")
        msg.setStandardButtons(QMessageBox.Ok)
        val = msg.exec_()

        self.ui.boardMatrix.setItem(pos_storm[0], pos_storm[1], QTableWidgetItem("T")) 
        self.ui.boardMatrix.item(pos_storm[0], pos_storm[1]).setForeground(QtGui.QColor(255,255,255))
        self.ui.boardMatrix.item(pos_storm[0], pos_storm[1]).setBackground(QtGui.QColor(0,0,135))

        self.ui.boardMatrix.setItem(node[0],node[1], QTableWidgetItem("X"))                
        self.ui.boardMatrix.item(past_node[0], past_node[1]).setForeground(QtGui.QColor(200,0,0))

        if self.board[node[0], node[1]] != 0:
            self.ui.boardMatrix.item(node[0], node[1]).setBackground(QtGui.QColor(115,140-(20*self.board[node[0]][node[1]]),0))
            self.ui.boardMatrix.item(past_node[0], past_node[1]).setBackground(QtGui.QColor(115,140-(20*self.board[node[0]][node[1]]),0))
        else:                    
            self.ui.boardMatrix.item(past_node[0],past_node[1]).setBackground(QtGui.QColor(80,155,0))
        
        waypoints = self.waypoints.copy()
        waypoints.append(pos_end)
        del waypoints[:step]
        waypoints = [node] + waypoints

        self.board[pos_storm[0],pos_storm[1]] = -3
        return self.findpaths(waypoints)
        
    def go(self):
        self.loadBoard()
        self.prob_tormenta = self.ui.p_tor.value() / 100
        self.save_board = self.board.copy()
        
        v_ejec = self.ui.vel_ejec.value() / 100
        
        meta = 0
        origen = 0
        
        pos_start = []
        pos_end = []
        riesgos = []
        vehiculos = []
        
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell >= self.ui.alt_max.value():
                    self.board[i][j] = -3
                elif cell == -2:
                    origen = origen + 1
                elif cell == -1:
                    meta = meta + 1
                elif cell == -6:
                    riesgos.append([i,j])
                else: self.board[i][j] = 0
        
        if meta == 0 or origen == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Datos incorrectos")
            msg.setInformativeText("Debe haber al menos una meta y un origen")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            val = msg.exec_()
            
        if meta != origen:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Datos incorrectos")
            msg.setInformativeText("Número dispar de metas y origenes")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            val = msg.exec_()
            
        else:    
            for r in riesgos:
                self.board[r[0]][r[1]] = self.riesgo[r[0]][r[1]]
                
            for i in range(len(self.meta)):
                pos_end.append(self.meta[i])
                pos_start.append(self.origen[i])
                
            for i in range(len(pos_start)):
                
                waypoints = self.waypoints.copy()
        
                waypoints.append(pos_end[i])
                waypoints = [pos_start[i]] + waypoints
                vehiculos.append(waypoints)
                
            paths = []
            past_nodes = []
            complete = True
            step = np.zeros(len(vehiculos))
            
            for i in range(len(vehiculos)):
                npath = self.findpaths(vehiculos[i])
                
                if not npath: 
                    complete = False
                    break
                else: 
                    paths.append(npath)
                    past_nodes.append(npath[0])
            if complete:
                i = 0
                checks = np.zeros(len(vehiculos))
                while 0.0 in checks:
                    ocupados = []

                    for j, path in enumerate(paths):
                        if i < len(path):

                            self.shownode(path[i], past_nodes[j],j)
                            past_nodes[j] = path[i]

                            if path[i] in vehiculos[j]:
                                step[j] = step[j] + 1

                            if path[i] in ocupados:
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Warning)
                                msg.setText("Se ha producido una colisión en " + str(path[i+1][0] + 1) + ", " + str(path[i+1][1] + 1))
                                msg.setWindowTitle("Atención")
                                msg.setStandardButtons(QMessageBox.Ok)
                                val = msg.exec_()
                                                                
                                self.shownode(past_nodes[j],past_nodes[j],j)
                                
                                paths[ocupados.index(path[i])] = []
                                paths[j] = []
                            else:
                                prob = random.uniform(0,1)            
                    
                                if prob <= self.prob_tormenta and i < len(path) - 1:
                                    postorm = random.randint(i+1,len(path)-1)

                                    while path[postorm] in vehiculos[j]:
                                        postorm = random.randint(i + 1, len(path) - 1)

                                    nt = path[postorm].copy()
                                    nuevo_path = self.tormenta(path[postorm],path[i],past_nodes[j],int(step[j]),pos_end[j])



                                    del paths[j][i+1:]
                                    if nuevo_path is not None: paths[j].extend(nuevo_path)

                                    for index, t_path in enumerate(paths):
                                        if nt in t_path and index != j:
                                            nw = self.waypoints.copy()
                                            nw.append(vehiculos[index][-1])
                                            del nw[:int( step[index])]
                                            nw = [t_path[i]] + nw

                                            auxp = self.findpaths(nw)

                                            del paths[index][i + 1:]
                                            if auxp is not None: paths[index].extend(auxp)

                            ocupados.append(past_nodes[j])

                        elif i == len(path):
                            self.shownode(past_nodes[j],past_nodes[j],j)
                            checks[j] = 1.0

                    time.sleep(0.2 / v_ejec)
                    app.processEvents()
                    i = i + 1
        self.board = self.save_board
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()

