from spacepy.pybats.bats import Bats2d
import matplotlib.pyplot as plt

p = r'C:/Users/Maxime/Desktop/SWMF-simulation'
mhd = Bats2d(p + r'/y=0_var_3_e20240510-000000-000_20240510-055900-031.outs')
# mhd.add_pcolor('x','z','p', target=plt.figure())

mhd.calc_ndens()
mhd.switch_frame(0) # range(mhd.attrs['nframe'])
fig, ax, contour, cbar = mhd.add_contour('x','z','N', xlim=[-70,30], ylim=[-25,25])
mhd.add_b_magsphere(ax)

fig.set_size_inches(10, 5)
plt.gca().get_children()[0].remove()

plt.show()
