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
    def __init__(self, paras):

        self.paras=paras

        self.init_plot()

        return 

    def init_plot(self):

        # DARK MODE!
        # /anaconda3/envs/{env_name}/lib/python3.7/site-packages/matplotlib/mpl-data/stylelib/{dvs_dark.mplstyle}
        # plt.style.use("dark_background")
        # plt.style.use("dvs_dark")

        # Set font
        plt.rc('font', family='serif')  # font

        #############################################
        # Figure 1, UI interactivce stuff
        #############################################
        # Blank figure
        self.fig1=plt.figure(figsize=(8,2))

        # Set slider position
        margin_left  =0.3
        margin_bottom=0.05
        spacing      =0.1

        # Slider width and height
        width      =0.6
        height     =0.1

        # Slider bg color
        axcolor='lightgoldenrodyellow'

        # left, bottom, width, height
        ax_ackpoint_offset=self.fig1.add_axes([margin_left, margin_bottom,           width, height], facecolor=axcolor)
        ax_taillen        =self.fig1.add_axes([margin_left, margin_bottom+1*spacing, width, height], facecolor=axcolor)
        ax_stepin         =self.fig1.add_axes([margin_left, margin_bottom+2*spacing, width, height], facecolor=axcolor)
        ax_angfrw         =self.fig1.add_axes([margin_left, margin_bottom+3*spacing, width, height], facecolor=axcolor)

        self.s_ackpoint_offset=Slider(ax=ax_ackpoint_offset,
                                      label='Ackerman point offset (mm)',
                                      valmin=-self.paras['track'], valmax=2*self.paras['track'], valinit=0, valstep=0.1,
                                      color=color_used[0],
                                      orientation='horizontal')
        
        self.s_taillen        =Slider(ax=ax_taillen,
                                      label='tail length (mm)',
                                      valmin=-self.paras['wheel_base'], valmax=self.paras['wheel_base'], valinit=5, valstep=0.1,
                                      color=color_used[1],
                                      orientation='horizontal')
        
        self.s_stepin         =Slider(ax=ax_stepin,
                                      label='stepin (mm)',
                                      valmin=0, valmax=self.paras['track']/2, valinit=5, valstep=0.1,
                                      color=color_used[0],
                                      orientation='horizontal')
        
        self.s_angfrw         =Slider(ax=ax_angfrw,
                                      label='RFW Angle (deg)',
                                      valmin=-90, valmax=90, valinit=0, valstep=0.1,
                                      color=color_used[3],
                                      orientation='horizontal')


        self.paras['ackpoint_offset']=self.s_ackpoint_offset.val
        self.paras['taillen'        ]=self.s_taillen.val
        self.paras['stepin'         ]=self.s_stepin.val
        self.paras['angfrw'         ]=self.s_angfrw.val

        # s_ackpoint_offset.on_changed(update)
        # s_taillen.on_changed(update)
        # s_stepin.on_changed(update)
        # s_angfrw.on_changed(update)

        # Reset button
        ax_rst=self.fig1.add_axes([0.03, 0.85, 0.1, 0.1])
        bt_rst=Button(ax_rst, 'Reset', color=axcolor, hovercolor='0.975')

        bt_rst.on_clicked(self.reset)
        #############################################


        #############################################
        # Figure 2
        #############################################
        self.fig2, self.axes2=plt.subplots(1, 1, figsize=(8, 6))
        # self.fig.tight_layout()

        # Major ticks every 20, minor ticks every 5
        major_ticks=np.arange(-90, 91, 20)
        minor_ticks=np.arange(-90, 91, 5)

        # Set major and minor ticks
        self.axes2.set_xticks(major_ticks)
        self.axes2.set_xticks(minor_ticks, minor=True)
        self.axes2.set_yticks(major_ticks)
        self.axes2.set_yticks(minor_ticks, minor=True)

        # Set major and minor grid lines
        self.axes2.grid(which='major')
        self.axes2.grid(which='minor', linestyle='--')

        # XY limits
        self.axes2.set_xlim([-50, 90])
        self.axes2.set_ylim([-90, 90])

        # XY lables
        self.axes2.set_xlabel("Front Right Wheel Steering Angle (deg)")
        self.axes2.set_ylabel("Front Left Wheel Steering Angle (deg)")
        
        # Title
        self.axes2.set_title("Ackerman")

        # Horizontal line
        self.f1_l1=self.axes2.axhline(0, color='r')
        # Vertical line
        self.f1_l2=self.axes2.axvline(0, color='r')
        # Infinite black line going through point a and b
        self.f1_l3=self.axes2.axline((0, 0), (1, 1), color='gray', label='Simple')

        # Ideal
        self.ang_ideal=self.cal_ideal_ackerman()
        self.f1_l4,   =self.axes2.plot(self.ang_ideal[0, :], self.ang_ideal[1, :], color='k', label='Ideal')

        # Real
        # self.ang_real =self.cal_real_ackerman()
        # self.f1_l5,   =self.axes2.plot(self.ang_real[ 0, :], self.ang_real[ 1, :], color='b', label='Real')

        self.axes2.legend(handles=[self.f1_l3, self.f1_l4])
        #############################################

        # self.fig2.canvas.mpl_connect("resize_event", self.TextResizer(lst_text))

       

        plt.show()

        return

    def reset(self, event):
        self.s_stepin.reset()
        self.s_taillen.reset()
        self.s_ackpoint_offset.reset()
        self.s_angfrw.reset()

        self.paras['ackpoint_offset']=self.s_ackpoint_offset.val
        self.paras['taillen'        ]=self.s_taillen.val
        self.paras['stepin'         ]=self.s_stepin.val
        self.paras['angfrw'         ]=self.s_angfrw.val

        # ackerman.ackpoint_offset=s_ackpoint_offset.val
        # ackerman.stepin         =s_stepin.val
        # ackerman.taillen        =s_taillen.val
        # ackerman.angfrw         =s_angfrw.val

        return

    def cal_ideal_ackerman(self):

        ang_right_list=np.arange(0, 91)

        # Ideal, turn right
        ideal_ang_right_list=[]
        ideal_ang_left_list =[]
        for ang_right in ang_right_list:
            
            if ang_right>0:
                d=self.paras['wheel_base']/np.tan(ang_right/180*pi)
                ang_left=np.arctan(self.paras['wheel_base']/(self.paras['track']+d))
                ang_left=ang_left/pi*180

            if ang_right<0:
                d=self.paras['wheel_base']/np.tan(-ang_right/180*pi)
                ang_left=np.arctan(self.paras['wheel_base']/(d-self.paras['track']))
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

    def cal_real_ackerman(self):

        ang_right_list=np.arange(0, 91)

        # Ideal, turn right
        real_ang_right_list=[]
        real_ang_left_list =[]
        for ang_right in ang_right_list:
            dum=1






        ang_real=np.asarray([real_ang_right_list, real_ang_left_list], dtype=np.float32)
        ang_real=ang_real[:, ang_real[0, :].argsort()]

        return ang_real




if __name__=="__main__":
    
    track     =151.8    # mm, width
    wheel_base=166.3    # mm, height

    wheel_diameter=60   # mm

    paras={'track':          track,
           'wheel_base':     wheel_base,
           'wheel_diameter': wheel_diameter}

    ackerman=Ackerman(paras)

    sys.exit()
