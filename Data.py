from matplotlib.patches import ConnectionPatch; from datetime import date,datetime
import matplotlib.dates as mdates; from locale import setlocale,LC_TIME
import numpy as np; import matplotlib.pyplot as plt

T = 'Analyse géomagnétique statistique (2024)'
# Fonctions de génération
p = lambda s: r'\{}.csv'.format(s)
def µ(b:list[np.ndarray]) -> np.ndarray:
	u = np.unique(np.array([b[0][i][:10] for i in range(np.size(b[0]))]) 
		if len(str(b[0][0]))>10 else b[0],return_inverse=True)
	return np.array([u[0],[b[1].astype(float)[i==u[1]].mean() for i in range(np.shape(u[0])[0])]])
t = lambda b,d=',',h=1,f=0,c=None: µ(np.genfromtxt(p(b),delimiter=d,dtype=None,unpack=1,
												   skip_header=h,skip_footer=f,usecols=c))
g = lambda e,b,c,l: ax[*e].plot(b[0],b[1].astype(float),label=l,color=c,ls='-')

# Bases de données
bgs   = t('bgs2024')
noaa  = t('noaa2024')
goes  = t('goesx052024')
aces  = t('acebs052024')
aced  = t('acedp052024')
gfz   = t('gfz',h=33643,f=41,c=(0,23))
sidc  = t('sidcspot',h=8767,f=31,c=(0,2))
nasa  = t('nasa2024v',d=None,h=0,c=(1,37))
sw    = t('spaceweather',h=20983,f=125,c=(0,5))

# Courbes de tendance
fig,ax = plt.subplots(3,3,sharex='col'); setlocale(LC_TIME,'fr_FR')
fig.suptitle(T,weight='bold',y=0.95); plt.get_current_fig_manager().set_window_title(T)
r = fig.canvas.manager.window.wm_maxsize(); fig.set_size_inches((r[0]/96)/1.5,(r[1]/96)/1.8)

g( (0,0), nasa, 'm', 'NASA (AE)'       )
g( (1,0), bgs,  'b', 'BGS (GFZ Kp)'    )
g( (2,0), noaa, 'b', 'NOAA (GFZ Ap)'   )
g( (0,1), sidc, 'r', 'SIDC (GFZ SN)'   )
g( (1,1), gfz,  'r', 'GFZ (F10.7o)'    )
g( (2,1), sw,   'r', 'SW (F10.7o)'     )
g( (0,2), goes, 'r', r'GOES (X$\Phi$)' )
g( (1,2), aces, 'r', 'ACE (BS)'        )
g( (2,2), aced, 'r', 'ACE (DP)'        )

# Mise en forme
for k in range(np.shape(ax)[1]):
	ax[0,k].xaxis.set_major_locator(mdates.DayLocator() if k==2 else mdates.MonthLocator())
	ax[0,k].xaxis.set_major_formatter(mdates.DateFormatter('%d/05' if k==2 else '%B'))
	X = ax[-1,k].get_lines()[0].get_xdata(); s = ax[-1,k].secondary_xaxis(location=0)
	s.tick_params('x',length=35,width=0.5,labelsize=8); s.set_xticks([(date(2024,5,10
		)-datetime.strptime(X[0],'%Y-%m-%d').date()).days],labels=['Gannon Storm'])
	if k!=2: plt.setp(ax[-1,k].get_xticklabels()[-1],visible=False)
	ax[0,k].set_xlim(X[0],X[-1])
	for l in ax[-1,k].get_xticklabels(which='major'):
		l.set(rotation=30,horizontalalignment='right',fontsize=fig.get_size_inches()[0]//1.5)
	for x in ('2024-05-10','2024-05-13'): ax[-1,k].add_artist(ConnectionPatch(xyA=(x,
		ax[0,k].get_ylim()[1]),xyB=(x,ax[-1,k].get_ylim()[0]),coordsA='data',coordsB='data',
		axesA=ax[0,k],axesB=ax[-1,k],ls='--',lw=0.5,color='k'))
plt.setp([l for l in ax[-1,2].get_xticklabels() if int(l.get_text()[:2])%5!=0],visible=False)
for i,_ in np.ndenumerate(ax): ax[*i].get_yaxis().set_visible(False); ax[*i].legend(loc=1)
plt.subplots_adjust(bottom=0.15); plt.show()
