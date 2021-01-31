from dearpygui.core import *
from dearpygui.simple import *
import time, math, random
from selenium import webdriver
from _thread import *
from Bot import Bot

bot = Bot()
start_new_thread(bot.main_loop, ())

def update_pie_chart_1():

    # you'll need to delete series
    delete_series("PieChart1", "data")

    # get your stored data
    enemies = list(get_data("enemies"))

    for x in range(0, len(enemies)):
        if x == 0:
            enemies[x] = bot.normal_enemies_killed
        elif x == 1:
            enemies[x] = bot.agile_enemies_killed
        elif x == 2:
            enemies[x] = bot.tough_enemies_killed
        elif x == 3:
            enemies[x] = bot.angry_enemies_killed
        elif x == 4:
            enemies[x] = bot.mad_enemies_killed
        elif x == 5:
            enemies[x] = bot.shielded_enemies_killed

    # only need to red store data if we changed it
    add_data("enemies", enemies)

    # replot the graph
    add_pie_series("PieChart1", "data", enemies,
                   ["Normal Enemies", "Agile Enemies", "Tough Enemies", "Angry Enemies", 'Mad Enemies', "Shielded Enemies"]
                   , 0.5, 0.5, 0.5, normalize=True, format="%.0f")

    set_color_map("PieChart1", mvPlotColormap_Dark)


def update_pie_chart_2():
    # you'll need to delete series
    delete_series("PieChart2", "data")

    # get your stored data
    shots = list(get_data("shots"))

    for x in range(0, len(shots)):
        if x == 0:
            shots[x] = bot.primary_shot
        elif x == 1:
            shots[x] = bot.special_shot
        elif x == 2:
            shots[x] = bot.destructive_shot

    # only need to red store data if we changed it
    add_data("shots", shots)

    # replot the graph
    add_pie_series("PieChart2", "data", shots,
                   ["Primary Shots", "Special Shots", "Destructive Shots"]
                   , 0.5, 0.5, 0.5, normalize=True, format="%.0f")

    set_color_map("PieChart2", mvPlotColormap_Dark)

def on_render():
    add_value('enemies_killed', 0)
    set_value('enemies_killed', bot.enemies_killed)

    add_value('shot_count', 0)
    set_value('shot_count', bot.shot_count)

    add_value('agile_enemies_killed', 0)
    set_value('agile_enemies_killed', bot.agile_enemies_killed)

    add_value('tough_enemies_killed', 0)
    set_value('tough_enemies_killed', bot.tough_enemies_killed)

    add_value('angry_enemies_killed', 0)
    set_value('angry_enemies_killed', bot.angry_enemies_killed)

    add_value('shielded_enemies_killed', 0)
    set_value('shielded_enemies_killed', bot.shielded_enemies_killed)

    add_value('normal_enemies_killed', 0)
    set_value('normal_enemies_killed', bot.normal_enemies_killed)

    add_value('primary_shot_count', 0)
    set_value('primary_shot_count', bot.primary_shot)

    add_value('special_shot_count', 0)
    set_value('special_shot_count', bot.special_shot)

    add_value('destructive_shot_count', 0)
    set_value('destructive_shot_count', bot.destructive_shot)

    add_value('special_ammo_count', 0)
    set_value('special_ammo_count', 0) #bot.special_amnmo

    update_pie_chart_1()
    update_pie_chart_2()


def idle_mode_callback(sender, data):
    bot.idle = get_value(sender)

def safe_mode_callback(sender, data):
    bot.safe_mode = get_value(sender)


with window(width=250, height= 150, x_pos=10, y_pos=10, name='Player Stats', no_resize=True, no_move=True):

    set_theme('Gold')

    add_text('Total Shot Count: ')
    add_same_line(spacing = 1)
    add_text(name = 'shot_count_value', source='shot_count', default_value= '0')

    add_text('Primary Shot Count: ')
    add_same_line(spacing=1)
    add_text(name='primary_shot_count_value', source='primary_shot_count', default_value='0')

    add_text('Special Shot Count: ')
    add_same_line(spacing=1)
    add_text(name='special_shot_count_value', source='special_shot_count', default_value='0')

    add_text('Destructive Shot Count: ')
    add_same_line(spacing=1)
    add_text(name='destructive_shot_count_value', source='destructive_shot_count', default_value='0')
    set_render_callback(on_render)

with window(width=250, height= 150, x_pos=270, y_pos=10, name='Enemy Stats', no_resize=True, no_move=True):
    add_text('Total Enemies Killed: ')
    add_same_line(spacing=1)
    add_text(name = 'enemies_killed_value', source='enemies_killed', default_value='0')

    add_text('Normal Enemies Killed: ')
    add_same_line(spacing=1)
    add_text(name='normal_enemies_killed_value', source='normal_enemies_killed', default_value='0')

    add_text('Agile Enemies Killed: ')
    add_same_line(spacing=1)
    add_text(name='agile_enemies_killed_value', source='agile_enemies_killed', default_value='0')

    add_text('Tough Enemies Killed: ')
    add_same_line(spacing=1)
    add_text(name='tough_enemies_killed_value', source='tough_enemies_killed', default_value='0')

    add_text('Angry Enemies Killed: ')
    add_same_line(spacing=1)
    add_text(name='angry_enemies_killed_value', source='angry_enemies_killed', default_value='0')

    add_text('Shielded Enemies Killed: ')
    add_same_line(spacing=1)
    add_text(name='shielded_enemies_killed_value', source='shielded_enemies_killed', default_value='0')


with window(width=250, height= 150, x_pos=(270 * 2) - 10, y_pos=10, name='Session Options', no_resize=True, no_move=True):

    add_checkbox('Idle Mode', callback = idle_mode_callback)
    add_checkbox('Safe Mode', callback = safe_mode_callback)


with window("Enemies Killed", width=500, height=500):
    add_plot("PieChart1",
             no_mouse_pos=True, xaxis_no_gridlines=True, xaxis_no_tick_marks=True, xaxis_no_tick_labels=True,
             yaxis_no_gridlines=True, yaxis_no_tick_marks=True, yaxis_no_tick_labels=True, width=400, height=400)
    set_plot_xlimits("PieChart1", 0, 1)
    set_plot_ylimits("PieChart1", 0, 1)

    # store your data
    add_data("enemies", [0,0,0,0,0,0])

with window("Shots Fired", width=500, height=500):
    add_plot("PieChart2",
             no_mouse_pos=True, xaxis_no_gridlines=True, xaxis_no_tick_marks=True, xaxis_no_tick_labels=True,
             yaxis_no_gridlines=True, yaxis_no_tick_marks=True, yaxis_no_tick_labels=True, width=400, height=400)
    set_plot_xlimits("PieChart2", 0, 1)
    set_plot_ylimits("PieChart2", 0, 1)

    # store your data
    add_data("shots", [0,0,0])



start_dearpygui()
