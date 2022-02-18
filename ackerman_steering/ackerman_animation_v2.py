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
        # Create figure and axes
        self.fig1, self.axes1=plt.subplots(1, 1, figsize=(8, 6))
        # self.fig.tight_layout()

        # Major ticks every 20, minor ticks every 5
        major_ticks=np.arange(-90, 91, 20)
        minor_ticks=np.arange(-90, 91, 5)

        # Set major and minor ticks
        self.axes1.set_xticks(major_ticks)
        self.axes1.set_xticks(minor_ticks, minor=True)
        self.axes1.set_yticks(major_ticks)
        self.axes1.set_yticks(minor_ticks, minor=True)

        # Set major and minor grid lines
        self.axes1.grid(which='major')
        self.axes1.grid(which='minor', linestyle='--')

        # XY limits
        self.axes1.set_xlim([-50, 90])
        self.axes1.set_ylim([-90, 90])

        # XY lables
        self.axes1.set_xlabel("Front Right Wheel Steering Angle (deg)")
        self.axes1.set_ylabel("Front Left Wheel Steering Angle (deg)")
        # Title
        self.axes1.set_title("Ackerman")

        # Horizontal line
        self.f1_l1=self.axes1.axhline(0, color='r', )
        # Vertical line
        self.f1_l2=self.axes1.axvline(0, color='r')
        # Infinite black line going through point a and b.
        self.f1_l3=self.axes1.axline((0, 0), (1, 1), color='k', label='Simple')

        self.axes1.legend(handles=[self.f1_l3])


        #############################################
        # UI interactivce stuff
        #############################################
        # Blank figure
        self.fig2=plt.figure(figsize=(8,2))

        # Set slider position
        margin_left  =0.4
        margin_bottom=0.05
        spacing      =0.1

        # Slider width and height
        width      =0.5
        height     =0.1

        # Slider bg color
        axcolor='lightgoldenrodyellow'

        # left, bottom, width, height
        ax_ackpoint_offset=self.fig2.add_axes([margin_left, margin_bottom,           width, height], facecolor=axcolor)
        ax_taillen        =self.fig2.add_axes([margin_left, margin_bottom+1*spacing, width, height], facecolor=axcolor)
        ax_stepin         =self.fig2.add_axes([margin_left, margin_bottom+2*spacing, width, height], facecolor=axcolor)
        ax_angfrw         =self.fig2.add_axes([margin_left, margin_bottom+3*spacing, width, height], facecolor=axcolor)

        s_ackpoint_offset =Slider(ax=ax_ackpoint_offset,
                                  label='Ackerman point offset (mm)',
                                  valmin=-self.paras['track'], valmax=2*self.paras['track'], valinit=0, valstep=0.1,
                                  color=color_used[0],
                                  orientation='horizontal')

        
        s_taillen         =Slider(ax=ax_taillen,
                                  label='tail length (mm)',
                                  valmin=-self.paras['wheel_base'], valmax=self.paras['wheel_base'], valinit=5, valstep=0.1,
                                  color=color_used[1],
                                  orientation='horizontal')

        
        s_stepin          =Slider(ax=ax_stepin,
                                  label='stepin (mm)',
                                  valmin=0, valmax=self.paras['track']/2, valinit=5, valstep=0.1,
                                  color=color_used[0],
                                  orientation='horizontal')

        
        s_angfrw          =Slider(ax=ax_angfrw,
                                  label='RFW Angle (deg)',
                                  valmin=-90, valmax=90, valinit=0, valstep=0.1,
                                  color=color_used[3],
                                  orientation='horizontal')

        # s_ackpoint_offset.on_changed(update)
        # s_taillen.on_changed(update)
        # s_stepin.on_changed(update)
        # s_angfrw.on_changed(update)

        ax_rst=self.fig2.add_axes([0.03, 0.05, 0.1, 0.03])
        bt_rst=Button(ax_rst, 'Reset', color=axcolor, hovercolor='0.975')
        # bt_rst.on_clicked(reset)
        #############################################



        plt.show()

        return


if __name__=="__main__":
    
    track     =151.8    # mm, width
    wheel_base=166.3    # mm, height

    wheel_diameter=60   # mm

    paras={'track':          track,
           'wheel_base':     wheel_base,
           'wheel_diameter': wheel_diameter}

    ackerman=Ackerman(paras)

    sys.exit()
