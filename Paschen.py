import numpy as np
import matplotlib.pyplot as plt

T = 'Courbe de Paschen pour l\'air à 20°C'
conversion = lambda p: (p/101325)*760
p,d = conversion(9),5 # Torr,cm
x = np.logspace(-0.5,1,10000)

# Constantes pour l'air
A = 15   # cm^-1·Torr^-1
B = 365  # V·cm^-1·Torr^-1
γ = 0.01 # second coefficient de Townsend

# Calcul de la tension de claquage
V = (B*x)/(np.log(A*x)-np.log(np.log(1+1/γ)))

# Tracé de la courbe de Paschen
plt.loglog(x,V,'r-')
plt.ylabel('Tension de claquage (V)')
plt.xlabel('Produit pression-distance (Torr·cm)')
plt.get_current_fig_manager().set_window_title(T)
plt.axvline(p*d,color='k',ls='--',
			label=r'Terrella ($p\approx9\text{ Pa}$ '
				  r'& $d\approx5\text{ cm}$)')
plt.axhline(V[np.argmin(abs(x-p*d))],color='k',ls='--')
plt.title(T,weight='bold'); plt.legend(); plt.show()
print(V[np.argmin(abs(x-p*d))])
