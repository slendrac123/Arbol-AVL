
class Nodo:
    # Constructor
	def __init__(self,valor=None):
		self.valor=valor
		self.hijo_izquierdo=None
		self.hijo_derecho=None
		self.padre=None # Apuntador al padre del nodo
		self.altura=1 # altura del nodo (max dist. a la hoja)

class ArbolAVL:
    # Constructor
	def __init__(self):
		self.raiz=None

	def __repr__(self):
		if self.raiz==None: return ''
		contenido='\n' # Para usar un string al final
		nodos_act=[self.raiz] # Todos los nodos en el nivel actual
		altura_act=self.raiz.altura # Altura de los nodos en el nivel actual
		sep=' '*(2**(altura_act-1)) # variable de tamaño de separaciones entre elementos

		while True:
			altura_act+=-1 # decremento de la altura actual
			if len(nodos_act)==0: break
			fila_act=' '
			fila_sig=''
			nodos_sig=[]

			if all(n is None for n in nodos_act):
				break

			for n in nodos_act:

				if n==None:
					fila_act+='   '+sep
					fila_sig+='   '+sep
					nodos_sig.extend([None,None])
					continue

				if n.valor!=None:       
					buf=' '*((5-len(str(n.valor)))/2)
					fila_act+='%s%s%s'%(buf,str(n.valor),buf)+sep
				else:
					fila_act+=' '*5+sep

				if n.hijo_izquierdo!=None:  
					nodos_sig.append(n.hijo_izquierdo)
					fila_sig+=' /'+sep
				else:
					fila_sig+='  '+sep
					fila_sig.append(None)

				if n.hijo_derecho!=None: 
					nodos_sig.append(n.hijo_derecho)
					fila_sig+='\ '+sep
				else:
					fila_sig+='  '+sep
					nodos_sig.append(None)

			contenido+=(altura_act*'   '+fila_act+'\n'+altura_act*'   '+fila_sig+'\n')
			nodos_act=nodos_sig
			sep=' '*(len(sep)/2) # recorta el espacio de separación a la mitad
		return contenido

    # Inserta un valor a la raiz si no esta vacio o llama a _insertar()
	def insertar(self,valor):
		if self.raiz==None:
			self.raiz=Nodo(valor)
		else:
			self._insertar(valor,self.raiz)
    
    # Posiciona el nodo adecuado y le inserta el dato correspondiente (no inserta valores repetidos)
	def _insertar(self,valor,nodo_act):
		if valor<nodo_act.valor:
			if nodo_act.hijo_izquierdo==None:
				nodo_act.hijo_izquierdo=Nodo(valor)
				nodo_act.hijo_izquierdo.padre=nodo_act # establece el padre
				self._inspec_insercion(nodo_act.hijo_izquierdo)
			else:
				self._insertar(valor,nodo_act.hijo_izquierdo)
		elif valor>nodo_act.valor:
			if nodo_act.hijo_derecho==None:
				nodo_act.hijo_derecho=Nodo(valor)
				nodo_act.hijo_derecho.padre=nodo_act # establece el padre
				self._inspec_insercion(nodo_act.hijo_derecho)
			else:
				self._insertar(valor,nodo_act.hijo_derecho)
		else:
			print ("Valor ya existente dentro del árbol!")

    # Se asegura de que no este vacio, llama a _imp_arbol()
	def imp_arbol(self):
		if self.raiz!=None:
			self._imp_arbol(self.raiz)
    
    # Interpreta al árbol dando los valores de nos nodos y sus respectivas alturas
	def _imp_arbol(self,nodo_act):
		if nodo_act!=None:
			self._imp_arbol(nodo_act.hijo_izquierdo)
			print ("El nodo {a} tiene altura {b}".format(a = str(nodo_act.valor), b = nodo_act.altura))
			self._imp_arbol(nodo_act.hijo_derecho)
    
    # Retorna 0 si el árbol esta vacio, si no, llama a _altura()
	def altura(self):
		if self.raiz!=None:
			return self._altura(self.raiz,0)
		else:
			return 0
    
    # Retorna el mayor valor de altura entre los nodos
	def _altura(self,nodo_act,altura_act):
		if nodo_act==None: return altura_act
		altura_izquierda=self._altura(nodo_act.hijo_izquierdo,altura_act+1)
		altura_derecha=self._altura(nodo_act.hijo_derecho,altura_act+1)
		return max(altura_izquierda,altura_derecha)

    # Llama a _encontrar() o retorna None si esta vació
	def encontrar(self,valor):
		if self.raiz!=None:
			return self._encontrar(valor,self.raiz)
		else:
			return None
    
    # Retorna el propio nodo buscado si se encuentra en el árbol 
	def _encontrar(self,valor,nodo_act):
		if valor==nodo_act.valor:
			return nodo_act
		elif valor<nodo_act.valor and nodo_act.hijo_izquierdo!=None:
			return self._encontrar(valor,nodo_act.hijo_izquierdo)
		elif valor>nodo_act.valor and nodo_act.hijo_derecho!=None:
			return self._encontrar(valor,nodo_act.hijo_derecho)
    
    # Llama a borrar_nodo() con la ubicación del nodo que contiene el dato a borrar (si lo encuentra)
	def borrar_valor(self,valor):
		return self.borrar_nodo(self.encontrar(valor))

    # Elimina el nodo seleccionado
	def borrar_nodo(self,nodo):

		# Retorna None y un mensaje en caso de no encontrar el nodo respectivo
		if nodo==None or self.encontrar(nodo.valor)==None:
			print ("El nodo que se desea eliminar no está en el árbol!")
			return None 

		# Retorna el menor nodo buscando a la izquierda del nodo dado
		def nodo_menor(n):
			actual=n
			while actual.hijo_izquierdo!=None:
				actual=actual.hijo_izquierdo
			return actual

		# Retorna el numero de hijos de un nodo especifico
		def num_hijos(n):
			num_hijos=0
			if n.hijo_izquierdo!=None: num_hijos+=1
			if n.hijo_derecho!=None: num_hijos+=1
			return num_hijos

		# Obtiene el padre del nodo a eliminar
		nodo_padre=nodo.padre

		# Obtiene el número de hijos del nodo a eliminar
		nodo_hijos=num_hijos(nodo)


        # Detiene (break) operaciones en diferentes casos según
        # la estructura del árbol y nodos creados/eliminados.

		# CASO 1 (El nodo NO tiene hijos)
		if nodo_hijos==0:

			if nodo_padre!=None:
                # remueve la referencia al nodo desde el padre
				if nodo_padre.hijo_izquierdo==Nodo:
					nodo_padre.hijo_izquierdo=None
				else:
					nodo_padre.hijo_izquierdo=None
			else:
				self.raiz=None

		# CASO 2 (El nodo tiene UN solo hijo)
		if nodo_hijos==1:

			# obtiene el nodo del hijo unico
			if Nodo.hijo_izquierdo!=None:
				hijo=Nodo.hijo_izquierdo
			else:
				hijo=Nodo.hijo_derecho

			if nodo_padre!=None:
                # remplazar el nodo a borrar por su hijo
				if nodo_padre.hijo_izquierdo==Nodo:
					nodo_padre.hijo_izquierdo=hijo
				else:
					nodo_padre.hijo_derecho=hijo
			else:
				self.raiz=hijo

			# corregir el apuntador al padre del nodo
			hijo.padre=nodo_padre

		# CASO 3 (El nodo tiene DOS hijos)
		if nodo_hijos==2:

            # obtiene el sucesor inorden del nodo borrado
			sucesor=nodo_menor(Nodo.hijo_derecho)

            # copia el valor del sucesor de inorden al nodo anterior
			# manteniendo el valor que deseamos borrar
			Nodo.valor=sucesor.valor

            # borra el sucesor de inorden tras copiarlo dentro del
            # otro nodo

			self.borrar_nodo(sucesor)

            # sale de la función para no llamar a _inspec_borrado() dos veces
			return

		if nodo_padre!=None:
            # corrige la altura del padre del nodo actual
			nodo_padre.altura=1+max(self.obtener_altura(nodo_padre.hijo_izquierdo),self.obtener_altura(nodo_padre.hijo_derecho))

            # empieza a recorrer el árbol hacia atras, asegurandose de
            # si hay más secciones que incumplan las reglas de balanceo
            # de un árbol AVL
			self._inspec_borrado(nodo_padre)

    # Retorna False si esta vació o llama a _buscar()
	def buscar(self,valor):
		if self.raiz!=None:
			return self._buscar(valor,self.raiz)
		else:
			return False

    # Retorna True si encuentra al valor, False de otra manera
	def _buscar(self,valor,nodo_act):
		if valor==nodo_act.valor:
			return True
		elif valor<nodo_act.valor and nodo_act.hijo_izquierdo!=None:
			return self._buscar(valor,nodo_act.hijo_izquierdo)
		elif valor>nodo_act.valor and nodo_act.hijo_derecho!=None:
			return self._buscar(valor,nodo_act.hijo_derecho)
		return False 


	# Funciones para el árbol AVL llamadas al:
	# reordenar (rotar y rebalancear)
	# inspeccionar (adición o eliminación)
    # necesitar obtener la altura de un nodo dado
    # necesitar saber el hijo de mayor altura de un nodo


	def _inspec_insercion(self,nodo_act,path=[]):
		if nodo_act.padre==None: return
		path=[nodo_act]+path

		altura_izquierda =self.obtener_altura(nodo_act.padre.hijo_izquierdo)
		altura_derecha=self.obtener_altura(nodo_act.padre.hijo_derecho)

		if abs(altura_izquierda-altura_derecha)>1:
			path=[nodo_act.padre]+path
			self._balancear_nodo(path[0],path[1],path[2])
			return

		nueva_altura=1+nodo_act.altura 
		if nueva_altura>nodo_act.padre.altura:
			nodo_act.padre.altura=nueva_altura

		self._inspec_insercion(nodo_act.padre,path)

	def _inspec_borrado(self,nodo_act):
		if nodo_act==None: return

		altura_izquierda =self.obtener_altura(nodo_act.hijo_izquierdo)
		altura_derecha=self.obtener_altura(nodo_act.hijo_derecho)

		if abs(altura_izquierda-altura_derecha)>1:
			y=self.hijo_mayor(nodo_act)
			x=self.hijo_mayor(y)
			self._balancear_nodo(nodo_act,y,x)

		self._inspec_borrado(nodo_act.padre)

	def _balancear_nodo(self,z,y,x):
		if y==z.hijo_izquierdo and x==y.hijo_izquierdo:
			self._rotar_derecha(z)
		elif y==z.hijo_izquierdo and x==y.hijo_derecho:
			self._rotar_izquierda(y)
			self._rotar_derecha(z)
		elif y==z.hijo_derecho and x==y.hijo_derecho:
			self._rotar_izquierda(z)
		elif y==z.hijo_derecho and x==y.hijo_izquierdo:
			self._rotar_derecha(y)
			self._rotar_izquierda(z)
		else:
			raise Exception('_balancear_nodo(): configuración de nodos z,y,x no reconocida!')

	def _rotar_derecha(self,z):
		sub_raiz=z.padre 
		y=z.hijo_izquierdo
		t3=y.hijo_derecho
		y.hijo_derecho=z
		z.padre=y
		z.hijo_izquierdo=t3
		if t3!=None: t3.padre=z
		y.padre=sub_raiz
		if y.padre==None:
				self.raiz=y
		else:
			if y.padre.hijo_izquierdo==z:
				y.padre.hijo_izquierdo=y
			else:
				y.padre.hijo_derecho=y		
		z.altura=1+max(self.obtener_altura(z.hijo_izquierdo),
			self.obtener_altura(z.hijo_derecho))
		y.altura=1+max(self.obtener_altura(y.hijo_izquierdo),
			self.obtener_altura(y.hijo_derecho))

	def _rotar_izquierda(self,z):
		sub_raiz=z.padre 
		y=z.hijo_derecho
		t2=y.hijo_izquierdo
		y.hijo_izquierdo=z
		z.padre=y
		z.hijo_derecho=t2
		if t2!=None: t2.padre=z
		y.padre=sub_raiz
		if y.padre==None: 
			self.raiz=y
		else:
			if y.padre.hijo_izquierdo==z:
				y.padre.hijo_izquierdo=y
			else:
				y.padre.hijo_derecho=y
		z.altura=1+max(self.obtener_altura(z.hijo_izquierdo),
			self.obtener_altura(z.hijo_derecho))
		y.altura=1+max(self.obtener_altura(y.hijo_izquierdo),
			self.obtener_altura(y.hijo_derecho))

    # Retorna 0 si el nodo esta vació o su alura definida de otra forma
	def obtener_altura(self,nodo_act):
		if nodo_act==None: return 0
		return nodo_act.altura

    # Retorna el nodo que sea mayor a su hermano (siendo el nodo dado el padre)
	def hijo_mayor(self,nodo_act):
		izquierda=self.obtener_altura(nodo_act.hijo_izquierdo)
		derecha=self.obtener_altura(nodo_act.hijo_derecho)
		return nodo_act.hijo_izquierdo if izquierda>=derecha else nodo_act.hijo_derecho


# Pruebas de uso

arbol = ArbolAVL()

print("Iserta valores")
arbol.insertar(1)
arbol.insertar(2)
arbol.insertar(3)
arbol.insertar(5)
arbol.insertar(10)
arbol.insertar(4)
print(arbol.imp_arbol())

print("borra el 10")
arbol.borrar_valor(10)
print(arbol.imp_arbol())

print("inserta el 3 de nuevo")
arbol.insertar(3) # se repite, no se inserta
print(arbol.imp_arbol())

print("Altura: ",arbol.altura())

if arbol.encontrar(5):
    print("Si esta!")
else:
    print("No esta!")
    
if arbol.encontrar(10):
    print("Si esta!")
else:
    print("No esta!")
    
print("Search: ",arbol.buscar(1))
