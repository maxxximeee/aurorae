from matplotlib.patches import FancyArrowPatch; from matplotlib.widgets import Slider
import numpy as np; from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Rectangle; import matplotlib.pyplot as plt

# Coordonnées (cm)
nx    = 17
x,y   = np.arange(-21,22,1),np.arange(-15,16,1)
X,Y   = np.meshgrid(np.arange(2,nx+2,1),np.array([-6,-4,-2,-1,0,1,2,4,6]))
Xަ,Yަ   = np.meshgrid(np.arange(2,nx+2,1),np.arange(-6,6+1))
lx,ly = np.array([0,1,0,1,1,0,1,1]),np.array([6,6,4,4,-2,-4,-4,-6])

# Composantes colinéaires (mT) pour x ≥ 2
Bx = np.array([[ -1.8,-1.3,-0.7,-0.3, 0.1,0.2,0.3,0.4,0.4,0.3,.3,.2,.2,.2,.1,.1,.0],  # y = 6
			   [ -3.6,-1.6, 0.1, 1.1, 1.4,1.5,1.2,1.0,0.8,0.6,.5,.4,.3,.2,.2,.1,.1],  # y = 4
			   [-11.5,-1.8, 7.1, 6.9, 5.1,3.5,2.4,1.7,1.2,0.9,.7,.5,.4,.3,.2,.2,.1],  # y = 2
			   [-35.5,15.0,29.5,17.6, 8.8,5.2,3.2,2.1,1.5,1.0,.8,.6,.4,.3,.3,.2,.1],  # y = 1
			   [    0, 475,99.5,22.8,10.2,5.5,3.3,2.2,1.5,1.1,.8,.6,.5,.4,.3,.2,.2],  # y = 0
			   [    0,-8.0,50.3,20.2, 9.5,5.4,3.4,2.1,1.5,1.0,.8,.6,.4,.3,.2,.2,.1],  # y = -1
			   [-17.4, 2.5,10.3, 8.7, 6.1,3.9,2.7,1.9,1.3,1.0,.7,.5,.4,.3,.2,.1,.1],  # y = -2
			   [ -4.4,-1.9, 0.1, 1.5, 1.8,1.6,1.3,1.1,0.9,0.7,.5,.4,.3,.3,.2,.2,.1],  # y = -4
			   [ -1.8,-1.2,-0.6, 0.1, 0.3,0.4,0.5,0.5,0.4,0.4,.3,.2,.2,.2,.1,.1,.0]]) # y = -6
Lx = np.array([-2.1,-2.0,-4.9,-4.6,-16.1,-5.7,-5.5,-2.3])
# Composantes normales correspondantes (mT)
By = -np.array([[  1.4,   1.8,  1.8, 1.6, 1.3, 1.1, 0.8, .6, .4, .3, .2, .1, .1, .1, .0, 0., 0.],
			    [  4.6,   5.1,  4.4, 3.5, 2.4, 1.7, 1.2, .7, .5, .3, .2, .1, .0, .0, .0, 0., 0.],
				[ 18.2,  23.4, 13.3, 7.0, 3.2, 1.8, 1.0, .6, .3, .2, .1, .0, .0, .0, .0, 0., 0.],
			    [ 57.6,  72.6, 21.4, 6.1, 2.7, 1.2, 0.6, .2, .1, .0, .0, .0, .0, .0, .0, 0., 0.],
			    [    0,  20.5, 11.0, 3.1, 0.8, 0.5, 0.3, .2, .1, .0, .0, .0, .0, .0, .0, 0., 0.],
			    [    0,-140.7,-22.7,-6.3,-2.3,-1.4,-0.8,-.5,-.4,-.3,-.1,-.2,-.2,-.1, .0, 0., 0.],
			    [-26.5, -28.8,-16.0,-6.9,-2.9,-1.5,-0.8,-.5,-.3,-.2,-.2,-.1,-.1,-.1,-.1, 0., 0.],
				[ -5.8,  -6.4, -5.8,-4.3,-3.1,-2.1,-1.5,-1.,-.8,-.5,-.4,-.3,-.3,-.2,-.2,-.2,-.2],
				[ -2.1,  -2.5, -2.3,-2.2,-1.7,-1.5,-1.1,-.9,-.7,-.6,-.5,-.4,-.3,-.3,-.2,-.2,-.1]])
Ly = np.array([0.2,0.8,0.7,2.8,-11.5,-1.1,-3.7,-1.4])

