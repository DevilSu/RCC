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

class Ackerman:
    def __init__(self,
                 track          =100,
                 wheel_base     =100,
                 ackpoint_offset=0,
                 taillen        =5,
                 stepin         =5,
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

        # 2 x 181
        self.ideal =self.gen_ideal()
        self.simple=np.asarray([self.ideal[0, :], self.ideal[0, :]])

        self.prev_ackpoint_offset=0
        self.prev_taillen        =0
        self.prev_stepin         =0

        self.ack_curve=self.update_curve()
        print(self.ack_curve)

        # Ployfit the curve
        aS  =np.polyfit(self.ack_curve[0, :], self.ack_curve[1, :], 8)
        self.ack_poly=np.poly1d(aS)

        # Create a loop so will plot a box
        self.four_wheels=np.asarray([[track/2, track/2, -track/2, -track/2, track/2],
                                     [0, wheel_base, wheel_base, 0, 0]])

        self.pos_rspindle_rotated=np.zeros((2, 3))
        self.pos_lspindle_rotated=np.zeros((2, 3))
        self.pos_linkbar         =np.zeros((2, 2))

    def gen_ideal(self):
        ang_right_list=np.arange(0, 91)

        # Ideal, turn right
        ideal_ang_right_list=[]
        ideal_ang_left_list =[]
        for ang_right in ang_right_list:
            
            if ang_right>0:
                d=self.wheel_base/np.tan(ang_right/180*pi)
                ang_left=np.arctan(self.wheel_base/(self.track+d))
                ang_left=ang_left/pi*180

            if ang_right<0:
                d=self.wheel_base/np.tan(-ang_right/180*pi)
                ang_left=np.arctan(self.wheel_base/(d-self.track))
                ang_left=-ang_left/pi*180
            
            if ang_right==0:
                ang_left=0
                ideal_ang_right_list.append(ang_right)
                ideal_ang_left_list.append( ang_left)
            else:
                # Ideal, turn right
                ideal_ang_right_list.append(ang_right)
                ideal_ang_left_list.append( ang_left)

                # Ideal, turn left
                ideal_ang_right_list.append(-ang_left)
                ideal_ang_left_list.append( -ang_right)

        ang_ideal=np.asarray([ideal_ang_right_list, ideal_ang_left_list], dtype=np.float32)
        ang_ideal=ang_ideal[:, ang_ideal[0, :].argsort()]

        return ang_ideal

    def gen_R(self, degree):
        theta=np.radians(degree)
        c, s =np.cos(theta), np.sin(theta)
        R    =np.array(((c, -s), (s, c)))

        return R

    def update(self):

        flag_changed=(self.prev_ackpoint_offset!=self.ackpoint_offset) | \
                     (self.prev_taillen        !=self.taillen)         | \
                     (self.prev_stepin         !=self.stepin)

        if flag_changed:
            self.prev_ackpoint_offset=self.ackpoint_offset
            self.prev_taillen =self.taillen
            self.prev_stepin  =self.stepin

            self.ack_curve=self.update_curve()
            print(self.ack_curve)

            # Ployfit the curve
            aS  =np.polyfit(self.ack_curve[0, :], self.ack_curve[1, :], 6)
            self.ack_poly=np.poly1d(aS)

        # Update points!
        R=self.gen_R(self.angfrw)
        self.pos_rspindle_rotated=np.dot(R, self.pos_rspindle)+self.pos_rspindle_org

        self.angflw=self.ack_poly(self.angfrw)
        R=self.gen_R(self.angflw)
        self.pos_lspindle_rotated=np.dot(R, self.pos_lspindle)+self.pos_lspindle_org

        self.pos_linkbar[:, 0]=self.pos_rspindle_rotated[:, 2]
        self.pos_linkbar[:, 1]=self.pos_lspindle_rotated[:, 2]
        return

    def update_curve(self):

        # Ackerman crossing point
        ackpoint=np.asarray([[0], [self.ackpoint_offset]])

        #------------------------------------------
        # Right spindle
        #------------------------------------------
        self.pos_rspindle=np.zeros((2, 3))

        # Anchor point of right spindle
        self.pos_rspindle_org=np.asarray([[self.track/2-self.stepin], [self.wheel_base]])

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
        len_linkbar=self.track+2*self.pos_rspindle[0, 2]-2*self.stepin

        r1=len_linkbar
        #------------------------------------------


        #------------------------------------------
        # Left spindle
        #------------------------------------------
        pos_lspindle=np.zeros((2, 3))

        # Anchor point of left spindle
        self.pos_lspindle_org=np.asarray([[-self.track/2+self.stepin], [self.wheel_base]])

        # Flip x of rspindle to get lspindle :)
        self.pos_lspindle=self.pos_rspindle.copy()
        self.pos_lspindle[0, :]*=-1

        vec1     =self.pos_lspindle[:, 2]
        unit_vec1=vec1/np.linalg.norm(vec1)

        # Move lspindle to its position
        pos_lspindle_moved=self.pos_lspindle+self.pos_lspindle_org

        r2=self.taillen
        #------------------------------------------


        lst_ang_right=[0]
        lst_ang_left =[0]
        # for ang_right in range(1, 91):
        for ang_right in np.arange(-1, -91, -1):
            # Rotate right spindle
            Rot=self.gen_R(ang_right)
            pos_rspindle_rotated=np.dot(Rot, self.pos_rspindle)
            # Move rspindle to its position
            pos_rspindle_rotated+=self.pos_rspindle_org

            # Get two center points
            x1=pos_rspindle_rotated[0, 2]
            y1=pos_rspindle_rotated[1, 2]
        
            x2=pos_lspindle_moved[  0, 1]
            y2=pos_lspindle_moved[  1, 1]

            # d from left spindle anchor point to right spindle link bar point
            R=np.linalg.norm([x1-x2, y1-y2],  2)

            # Check if R is larger than r1+r2
            if R>(r1+r2):
                # print(R)
                # print(r1+r2)
                break

            # # https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
            # # Calculate intersection points of two circles
            # tmp_a=(r1*r1-r2*r2)/(2*R*R)
            # tmp_x=1/2*(x1+x2)+tmp_a*(x2-x1)
            # tmp_y=1/2*(y1+y2)+tmp_a*(y2-y1)

            # tmp_b=1/2*np.sqrt(2*(r1*r1+r2*r2)/R/R-(r1*r1-r2*r2)*(r1*r1-r2*r2)/R/R/R/R-1)
            
            # # Get the point with lower y
            # sign=1
            # if (x1-x2)>0:
            #     sign=-1

            # x_ans=tmp_x+sign*tmp_b*(y2-y1)
            # y_ans=tmp_y+sign*tmp_b*(x1-x2)

            # ------------------------
            # Take 2
            l=(r1*r1-r2*r2+R*R)/(2*R)

            # print("l:", l)

            h=np.sqrt(r1*r1-l*l)

            # Get the point with lower y
            sign=1
            if (x2-x1)<0:
                sign=-1

            x_ans=l/R*(x2-x1)+sign*h/R*(y2-y1)+x1
            y_ans=l/R*(y2-y1)-sign*h/R*(x2-x1)+y1

            # dx=x_ans-x1
            # dy=y_ans-y1
            # print("LOL:", ang_right, dx*dx+dy*dy, r1*r1)
            # ------------------------

            # Recover angle of left spindle
            vec2     =np.asarray([[x_ans-x2],[y_ans-y2]])
            unit_vec2=vec2/np.linalg.norm(vec2)
            ang_left=np.arccos(np.dot(unit_vec1, unit_vec2))*180/pi
            ang_left=ang_left[0]
            print(ang_left)


            # tmp=self.gen_R(ang_left)
            # print(tmp.shape)
            # tmp=np.dot(tmp, self.pos_lspindle)+self.pos_lspindle_org
            # print("err:", tmp[0, 2]-x_ans, tmp[1, 2]-y_ans)

            # Check if angle of left spindle is increasing
            # break

            # Turn right
            lst_ang_right.append(ang_right)
            lst_ang_left.append( ang_left)

            # Turn left
            lst_ang_right.append(-ang_left)
            lst_ang_left.append( -ang_right)

        ang_ack=np.asarray([lst_ang_right, lst_ang_left], dtype=np.float32)
        ang_ack=ang_ack[:, ang_ack[0, :].argsort()]

        return ang_ack

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

def init():
    global ackerman
    global p_dot_on_ack
    global l_ack
    global l_rspindle, l_lspindle, l_linkbar
    
    
    p_dot_on_ack.set_data(ackerman.angfrw, ackerman.ack_poly(ackerman.angfrw))
    
    l_ack.set_data(ackerman.ack_curve[ 0, :], ackerman.ack_curve[ 1, :])

    l_rspindle.set_data(ackerman.pos_rspindle_rotated[0, :], ackerman.pos_rspindle_rotated[1, :])
    l_lspindle.set_data(ackerman.pos_lspindle_rotated[0, :], ackerman.pos_lspindle_rotated[1, :])
    l_linkbar.set_data( ackerman.pos_linkbar[0, :],          ackerman.pos_linkbar[1, :])

    # The ',' at the end is important!!!! Don't miss
    return p_dot_on_ack, l_ack, l_rspindle, l_lspindle, l_linkbar

def animate(i):
    global ackerman
    global p_dot_on_ack
    global l_ack
    global s_angfrw

    global l_rspindle, l_lspindle, l_linkbar
    
    ackerman.update()

    # Adjust frw angle slider
    s_angfrw.valmin=float(np.min(ackerman.ack_curve[ 0, :]))
    s_angfrw.valmax=float(np.max(ackerman.ack_curve[ 0, :]))
    if s_angfrw.val>s_angfrw.valmax:
        s_angfrw.set_val(s_angfrw.valmax)
    elif s_angfrw.val<s_angfrw.valmin:
        s_angfrw.set_val(s_angfrw.valmin)
    ackerman.angfrw=s_angfrw.val

    p_dot_on_ack.set_data(ackerman.angfrw, ackerman.ack_poly(ackerman.angfrw))

    l_ack.set_data(ackerman.ack_curve[ 0, :], ackerman.ack_curve[ 1, :])

    l_rspindle.set_data(ackerman.pos_rspindle_rotated[0, :], ackerman.pos_rspindle_rotated[1, :])
    l_lspindle.set_data(ackerman.pos_lspindle_rotated[0, :], ackerman.pos_lspindle_rotated[1, :])
    l_linkbar.set_data( ackerman.pos_linkbar[0, :],          ackerman.pos_linkbar[1, :])

    dx=ackerman.pos_linkbar[0, 0]-ackerman.pos_linkbar[0, 1]
    dy=ackerman.pos_linkbar[1, 0]-ackerman.pos_linkbar[1, 1]
    print("lb len:", dx*dx+dy*dy)


    # The ',' at the end is important!!!! Don't miss
    return p_dot_on_ack, l_ack, l_rspindle, l_lspindle, l_linkbar

if __name__=="__main__":
    global wheel
    global l_frw
    global s_stepin, s_taillen, s_ackpoint, s_angfrw

    track     =151.8    # mm, width
    wheel_base=166.3    # mm, height

    wheel_diameter=60   # mm

    #############################################
    # Plot settings
    #############################################
    plt.rc('font', family='serif')  # font

    # fig=plt.figure(figsize=(10, 10))
    # fig.tight_layout()
    # ax =fig.add_subplot(111, aspect='equal')

    fig, axs=plt.subplots(1, 2, figsize=(20, 10))
    fig.tight_layout()
    plt.subplots_adjust(left=0.13, bottom=0.16)

    ax=axs[0]

    # Major ticks every 20, minor ticks every 5
    major_ticks=np.arange(-90, 91, 20)
    minor_ticks=np.arange(-90, 91, 5)

    axs[0].set_xticks(major_ticks)
    axs[0].set_xticks(minor_ticks, minor=True)
    axs[0].set_yticks(major_ticks)
    axs[0].set_yticks(minor_ticks, minor=True)

    axs[0].set_xlim([-50, 90])
    axs[0].set_ylim([-90, 90])

    # And a corresponding grid
    axs[0].grid(which='both')

    axs[0].set_xlabel("Front Right Wheel Steering Angle (deg)")
    axs[0].set_ylabel("Front Left Wheel Steering Angle (deg)")

    # Define the 4 margins of the plot
    # ranging between 0~1
    # plt.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.16)
    plt.margins(x=0)

    # Plot on right
    # Major ticks every 20, minor ticks every 5
    major_ticks=np.arange(-1000, 1000, 100)
    minor_ticks=np.arange(-1000, 1000, 20)

    axs[1].set_xticks(major_ticks)
    axs[1].set_xticks(minor_ticks, minor=True)
    axs[1].set_yticks(major_ticks)
    axs[1].set_yticks(minor_ticks, minor=True)

    axs[1].set_xlim([-1.5*track,  1.5*track])
    axs[1].set_ylim([-wheel_base, 2*wheel_base])

    # And a corresponding grid
    axs[1].grid(which='both')

    axs[1].set_xlabel("x (mm)")
    axs[1].set_ylabel("y (mm)")

    #############################################
    

    #############################################
    # UI interactivce stuff
    #############################################
    axcolor='lightgoldenrodyellow'
    # left, bottom, width, height
    ax_ackpoint_offset=plt.axes([0.075, 0.16, 0.015, 0.74], facecolor=axcolor)
    s_ackpoint_offset =Slider(ax=ax_ackpoint_offset,
                              label='Ackerman\npoint\noffset\n(mm)',
                              valmin=-track, valmax=2*track, valinit=0, valstep=0.1,
                              color=color_used[2],
                              orientation='vertical')

    ax_taillen        =plt.axes([0.05, 0.16, 0.015, 0.74], facecolor=axcolor)
    s_taillen         =Slider(ax=ax_taillen,
                              label='tail\nlength\n(mm)',
                              valmin=-wheel_base, valmax=wheel_base, valinit=5, valstep=0.1,
                              color=color_used[1],
                              orientation='vertical')

    ax_stepin         =plt.axes([0.025, 0.16, 0.015, 0.74], facecolor=axcolor)
    s_stepin          =Slider(ax=ax_stepin,
                              label='stepin\n(mm)',
                              valmin=0, valmax=track/2, valinit=5, valstep=0.1,
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
    #############################################


    #############################################
    # Ackerman class
    #############################################
    global ackerman
    ackerman=Ackerman(
                      track          =track,
                      wheel_base     =wheel_base,
                      ackpoint_offset=0,
                      taillen        =5,
                      stepin         =5,
                      angfrw         =0)
    #############################################


    #############################################
    # Lines on the plot (that won't change)
    #############################################
    l_simple=ax.plot(ackerman.simple[0, :], ackerman.simple[1, :], '-', color=color_used[6], lw=2, label='Simple')
    l_ideal =ax.plot(ackerman.ideal[ 0, :], ackerman.ideal[ 1, :], '-', color=color_used[5], lw=2, label='Ideal')
    
    ax.hlines(y=0, xmin=-90, xmax=90, linewidth=2, color='r')

    axs[1].plot(ackerman.four_wheels[0, :], ackerman.four_wheels[1, :], '-.')
    #############################################


    #############################################
    # Lines on the plot (that will change)
    #############################################
    global l_ack
    l_ack, =ax.plot([], [], 'o-', lw=2, color=color_used[8], label='Ackerman')

    global p_dot_on_ack
    p_dot_on_ack, =ax.plot([], [], '.', ms=15, color=color_used[3])


    global l_rspindle
    l_rspindle, =axs[1].plot([], [], 'o-', lw=2, ms=4, color=color_used[0])

    global l_lspindle
    l_lspindle, =axs[1].plot([], [], 'o-', lw=2, ms=4, color=color_used[1])

    global l_linkbar
    l_linkbar,  =axs[1].plot([], [], 'o-', lw=2, ms=4, color=color_used[2])

    #############################################


    #############################################
    # Setup animation
    #############################################
    t0=time.time()
    animate(0)
    t1=time.time()
    dt=1./30 # 30 fps
    interval=1000 *dt-(t1-t0)

    # ani=animation.FuncAnimation(fig,
    #                             animate,
    #                             # frames=300,
    #                             interval=interval,
    #                             blit=True,
    #                             init_func=init)

    ax.legend(loc='lower right')

    plt.show()
    #############################################

    sys.exit()

