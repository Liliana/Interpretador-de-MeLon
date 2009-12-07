#! /usr/bin/python
import Nodo,CLS

# Match
def match(nodo1,nodo2):
	print 'MATCH\n -',nodo1,'\n -',nodo2
	# Fin de recursion
	if (not isinstance(nodo1,Nodo.Nodo)) and (not isinstance(nodo2,Nodo.Nodo)):
		#print '- ',nodo1,'\n- ',nodo2
		return nodo1 == nodo2

	# Bajar si el nodo es no_terminal
	if nodo1.type == 'no_terminal' or nodo1.type == '' or nodo1.type == 'PATRON' or nodo1.type == 'sub' or nodo1.type == 'LISTAPATRON' or nodo1.type == 'lp': return match(nodo1.izquierdo,nodo2)
	if nodo2.type == 'no_terminal' or nodo2.type == '' or nodo2.type == 'PATRON' or nodo2.type == 'sub' or nodo2.type == 'LISTAPATRON' or nodo2.type == 'lp': return match(nodo2.izquierdo,nodo1)

	# Variables hacen match con todo
	if nodo1.type == 'VARIABLE' or nodo2.type == 'VARIABLE':
		#print '- Variable\n -'
		return True

	# Constantes
	if nodo1.type == 'CONSTANTE' and nodo2.type == 'CONSTANTE':
		#print '- Constante\n -'
		#print '(',nodo1.type,' ',nodo2.type,')\n'
		return match(nodo1.izquierdo.izquierdo,nodo2.izquierdo.izquierdo)

	# Entero
	if nodo1.type == 'ENTERO' and nodo2.type == 'ENTERO':
		#print '- Entero\n -'
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Booleano
	if nodo1.type == 'BOOLEANO' and nodo2.type == 'BOOLEANO':
	#	print '- Booleano\n -'
		return match(nodo1.izquierdo,nodo2.izquierdo)

	# Listavacia
	if nodo1.type == 'CONSTLV' and nodo2.type == 'CONSTLV':
		#return match(nodo1.izquierdo,nodo2.izquierdo)
		return True

	# Listas
	if nodo1.type == 'LISTA' and nodo2.type == 'LISTA':
		#print 'BLAH'
		return match(nodo1.izquierdo,nodo2.izquierdo) and  match(nodo1.derecho,nodo2.derecho)
	#print 'falso' 

	return False

# Replace
def replace(diccionario,clave,valor):
	diccionario[clave] = valor
	return diccionario

# Extend
def extend(diccionario,clave,valor):
	diccionario[clave] = valor
	return diccionario

# Lookup
def lookup(clave,diccionario):
	#print 'LOOKUP\n',clave.__class__, diccionario
	if clave in diccionario: return diccionario[clave]
	else: raise 'ERROR: variable '+clave+' no definida' 

# Eval
def eval(nodo,env,orientacion):
	if orientacion == 'izquierda': return eval(nodo.izquierdo,env)
	return eval(nodo.derecho,env)

# Valor
def valor(nodo):
	while isinstance(nodo,Nodo.Nodo):
		if nodo.type != 'LISTA':
			nodo = nodo.izquierdo
		else:
			return str(valor(nodo.izquierdo))+'::'+str(valor(nodo.derecho))
	return nodo

# Apply
def apply(cls,nodo):
	for c in cls.clausura:
		#print 'C[0]\n =',valor(c[0])
		if match(c[0],nodo):
			print 'APPLY\n @',cls,'\n @',c[1],'\n @',cls.env,'\n @',extend(cls.env,str(valor(c[0])),valor(nodo))
			#return eval(c[1],extend(cls.env,str(valor(c[0])),valor(nodo)))
			return eval(c[1],extend(cls.env,str(valor(c[0])),valor(nodo)))
	raise 'ERROR APPLY'

