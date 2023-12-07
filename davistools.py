import os

def bar_string(percent, num_ticks):
    barstr = ''
    num_loaded = int(percent/100.0 * num_ticks) # integer rounding
    num_unloaded = num_ticks - num_loaded
    barstr = '['
    for i in range(num_loaded):
        percent = i/num_loaded
        g = int(percent * 255)
        b = int((1.0-percent) * 128)
        r = int((1.0-percent) * 84)
        colour = '\u001b[38;2;{r};{g}{b}m\u001b[48;2;{r};{g};{b}m'.format(r=r, g=g, b=b)
        barstr += colour + ' '
    barstr += '\u001b[0m' + ' ' * num_unloaded
    barstr += ']'
    return barstr

def progress_statement(iteration, datalen, dt=0.0, bar=True, label=''):
    percent = (iteration+1)/datalen * 100.0
    statement = 'Iteration {}/{} complete ({:.1f}%)'.format(iteration+1, datalen, percent)
    
    begin_section = 30
    mid_section = 50
    end_section = os.get_terminal_size().columns - begin_section - mid_section - 1

    barstr = ''
    if(bar == True):
        barstr = bar_string(percent, end_section-2)

    dtstring = ''
    if(dt != 0.0):
        eta = dt * (datalen-iteration-1)
        dtstring = 'Took {:.1f}s (ETA: {:.1f}s)'.format(dt, eta)

    if(label != ''):
        label += ': '
    print('\r'.format(''),'{:<{begin}}{:^{mid}}{:>}'.format(label + statement, dtstring, barstr, begin=begin_section, mid=mid_section), end='', flush=True)

    if(iteration == datalen-1):
        print('')

def progress_statement_range(cur_val, data, bar=True, label='', dt=0.0):
    percent = (cur_val-data[0])/(data[-1]-data[0]) * 100.0
    statement = 'Process {:.1f}% complete'.format(percent)
    
    begin_section = 30
    mid_section = 40
    end_section = os.get_terminal_size().columns - begin_section - mid_section - 1

    barstr = ''
    if(bar == True):
        barstr = bar_string(percent, end_section-2)

    dtstr = ''
    if(dt != 0.0):
        eta = dt * (100.0-percent)/100.0 * len(data)
        dtstr = 'Took {:.1f}s (ETA: {:.1f}s)'.format(dt, eta)

    if(label != ''):
        label += ': '
    print('\r'.format(''),'{:<{begin}}{:^{mid}}{:>}'.format(label + statement, dtstr, barstr, begin=begin_section, mid=mid_section), end='', flush=True)

    if(cur_val == data[-1]):
        print('') # newline
