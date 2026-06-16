import numpy as np; import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

T = 'Composition de l\'air et couleurs aurorales'
p = r'\NRLMSIS.csv'
# 01/01/2025 00:00 55/45
b = np.genfromtxt(p,delimiter=',',dtype=float,unpack=1,
				  skip_header=1,usecols=(5,8,9,10,14,15,16,17))
t = sum([b[i] for i in range(1,len(b))])
c = ['red','orange','lime','cyan','blue','darkviolet','magenta']
l = ['$O$','$N_2$','$O_2$','$He$','$Ar$','$H$','$N$']
plt.gca().fill_betweenx([0,100], 50,100,facecolor='mediumvioletred',alpha=0.3)
plt.gca().fill_betweenx([0,100],100,250,facecolor='springgreen',alpha=0.3)
plt.gca().fill_betweenx([0,100],250,400,facecolor='crimson',alpha=0.3)
for i in range(1,len(b)): plt.plot(b[0],100*b[i]/t,ls='-',color=c[i-1],label=l[i-1])

plt.title(T,weight='bold'); plt.get_current_fig_manager().set_window_title(T)
plt.xlabel('Altitude (km)'); plt.ylabel('Pourcentage volumique (%)')
plt.gca().yaxis.set_major_formatter(PercentFormatter())
plt.ylim(0,100); plt.xlim(0,1000); plt.legend(); plt.show()