#APPLY VIEJO
# 	global num_clausura
# 	#if isinstance(nodo1,Nodo.Nodo) and isinstance(nodo2,Nodo.Nodo): print 'APPLY',nodo1.type,nodo2.type
# 	#print 'APPLY\n -',nodo1,'\n -',nodo2
# 	#if nodo2 is None and nodo1 is None: return
# 	if 'clausura' in env:
# 		#print 'here'#, valor(env['clausura'][0][0]),valor(env['clausura'][1][0])
# 		#print 'APPLY',nodo1,nodo2
# 		#print env
# 		#i=555
# 		for c in env['clausura']:
# 			print '+C0\n +',nodo2,'\n +',c[0],'\n +',c[1],'\n +',env['clausura'][0][1]
# 			if match(nodo2,c[0]):
# 				print 'Macheo \n *',c[1],'\n *',extend(env,str(valor(c[0])),valor(nodo2))
# 				print valor(eval(c[1],extend(env,str(valor(c[0])),valor(nodo2))))
# 				return #eval(c[1],extend(env,str(valor(c[0])),valor(nodo2)))
# 		#	else: return False
# 		#	i+=111
# 		#print 'ERROR',c[0],nodo2
# 		#n = c[0]
# 		#print n.type, nodo2.type
# 		#while isinstance(n,Nodo.Nodo):
# 		#	print n.type
# 		#	n = n.izquierdo
# 		raise 'AA'
# 	else:
# 		#print 'aqui \n ',nodo1,'\n ',nodo2,'\n ' ,env
# 		#print '1zzz'
# 		#print 'ZZ', eval(nodo1,env)
# 		#print '2zzz'
# 		return apply(eval(nodo1,env),eval(nodo2,env),env)
# 		#return apply(eval(nodo2,eval(nodo2,env)),env
	
# Obtener clausura de una funcion
def clausura(nodo,env,temp):
	if isinstance(nodo,Nodo.Nodo):
		if nodo.type == 'lfe':
			temp.append((nodo.izquierdo,nodo.derecho))
		clausura(nodo.izquierdo,env,temp)
		clausura(nodo.derecho,env,temp)
	return CLS.CLS(env,temp)


