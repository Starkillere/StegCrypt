import random

csprng = random.SystemRandom()

def pgcde(a:int, b:int):
	r, u, v = a, 1, 0
	rp, up, vp = b, 0, 1
	
	while rp != 0:
		q = r//rp
		rs, us, vs = r, u, v
		r, u, v = rp, up, vp
		rp, up, vp = (rs - q*rp), (us - q*up), (vs - q*vp)
	
	return (r, u, v)

def random_prime(min=100, max=1000) -> int:
    prime_list = []
    for n in range(min, max):
        isPrime = True
        for num in range(2, n):
            if n % num == 0:
                isPrime = False     
        if isPrime:
            prime_list.append(n)
    nb_random_prime = csprng.choice(prime_list)
    return nb_random_prime

def random_number(min=0, max=1000) -> int:
    return csprng.randint(min, max)

def generate_keys() -> dict:
    p,q = random_prime(), random_prime()
    n = p*q
    phi = (p-1) * (q-1)
    r = 10
    d = 0
    while r != 1 or d <= 2 or d >= phi:
        e = random_number()
        r, d, v = pgcde(e, phi)
    return {'key publique':(int(n), int(e)), 'key priver':(int(n),int(d))}

class RSA:
    def chiffrement(self, n, e, text):
        asc = [str(ord(j)) for j in text]
        for i, k in enumerate(asc):
            if len(k) < 3:		
                while len(k) < 3:
                    k = '0' + k
                asc[i] = k       
        ascg = ''.join(asc)
        d , f = 0 , 4
        while len(ascg)%f != 0: 
            ascg = ascg + '0'
        l = []
        while f <= len(ascg):
            l.append(ascg[d:f])
            d , f = f , f + 4
        crypt = [str(((int(i))**e)%n) for i in l]
        texte_crypt = ''
        for i in range(len(crypt)):
            for j in range(len(crypt[i])):
                texte_crypt += chr(int(crypt[i][j])+80)
            texte_crypt += '/Reptemp°'
        
        return texte_crypt
	
    def dechiffrement(self, n, d, texte_crypt):
        texte_crypt = texte_crypt.split('/Reptemp°')[:-1]
        crypt = []
        for i in range(len(texte_crypt)):
            elements = ''
            for j in range(len(texte_crypt[i])):
                elements += str(ord(texte_crypt[i][j])-80)
            crypt.append(elements)    
        resultat = [str((int(i)**d)%n) for i in crypt]
        for i, s in enumerate(resultat):
            if len(s) < 4:
                while len(s) < 4:
                    s = '0' + s
                resultat[i] = s
        g = ''.join(resultat)
        asci = ''
        d , f = 0 , 3
        while f < len(g):
            asci = asci + chr(int(g[d:f]))
            d , f = f , f + 3
        
        return asci