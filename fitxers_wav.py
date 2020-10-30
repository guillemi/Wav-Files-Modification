
"""
    
    Autors: Marc Léon Gimeno i Guillem Martínez-illescas Ruíz

"""

import struct

"""

    Funció de lectura d'un fitxer WAV

"""

def lectura_WAV(fitxer):
    
    # fm: freqüència de mostratge
    
    f = open(fitxer, 'rb') # Obrim el fitxer en mode de lectura i binari
    
    formato = '<24si' # Eliminem els primers 24 bytes i agafem els 4 bytes següents (és la fm)
    
    dades = f.read(struct.calcsize(formato)) # Llegim la fm
    
    cc, fm = struct.unpack(formato, dades) # Traduïm la fm
    
    formato = '12si'
    
    dades = f.read(struct.calcsize(formato))
    
    cc, num_bytes = struct.unpack(formato, dades) # Total de mostres
    
    num_mostres = num_bytes//2 # Cada mostra són 2 bytes. Per tant, el nombre de mostres seran el total de bytes entre dos
    
    num_mostres = str(num_mostres) # Passem a string per fer el format
    
    formato = '<' + num_mostres + 'h' # Construïm el format
    
    dades = f.read(struct.calcsize(formato)) # Calculem les dades
    
    mostres = struct.unpack(formato, dades) # Traduïm les mostres a valors enters
    
    f.close() # Tanquem el fitxer 
    
    return fm, mostres # retornem la fm i les mostres d'audio

"""
    
    Funció d'escriptura d'un fitxer WAV

"""

def escriptura_WAV(fitxer, freq_mostratge, senyal_audio):
    
    f = open(fitxer, 'wb') # Obrim el fitxer a escriure
    
    num_mostres = len(senyal_audio) # Nombre de mostres del senyal d'audio
    
    bytes_senyal = num_mostres * 2 # número de bytes a codificar del senyal
    
    formato = 'i'
    
    bs_cod = struct.pack(formato, bytes_senyal)
    
    formato = str(num_mostres) + 'h' # Format per codificar l'àudio
    
    senyal_codificat = struct.pack(formato, *senyal_audio) # Senyal codificat 
    
    formato = 'i' # Codifiquem un enter de 4 bytes
    
    fm_cod = struct.pack(formato, freq_mostratge)
    
    cap1 = b'RIFFZ\xee\x02\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00'
    cap2 = b'\x88X\x01\x00\x02\x00\x10\x00data'
    
    # Escrivim en el fitxer de sortida
    
    f.write(cap1)
    f.write(fm_cod)
    f.write(cap2)
    f.write(bs_cod)
    f.write(senyal_codificat)
    
    f.close() # Tanquem el fitxer

"""

    Funció de delmació

"""

def delmat(senyal_audio, D):
    
    l = len(senyal_audio) # Calculem el nombre de mostres del senyal
    delmacio = [senyal_audio[0]] # Omplim un nou senyal amb la primera mostra
    
    pos = D # pos s'utilitza per calcular la posició dins de la llista de mostres del senyal
    
    while pos <= l - 1:
        delmacio.append(senyal_audio[pos]) # Afegim les mostres al nou senyal
        pos = pos + D
        
    return delmacio # Retornem el senyal

"""
    Funció d'interpolació
    
"""
      
def interpolat(senyal_audio, L):
    
    l = len(senyal_audio)
    interpolacio = [senyal_audio[0]]
    
    pos = 1
    
    while pos <= l - 1:
        
        i = 1
        
        # Afegim els L zeros
        while i <= L:
            
            interpolacio.append(0) 
            i += 1
        
        # Afegim la mostra següent
        interpolacio.append(senyal_audio[pos]) 
        pos += 1
        
    return interpolacio

"""
    
    Adjuntem una segona funció d'interpolació

"""
   
def afegir_zeros(L, senyal):
    
    for l in range(L):
        senyal.append(0)
    return senyal
         
def interpolat1(senyal_audio, L):
   
    l = len(senyal_audio)
    sen=[]
    i=0
   
    while i<l-1:
        if i%2:
            sen=afegir_zeros(L,sen)
           
        else:
            sen.append(senyal_audio[i])
   
        i+=1
    return sen

"""
    
    Test de functions

"""

# 1. Llegim el fitxer prova.wav
# 2. Guardem la freqüència de mostratge a la variable 'fm'
# 3. Guardem les mostres d'àudio a la variable 'audio'

fm, audio = lectura_WAV("prova.wav") 

# 4. Fem una delmació del senyal per D = 2

D = 2
delmacio = delmat(audio, D)

# 5. Guardem el senyal delmat sense modificar la freqüència de mostratge

escriptura_WAV("delmacio_malament.wav", fm, delmacio)

# 6. Guardem el senyal delmat modificant la freqüència de mostratge d'acord amb la delmació

escriptura_WAV("delmacio_correcte.wav", fm//D, delmacio)

# 7. Fem una interpolació per L = 2

L = 2
interpolacio = interpolat1(audio, L)

# 8. Guardem el senyal interpolat sense modificar la freqüència de mostratge

escriptura_WAV("interpolacio_malament.wav", fm, interpolacio)

# 9. Guardem el senyal interpolat modificant la freqüència de mostratge

escriptura_WAV("interpolacio_correcte.wav", fm*L, interpolacio)

# 10. Fem el mateix per la funcio interpolat1

interpolacio1 = interpolat1(audio, L)

escriptura_WAV("interpolat_1_malament.wav", fm, interpolacio1)
escriptura_WAV("interpolat_1_correcte.wav", fm*L, interpolacio1)