# Eval
def eval(nodo,env):
	
	if isinstance(nodo,Nodo.Nodo):
		if isinstance(nodo.izquierdo,Nodo.Nodo):
			if isinstance(nodo.derecho,Nodo.Nodo):
				print nodo.type,'\n I: ', nodo.izquierdo.type,'\n D: ',nodo.derecho.type
			else:
				print nodo.type,'\n I: ', nodo.izquierdo.type
		else: print nodo.type
	if not isinstance(nodo,Nodo.Nodo): return nodo
	#if nodo.type == 'lp' or nodo.type == 'arg' or nodo.type == 'arg2': return eval(nodo.izquierdo,env)
	if nodo.type == 'arg': 
		#apply(nodo.izquierdo,nodo.derecho,env)
		#print 'Doble \n ',nodo.izquierdo,'\n ',nodo.derecho
		eval(nodo.izquierdo,env)
		eval(nodo.derecho,env)
		#apply(eval(nodo.izquierdo,env),eval(nodo.derecho,env))
		#print 'Doble2 \n ',nodo.izquierdo,'\n ',nodo.derecho
	#if nodo.type == 'lp' or nodo.type == 'arg2': return eval(nodo.izquierdo,env)
	if nodo.type == 'arg2': return eval(nodo.izquierdo,env)
	if nodo.type == 'lp':return nodo
	elif nodo.type == 'FUN': 
		#print 'In-Fun\n -',nodo.izquierdo,'\n -',nodo.derecho
		return clausura(nodo,env,[])
		#return eval(nodo.izquierdo,env)
	#elif nodo.type == 'LISTAPATRON': return eval(nodo.izquierdo,env)
	elif nodo.type == 'LISTAPATRON' or nodo.type == 'LISTA': return nodo
	elif nodo.type == 'no_terminal': return eval(nodo.izquierdo,env)
	elif nodo.type == 'sub': return eval(nodo.izquierdo,env)
	elif nodo.type == '': return eval(nodo.izquierdo,env)
	#elif nodo.type == 'CONSTANTE': return nodo.izquierdo.izquierdo
	elif nodo.type == 'CONSTANTE':
		#print valor(nodo)
		return nodo
	elif nodo.type == 'CONSTLV': 
		#print nodo.izquierdo
		#return '[]'
		#print nodo.type
		return nodo
	elif nodo.type == 'MAS' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = valor(eval(nodo.izquierdo,env)) + valor(eval(nodo.derecho,env))
		print resultado
	elif nodo.type == 'MENOS' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = valor(eval(nodo.izquierdo,env)) - valor(eval(nodo.derecho,env))
		print resultado
	elif nodo.type == 'NEGATIVO' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = -valor(eval(nodo.izquierdo,env))
		print resultado
	elif nodo.type == 'PRODUCTO' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = valor(eval(nodo.izquierdo,env)) * valor(eval(nodo.derecho,env))
		print resultado
	elif nodo.type == 'COCIENTE' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = valor(eval(nodo.izquierdo,env)) / valor(eval(nodo.derecho,env))
		print resultado
	elif nodo.type == 'MENOR' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str((valor(eval(nodo.izquierdo,env)) < valor(eval(nodo.derecho,env))))).lower()
		print resultado
	elif nodo.type == 'MENOROIGUAL' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) <= valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'MAYOR' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) > valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'MAYOROIGUAL' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) >= valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'IGUAL' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) == valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'DISTINTO' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) != valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'NO' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = not (valor(eval(nodo.izquierdo,env)))
	elif nodo.type == 'OR' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) or  valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'AND' :
		#print 'maz',eval(nodo.izquierdo,env).__class__,'maz1',eval(nodo.derecho,env).__class__,'zam'
		resultado = (str(valor(eval(nodo.izquierdo,env)) and valor(eval(nodo.derecho,env)))).lower()
		print resultado
	elif nodo.type == 'VARIABLE':
		#print 'Pepe',env
		#if 'clausura' in env:
			#print 'pepe'
			#for c in env['clausura']:
			#print '+C0\n +',nodo2,'\n +',c[0]#,'\n +',env['clausura']
			#	if match(nodo,c[0]):
				#print 'Macheo',nodo2,c[0]
			#		print 'aaa', c[1]
			#		return c[1]
		#else:
		return lookup(str(valor(nodo.izquierdo)),env)	
		#return eval(lookup(str(valor(nodo.izquierdo)),env),env)
	#elif nodo.type == 'PATRON': return eval(nodo.izquierdo,env)
	elif nodo.type == 'PATRON': return nodo
	elif nodo.type == 'LET':
		valor_patron = str(nodo.izquierdo.izquierdo.izquierdo.izquierdo.izquierdo)
		env = extend(env,valor_patron,nodo.izquierdo.derecho)
		p = nodo.izquierdo.izquierdo
		e1 = nodo.izquierdo.derecho
		e2 = nodo.derecho
		env1 = extend(env,p,'fake')
		v1 = eval(e1,env1)
		return eval(e2,replace(env1,str(valor(p)),v1))
	elif nodo.type == 'lfe':
		#print 'LFE \n ===>', nodo.derecho
		if 'clausura' in env:
			extend(env,'clausura',env['clausura']+[(nodo.izquierdo,nodo.derecho)])
			#print 'a'
		else:
			extend(env,'clausura',[(nodo.izquierdo,nodo.derecho)])
			#print 'b'
		print'ENV', env, nodo
	elif nodo.type == 'APLICAR':
		#print 'APLICAR',nodo.izquierdo,nodo.derecho
		#apply(nodo.izquierdo,nodo.derecho,env)
		return apply(eval(nodo.izquierdo,env),eval(nodo.derecho,env))

		

		
