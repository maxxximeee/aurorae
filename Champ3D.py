from matplotlib.widgets import Slider; import matplotlib.pyplot as plt
from matplotlib.colors import Normalize; import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Repérage
d = lambda α,β,γ,δ,ε,ζ: np.sqrt((α-δ)**2+(β-ε)**2+(γ-ζ)**2)
Θ,Φ = np.linspace(0,np.pi,100), np.linspace(0,2*np.pi,100)
θ,φ = np.meshgrid(Θ,Φ)
x,y,z = (lambda r,θ,φ: r*np.sin(θ)*np.cos(φ), 
		 lambda r,θ,φ: r*np.sin(θ)*np.sin(φ), 
		 lambda r,θ:   r*np.cos(θ))

# Paramétrage
f = plt.figure(); ax = f.add_subplot(projection='3d'); ax.view_init(elev=30,azim=150)
plt.title('Champ dipolaire magnétique en surface',weight='bold'); α=0.3
plt.get_current_fig_manager().set_window_title('Champ dipolaire magnétique en surface')
ax.set_box_aspect([1,1,1]); ax.set_aspect('equal'); ax.axis('equal'); ax.set_axis_off()
S=Slider(ax=f.add_axes([0.88,0.1,0.03,0.8]),label='',color='k',
		 valmin=0,valmax=1,valinit=α,valstep=0.01,orientation='vertical')

# Aimant
ψ = np.linspace(0,2*np.pi,50); xަ,yަ,zަ =0.2*np.cos(ψ),0.2*np.sin(ψ),np.array([-0.75,0.75])
xަ,zަ = np.meshgrid(xަ,zަ); ax.plot_surface(zަ,yަ,xަ,color='k',alpha=0.5)

# Valeurs du champ en surface en mT (N←S←N;⩍↓⊚)
Bx = np.array([[  -4.1,  -4.4,  -3.3, -1.1, 1.4,  1.9,  3.0,  1.8, -0.7, -2.5  ],  # z = 7
			   [ -14.1,  -9.0,  -3.7, -0.8, 1.9,  3.7,  4.2,  1.6, -0.3, -2.4  ],  # z = 6
			   [ -31.4, -17.5,  -4.0, -0.6, 4.5, 10.0,  8.4,  2.0, -2.2, -7.2  ],  # z = 5
			   [ -49.0, -17.0,  -3.9, -0.2, 9.5, 65.5, 12.4,  3.2, -1.5, -6.0  ],  # z = 4
			   [ -13.6,  -5.3,  -0.9,  2.2, 7.3, 17.6,  2.8,  0.1, -4.1, -10.7 ],  # z = 3
			   [  -6.4,  -2.7,  -0.9,  2.5, 4.8,  6.9,  2.2, -1.1, -2.6, -5.5  ],  # z = 2
			   [  -2.6,  -2.7,  -1.9, -1.0, 1.8,  1.4,  1.8,  1.8,  0.1, -1.7  ]]) # z = 1
By = np.array([[   6.7,  5.4,  1.5, -1.1, -4.7,  -6.7, -5.4, -2.0,  0.5,  4.5  ],
			   [  10.2,  4.6, -0.7, -2.3, -5.7,  -8.0, -5.5, -1.5,  0.9,  4.8  ],
			   [  14.3,  3.7, -0.3, -1.5, -6.6, -15.1, -7.5, -1.1,  0.1,  3.4  ],
			   [  -8.7, -5.2, -1.0, -0.3,  1.4,  -3.8, -0.6, -0.9, -1.1, -3.8  ],
			   [ -10.3, -6.1, -1.5,  0.1,  3.9,  12.5,  4.0,  1.1, -1.0, -5.0  ],
			   [  -7.8, -5.7, -1.8,  0.1,  4.8,   9.6,  4.4,  1.0, -1.5, -4.3  ],
			   [  -6.1, -4.8, -1.8,  0.2,  3.7,   6.4,  4.3,  1.4, -2.1, -4.3  ]])
N = np.abs(np.log2(np.sqrt(Bx**2 + By**2))); v = np.max(N); M = N/v

# Vecteurs
q = []; vect = lambda r,θ,φ,l: q.append(ax.quiver( x(r,θ,φ),   y(r,θ,φ),   z(r,θ),
												   x(r+l,θ,φ), y(r+l,θ,φ), z(r+l,θ),
												   length=l,color='w',alpha=1-α))
for i in range(1,7+1):
	for j in range(10): vect(1,i*(np.pi/(7+1)),j*(2*np.pi/10),M[i-1,j]/2)
vect(1, 0,     0, np.abs(np.log2(np.sqrt(0.8**2+4.4**2))/(2*v)))         # z = 8
vect(1, np.pi, 0, np.abs(np.log2(np.sqrt((-0.9)**2+(-4.2)**2))/(2*v)))   # z = 0

# Cartographie thermique
C = np.array([[(x(1,i*(np.pi/(7+1)),j*(2*np.pi/10)),
				y(1,i*(np.pi/(7+1)),j*(2*np.pi/10)),
				z(1,i*(np.pi/(7+1))),M[i-1,j]) for j in range(10)] for i in range(1,7+1)])
N = np.zeros((100,100))
for λ in range(np.size(Θ)):
	for µ in range(np.size(Φ)):
		D,I,J = None,None,None
		for i in range(7):
			for j in range(10):
				Dަ = d( x(1,Θ[λ],Φ[µ]), y(1,Θ[λ],Φ[µ]), z(1,Θ[λ]),
					   C[i][j][0],     C[i][j][1],     C[i][j][2])
				if not D or Dަ < D: D,I,J = Dަ,i,j
		N[µ,λ] = C[I][J][3]
m = plt.cm.ScalarMappable(norm=Normalize(N.min(),N.max()),cmap='plasma')
b = f.colorbar(m,label='Intensité normalisée du champ magnétique',alpha=α,
	cax=make_axes_locatable(plt.gca()).append_axes('right',size=0.1,pad=0.3))
T = ax.plot_surface(x(1,θ,φ),y(1,θ,φ),z(1,θ),alpha=α,edgecolor='w',
					rstride=5,cstride=6,facecolors=m.to_rgba(N),cmap='plasma') # 10,12
def update(val)->None:
	T.set_alpha(val); b.solids.set(alpha=val)
	for v in q: v.set_alpha(1-val)
	plt.gcf().canvas.draw_idle()
ax.set_xlim([-1,1]); ax.set_ylim([-1,1]); ax.set_zlim([-1,1])
S.valtext.set_visible(False); S.on_changed(update); plt.show()