# Tracé de la carte de champ
plt.title('Carte de champ',weight='bold'); assert nx==np.shape(Bx)[1]
plt.grid(alpha=0.5,which='both',zorder=0); l,b,w,h = -3,-0.6,3,1.2
plt.gca().add_patch(Rectangle((l,b),w,h,color='r',zorder=4))
plt.gca().add_patch(Rectangle((l+w,b),w,h,color='b',zorder=4))
plt.get_current_fig_manager().set_window_title('Carte de champ')
plt.xlim([np.min(x),np.max(x)]); plt.xlabel('Axe X (cm)'); plt.xticks(x,minor=True)
plt.ylim([np.min(y),np.max(y)]); plt.ylabel('Axe Y (cm)'); plt.yticks(y,minor=True)
plt.text(l+0.2*w,b+.5*h,'N',c='w',weight='demi',alpha=0.8,ha='center',va='center',size=8,zorder=4)
plt.text(l+1.8*w,b+.5*h,'S',c='w',weight='demi',alpha=0.8,ha='center',va='center',size=8,zorder=4)

# Carte vectorielle (vecteurs axiaux et latéraux)
Q = lambda α,β,dα,dβ,p: plt.quiver(α,β,dα,dβ,scale=100,color='k',width=.003,
								   zorder=3,pivot=p,visible=False)
V = [ Q( X, Y,-Bx,-By,'tip'), Q( -X, -Y,-Bx,-By,'tail'),
	  Q(lx,ly,-Lx,-Ly,'tip'), Q(-lx,-ly,-Lx,-Ly,'tail') ]

# Complétion via la méthode Monte-Carlo avec incertitudes composées
def complete(A:np.ndarray)->np.ndarray:
	Aަ = np.insert(A,[1,2,7,8],0,axis=0)
	for i in [1,3,9,11]:
		for j in range(nx):
			v,u=(Aަ[i-1][j]+Aަ[i+1][j])/2,np.sqrt(2*0.1**2)/2
			Aަ[i][j] = np.mean(np.random.uniform(v-u,v+u,10000))
	return Aަ
Bxަ,Byަ = complete(Bx),complete(By)

# Lignes de champ
L = [plt.streamplot(Xަ,Yަ,-Bxަ,-Byަ,color='k',density=1.5,linewidth=0.7,arrowsize=0.5),
	 plt.streamplot(np.flip(-Xަ),np.flip(-Yަ),np.flip(-Bxަ),np.flip(-Byަ),
			  		color='k',density=1.5,linewidth=0.7,arrowsize=0.5)]

# Carte thermique
a=make_axes_locatable(plt.gca()); α = 0.5
n=np.array([np.array([np.sqrt(Bxަ[i][j]**2+Byަ[i][j]**2)
		   for j in range(np.shape(Xަ)[1])]) for i in range(np.shape(Xަ)[0])])
N=np.zeros((np.size(y),np.size(x)))
for i in range(np.size(y)):
	for j in range(np.size(x)):
		if abs(15-i)<=6:
			if 21-j in range(-18,-2+1): N[i][j] = n[i-9][j-23]
			elif 21-j in range(2,18+1): N[i][j] = np.flip(n)[i-9][j-3]
		# if (21-j,15-i) in zip(lx,ly):
		# 	k=list(zip(lx,ly)).index((21-j,15-i)); N[i][j] = np.sqrt(Lx[k]**2+Ly[k]**2)
		# if (21-j,15-i) in zip(-lx,-ly):
		# 	k=list(zip(-lx,-ly)).index((21-j,15-i)); N[i][j] = np.sqrt(Lx[k]**2+Ly[k]**2)
m=plt.imshow(N,cmap='plasma',interpolation='catrom', # np.log(N+1)
			 extent=[np.min(x),np.max(x),np.min(y),np.max(y)],zorder=3,alpha=α)
S=Slider(ax=a.append_axes('right',size='4%',pad=0.1),label='',
		 valmin=0,valmax=1,valinit=α,valstep=0.01,color='k',orientation='vertical')
b=plt.colorbar(label='Norme du champ (mT)',cax=a.append_axes('right',size='5%',pad=0.1))
def update(val)->None:m.set_alpha(val);b.solids.set(alpha=val);plt.gcf().canvas.draw_idle()
S.valtext.set_visible(False); S.on_changed(update); m.set_clim(0,150) # np.max(N)
def switch(event)->None:
	if event.xdata and int(event.xdata):
		for v in V: v.set_visible(not v.get_visible())
		for s in L: s.lines.set_visible(not s.lines.get_visible())
		for a in plt.gcf().axes[0].get_children():
			if isinstance(a,FancyArrowPatch): a.set_alpha(0 if a.get_alpha() in [1,None] else 1)
		plt.gcf().canvas.draw_idle()
plt.connect('button_press_event',switch); plt.show()

