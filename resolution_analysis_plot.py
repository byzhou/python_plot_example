import sys, os, re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def resolution_analysis_plot(resolution):

    noise_magnitude = [0.00000001, 0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000, 10000000, 100000000]

    data_base       = []
    for root, dirs, files in os.walk('resolution_analysis'):
        for filename in files:
            file_full_path  = os.path.join(root, filename)
            single_item     = filter(None, re.split('/|\ |monte_carlo_|\.|txt|_|diff|test|noise|resolution|analysis',file_full_path))
            error_rate_data = []
            read_file       = open(file_full_path)
            for lines in read_file:
                if "not_white_rate" in lines:
                    if "matrix_diff" in file_full_path:
                        results     = 1 - float(lines.split(' ')[1])
                    else:
                        results     = float(lines.split(' ')[1])
                    error_rate_data.append(results)
            read_file.close()
            single_item.append(error_rate_data)
            data_base.append(single_item)
            #print single_item

    # change global font 
    font = {\
            'family' : 'serif',\
            'size'   : 30}
    plt.rc('font', **font)

    line_set        = []
    line_name_set   = []
    fig1, ax = plt.subplots(figsize=(16,8))
    for single_item in data_base:
        if single_item[0] == resolution:
            line,=ax.semilogx(noise_magnitude, single_item[4])
            line_set.append(line)
            if single_item[2] == 'c1355':   line_color = 'r'
            if single_item[2] == 'c1908':   line_color = 'b'
            if single_item[2] == 'c2670':   line_color = 'c'
            if single_item[2] == 'c499':    line_color = 'k'
            if single_item[2] == 'c880a':   line_color = 'm'
            if single_item[1] == '10':      line_linestyle = '-.'
            if single_item[1] == '20':      line_linestyle = '-'
            if single_item[1] == '30':      line_linestyle = ':'
            if single_item[3] == 'matrix':  
                line_marker = 'o'
                false_kind  = 'neg'
            if single_item[3] == 'white':   
                line_marker = '^'
                false_kind  = 'pos'
            plt.setp(line, linewidth=9, color=line_color, markersize=20, marker=line_marker, linestyle=line_linestyle)
            line_name_set.append(single_item[2]+'-'+false_kind+'-'+single_item[1])
                       
                            
    ax.legend(line_set, line_name_set,\
        framealpha=0,\
        fontsize=18,\
        ncol=2,\
        borderaxespad=0.4,\
        loc='best'
        )
    ax.set_xscale("log", nonposx='clip')
    plt.grid()
    #plt.show()

    savefig_name = PdfPages(resolution+'_resolution_analysis_error_rate'+'.pdf')
    plt.savefig(savefig_name, format='pdf', bbox_inches='tight')
    savefig_name.close()
    plt.close()

resolution_analysis_plot('0p1')
resolution_analysis_plot('0p2')
resolution_analysis_plot('0p4')
