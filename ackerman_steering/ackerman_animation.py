import sys
import time

from math import pi

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.animation as animation

pkmn_type_colors=['#78C850',  # Grass
                  '#F08030',  # Fire
                  '#6890F0',  # Water
                  '#A8B820',  # Bug
                  '#A8A878',  # Normal
                  '#A040A0',  # Poison
                  '#F8D030',  # Electric
                  '#E0C068',  # Ground
                  '#EE99AC',  # Fairy
                  '#C03028',  # Fighting
                  '#F85888',  # Psychic
                  '#B8A038',  # Rock
                  '#705898',  # Ghost
                  '#98D8D8',  # Ice
                  '#7038F8']  # Dragon

color_used=pkmn_type_colors

def update(val):
    global ackerman
    global s_ackpoint_offset, s_stepin, s_taillen, s_angfrw

    ackerman.ackpoint_offset=s_ackpoint_offset.val
    ackerman.stepin         =s_stepin.val
    ackerman.taillen        =s_taillen.val
    ackerman.angfrw         =s_angfrw.val

def reset(event):
    global ackerman
    global s_stepin, s_taillen, s_ackpoint_offset, s_angfrw
    s_stepin.reset()
    s_taillen.reset()
    s_ackpoint_offset.reset()
    s_angfrw.reset()

    ackerman.ackpoint_offset=s_ackpoint_offset.val
    ackerman.stepin         =s_stepin.val
    ackerman.taillen        =s_taillen.val
    ackerman.angfrw         =s_angfrw.val


class Ackerman:
    """Double Pendulum Class

    init_state is [theta1, omega1, theta2, omega2] in degrees,
    where theta1, omega1 is the angular position and velocity of the first
    pendulum arm, and theta2, omega2 is that of the second pendulum arm
    """
    def __init__(self,
                 track          =100,
                 wheel_base     =100,
                 ackpoint_offset=0,
                 taillen        =0,
                 stepin         =0,
                 angfrw         =0): 

        self.track          =track
        self.wheel_base     =wheel_base

        self.angfrw         =angfrw
        self.ackpoint_offset=ackpoint_offset
        self.taillen        =taillen
        self.stepin         =stepin

        self.ackpoint=np.asarray([[0], [self.ackpoint_offset]])

        self.pos_rspindle    =np.zeros((2,3))
        self.pos_rspindle_org=np.zeros((2,1))
    
    def gen_R(self, degree):
        theta=np.radians(degree)
        c, s =np.cos(theta), np.sin(theta)
        R    =np.array(((c, -s), (s, c)))

        return R

    def update(self):

        # Ackerman crossing point
        self.ackpoint=np.asarray([[0], [self.ackpoint_offset]])

        #------------------------------------------
        # Calculate min-max angle
        #------------------------------------------
        
        #------------------------------------------


        #------------------------------------------
        # Right spindle
        #------------------------------------------
        # Anchor point of right spindle
        self.pos_rspindle_org  =np.asarray([[self.track/2-self.stepin], [self.wheel_base]])

        # center position of the wheel
        self.pos_rspindle[:, 0]=[self.stepin, 0]

        # anchor point of right spindle (pre-shift)
        self.pos_rspindle[:, 1]=[0, 0]

        # End of right spindle, link bar connection point
        tmp=np.arctan((self.track/2-self.stepin)/(self.wheel_base-self.ackpoint_offset))
        self.pos_rspindle[:, 2]=[-self.taillen*np.sin(tmp), -self.taillen*np.cos(tmp)]
        if tmp<0:
            self.pos_rspindle[:, 2]*=-1

        # Length of link bar, abs in case exploding
        len_linkbar=np.abs(self.pos_rspindle[0, 2])*2

        # Rotate right spindle
        R=self.gen_R(self.angfrw)
        self.pos_rspindle=np.dot(R, self.pos_rspindle)

        # Move rspindle to its position
        self.pos_rspindle+=self.pos_rspindle_org
        #------------------------------------------

        #------------------------------------------
        # Anchor point of left spindle
        self.pos_lspindle_org  =np.asarray([[-self.track/2+self.stepin], [self.wheel_base]])

        # https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
        x1=self.pos_rspindle[0, 2]
        y1=self.pos_rspindle[1, 2]
        r1=len_linkbar
        x2=self.pos_lspindle_org[0]
        y2=self.pos_lspindle_org[1]
        r2=self.stepin

        # d from left spindle anchor point to right spindle link bar point
        R=np.linalg.norm([x1-x2, y1-y2],  2)

        tmp_a=(r1*r1-r2*r2)/(2*R*R)
        tmp_x=1/2*(x1+x2)+tmp_a*(x2-x1)
        tmp_y=1/2*(y1+y2)+tmp_a*(y2-y1)

        tmp_b=1/2*np.sqrt(2*(r1*r1+r2*r2)/R/R-(r1*r1-r2*r2)*(r1*r1-r2*r2)/R/R/R/R-1)
        # if (y2-y1)>=0:            
        # else:






        


        # tmp=



        return

