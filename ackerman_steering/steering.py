# https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
# https://stackoverflow.com/questions/43397162/show-matplotlib-plots-and-other-gui-in-ubuntu-wsl1-wsl2
import sys
import numpy as np
import matplotlib.pyplot as plt

from math import pi

track     =151.8	# mm, width
wheel_base=166.3	# mm, height

# Cool stuff
# If wheel_base >> track
# - a super long car
# - ang_right=-90~90
# - ang_left =ang_right
# - ex. wheel_base=1	    # mm, height

# If wheel_base << track
# - a super short car
# - ang_right=-90~90
# - ang_left=0
# - ex. wheel_base=10000	# mm, height

###############################################
#
#					#=====================#
#					|                     |
#					|                     |
#					|                     | W
#					|                     | h
#					|                     | e
#					|                     | e
#					|                     | l
#					|                     |
#					|                     | B
#					|                     | a
#					|                     | s
#					|                     | e
#					|                     |
#					|                     |
#					|                     |
#	!---------------#=====================#
#          d                 track
#
###############################################


###############################################
# Calculation
###############################################
ang_right_list=np.arange(-90, 91)

# Ideal
ideal_ang_left_list=[]
for ang_right in ang_right_list:

	if ang_right>0:
		d=wheel_base/np.tan(ang_right/180*pi)
		ang_left=np.arctan(wheel_base/(track+d))
		ang_left=ang_left/pi*180
		ideal_ang_left_list.append(ang_left)

	if ang_right<0:
		d=wheel_base/np.tan(-ang_right/180*pi)
		ang_left=np.arctan(wheel_base/(d-track))
		ang_left=-ang_left/pi*180
		ideal_ang_left_list.append(ang_left)

	if ang_right==0:
		ideal_ang_left_list.append(0)


# Ackeman
# Ackeman_ang_left_list=[]
# for ang_right in ang_right_list:



###############################################


class TextResizer():
    def __init__(self, texts, fig=None, ax=None, minimal=4):
        if not fig: fig = plt.gcf()
        if not ax: ax = plt.gca()
        self.ax=ax
        self.fig=fig
        self.texts = texts
        self.fontsizes = [t.get_fontsize() for t in self.texts]
        _, self.windowheight = fig.get_size_inches()*fig.dpi
        self.minimal= minimal

    def __call__(self, event=None):
        scale = event.height / self.windowheight
        for i in range(len(self.texts)):
            newsize = np.max([int(self.fontsizes[i]*scale), self.minimal])
            self.texts[i].set_fontsize(newsize)

        newsize = np.max([int(12*scale), self.minimal])
        self.ax.legend(prop={'size': newsize})


###############################################
# Plot
###############################################
f =plt.figure()
ax=f.add_subplot(1, 1, 1)

l1=ax.plot(ang_right_list, ang_right_list,      label='Simple')
l2=ax.plot(ang_right_list, ideal_ang_left_list, label='Ideal')

ax.legend()

ax.hlines(y=0, xmin=-90, xmax=90, linewidth=2, color='r')

ax.set_xlim(-90, 90)
ax.set_ylim(-90, 90)

# Major ticks every 20, minor ticks every 5
major_ticks=np.arange(-90, 90, 20)
minor_ticks=np.arange(-90, 90, 5)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

t1=ax.set_title("Ackeman Steering")
t2=ax.set_xlabel("Right front wheel steering angle (deg)")
t3=ax.set_ylabel("Left front wheel steering angle (deg)")
t4=ax.get_xticklabels()
t5=ax.get_yticklabels()
lst_text=[t1, t2, t3]
lst_text.extend(t4)
lst_text.extend(t5)

cid=plt.gcf().canvas.mpl_connect("resize_event", TextResizer(lst_text))

plt.show()
###############################################