def init():
    global ackerman
    global p_ackpoint
    global l_rspindle
    
    p_ackpoint.set_data(ackerman.ackpoint)
    l_rspindle.set_data(ackerman.pos_rspindle)

    # The ',' at the end is important!!!! Don't miss
    return p_ackpoint, l_rspindle

def animate(i):
    global ackerman
    global p_ackpoint
    global l_rspindle
    
    ackerman.update()
    
    p_ackpoint.set_data(ackerman.ackpoint)
    l_rspindle.set_data(ackerman.pos_rspindle)

    # The ',' at the end is important!!!! Don't miss
    return p_ackpoint, l_rspindle


if __name__=="__main__":
    global wheel
    global l_frw
    global s_stepin, s_taillen, s_ackpoint, s_angfrw

    track     =151.8    # mm, width
    wheel_base=166.3    # mm, height

    wheel_diameter=60   # mm

    step_in=0

    # x1 x2 ...
    # y1 y2 ...
    rspindle=np.zeros((2, 3))


    plt.rc('font', family='serif')  # font

    # fig=plt.figure(figsize=(10, 8))
    fig=plt.figure(figsize=(10, 10))
    fig.tight_layout()
    # ax =fig.add_subplot(111)
    ax =fig.add_subplot(111, aspect='equal')
    ax.set_xlim([-track, track])
    ax.set_ylim([-wheel_base, wheel_base])

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")

    # Define the 4 margins of the plot
    # ranging between 0~1
    plt.subplots_adjust(left=0.25, right=0.99, top=0.9, bottom=0.16)
    plt.margins(x=0)

    
    axcolor='lightgoldenrodyellow'

    # left, bottom, width, height
    ax_ackpoint_offset=plt.axes([0.15, 0.16, 0.03, 0.74], facecolor=axcolor)
    s_ackpoint_offset =Slider(ax=ax_ackpoint_offset,
                              label='Ackerman\npoint\noffset\n(mm)',
                              valmin=-track, valmax=2*track, valinit=0, valstep=0.1,
                              color=color_used[2],
                              orientation='vertical')

    ax_taillen        =plt.axes([0.1, 0.16, 0.03, 0.74], facecolor=axcolor)
    s_taillen         =Slider(ax=ax_taillen,
                              label='tail\nlength\n(mm)',
                              valmin=-wheel_base, valmax=wheel_base, valinit=0, valstep=0.1,
                              color=color_used[1],
                              orientation='vertical')

    ax_stepin         =plt.axes([0.05, 0.16, 0.03, 0.74], facecolor=axcolor)
    s_stepin          =Slider(ax=ax_stepin,
                              label='stepin\n(mm)',
                              valmin=0, valmax=track/2, valinit=0, valstep=0.1,
                              color=color_used[0],
                              orientation='vertical')

    ax_angfrw         =plt.axes([0.28, 0.05, 0.65, 0.03], facecolor=axcolor)
    s_angfrw          =Slider(ax=ax_angfrw,
                              label='RFW Angle (deg)',
                              valmin=-90, valmax=90, valinit=0, valstep=0.1,
                              color=color_used[3])

    s_ackpoint_offset.on_changed(update)
    s_taillen.on_changed(update)
    s_stepin.on_changed(update)
    s_angfrw.on_changed(update)

    ax_rst=plt.axes([0.03, 0.05, 0.1, 0.03])
    bt_rst=Button(ax_rst, 'Reset', color=axcolor, hovercolor='0.975')
    bt_rst.on_clicked(reset)

    global ackerman
    ackerman=Ackerman(ackpoint_offset=0,
                      taillen        =0,
                      stepin         =0,
                      angfrw         =0)

    global l_rspindle
    l_rspindle, =ax.plot([], [], 'o-', lw=2)

    global p_ackpoint
    p_ackpoint, =ax.plot([], [], '.', ms=15)

    
    t0=time.time()
    animate(0)
    t1=time.time()
    dt=1./30 # 30 fps
    interval=1000 *dt-(t1-t0)

    ani=animation.FuncAnimation(fig,
                                animate,
                                # frames=300,
                                interval=interval,
                                blit=True,
                                init_func=init)
    plt.show()

    sys.exit()

