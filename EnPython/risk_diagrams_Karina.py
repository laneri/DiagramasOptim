import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas import ExcelWriter

import plotly.graph_objects as go


def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* kwarg.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, alpha=0.45, interpolation='bicubic',
                   vmin=0, vmax=1, **kwargs)
    return im


def main():
    try:
        filename="Data_Argentina.xlsx"
        #filename = sys.argv[1]
        print(filename)
    except:
        print('Error! Usage: python3 risk_diagrams.py filename')
        sys.exit()
           
    data = pd.read_excel(filename, sheet_name='Cases')
    population = pd.read_excel(filename, sheet_name='Population')
    dia = pd.to_datetime(data['Dia']).dt.strftime('%d/%m/%Y')
    dia = dia.to_numpy()
    region = population.columns

    for ID in range(len(region)):

            cumulative_cases = data[region[ID]]  # region for ALL
            cumulative_cases = cumulative_cases.to_numpy()
            new_cases = np.zeros((len(cumulative_cases)), dtype=np.int)
            for i in range(len(cumulative_cases)):
                if i != 0: new_cases[i] = cumulative_cases[i] - cumulative_cases[i - 1]

            p = np.zeros((len(new_cases)), dtype=np.float)
            for i in range(7, len(new_cases)):
                div = 0
                aux = new_cases[i - 5] + new_cases[i - 6] + new_cases[i - 7]
                if aux == 0:
                    div = 1
                else:
                    div = aux
                p[i] = min((new_cases[i] + new_cases[i - 1] + new_cases[i - 2]) / div, 4)

            p_seven = np.zeros((len(new_cases)), dtype=np.float)
            n_14_days = np.zeros((len(new_cases)), dtype=np.float)
            a_14_days = np.zeros((len(new_cases)), dtype=np.float)
            risk = np.zeros((len(new_cases)), dtype=np.float)
            risk_per_10 = np.zeros((len(new_cases)), dtype=np.float)
            for i in range(13, len(new_cases)):
                p_seven[i] = np.average(p[i - 6:i + 1])
                n_14_days[i] = np.sum(new_cases[i - 13: i + 1])
                pop = population[region[ID]]  # 204449000
                # pop *= 1000
                a_14_days[i] = n_14_days[i] / pop * 100000
                risk[i] = n_14_days[i] * p_seven[i]
                risk_per_10[i] = a_14_days[i] * p_seven[i]
                #print(dia[i], cumulative_cases[i], new_cases[i], p[i], p_seven[i], n_14_days[i], a_14_days[i], risk[i], risk_per_10[i])
                print(dia[i], p_seven[i], a_14_days[i], risk[i], risk_per_10[i])
            first_day = dia[13]
            last_day = dia[len(dia) - 1]
            first_day = first_day.replace('/', '-')
            last_day = last_day.replace('/', '-')
            save_path = 'reports_pdf/risk/' + last_day + '-' + region[ID] + '.pdf'

            
            with PdfPages(save_path) as pdf:
                fig1, ax1 = plt.subplots()
                ax1.plot(a_14_days, p_seven, 'ko--', fillstyle='none', linewidth=0.5)
                lim = ax1.get_xlim()
                x = np.ones(int(lim[1]))
                ax1.plot(x, 'k-', fillstyle='none', linewidth=0.5)
                ax1.set_ylim(0, 4)
                ax1.set_xlim(0, max(a_14_days+2))#Karina 
                ax1.set_ylabel('$\u03C1$ (mean of the last 7 days)')
                ax1.set_xlabel('Attack rate per $10^5$ inh. (last 14 days)')
                #ax1.set_xlabel('Attack rate per $10000$ inh. (last 14 days)')
                ax1.annotate(first_day,
                             xy=(a_14_days[13], p_seven[13]), xycoords='data',
                             xytext=(len(x) - abs(len(x) / 1.13), 1.2), textcoords='data',
                             arrowprops=dict(arrowstyle="->",
                                             connectionstyle="arc3", linewidth=0.4),
                             )
                ax1.annotate(last_day,
                             xy=(a_14_days[len(a_14_days) - 1], p_seven[len(p_seven) - 1]), xycoords='data',
                             xytext=(len(x) - abs(len(x) /4), 3.5), textcoords='data',
                             arrowprops=dict(arrowstyle="->",
                                             connectionstyle="arc3", linewidth=0.4),
                             )

                plt.title(region[ID])
                color_map = plt.cm.hsv
                cmap = color_map.reversed()
                for i in a_14_days:
                    if i < 30:
                        c_min = 0.6
                        c_max = 0.89
                    elif 30 > i < 100:
                        c_min = 0.65
                        c_max = 0.95
                    elif 100 > i < 200:
                        c_min = 0.65
                        c_max = 1.1
                    else:
                        c_min = 0.65
                        c_max = 1.3

                gradient_image(ax1, direction=0.6, extent=(0, 1, 0, 1), transform=ax1.transAxes,
                               cmap=cmap, cmap_range=(c_min, c_max))
                ax1.set_aspect('auto')
                fig1.tight_layout()
                plt.show()

                # if brasil and pt:
                #     save_path_img = 'reports_pdf/brasil/risk-pt/' + last_day + '-' + region[ID] + '.png'
                #     plt.savefig(save_path_img, bbox_inches='tight', dpi=300)
                # try:
                pdf.savefig(fig1,bbox_inches='tight', dpi=300)
                plt.close('all')
                print(
                    "\n\nPrediction for the region of " + region[
                    ID] + " performed successfully!\nPath:" + save_path)
                # except:
                #     print("An exception occurred")
                # break


'''
            df = pd.DataFrame({
                                'Day': DIA,
                                'Cumulative cases': cumulative_cases,
                                'New cases': new_cases,
                                'ρ': p,
                                'ρ7': p_seven,
                                'New cases last 14 days (N14)': n_14_days,
                                'New cases last 14 days per 105 inhabitants (A14)': a_14_days,
                                'Risk (N14*ρ7)': risk,
                                'Risk per 105 (A14*ρ7)': risk_per_10,
                                'population':pop 
      
            })
            with ExcelWriter('/home/allissondantas/Matlab/Code/Indexs_Brasil-caruaru.xlsx') as writer:
                df.to_excel(writer, sheet_name='Alt_Urgell')
            break
'''

if __name__ == "__main__":
    #sys.argv.append('brasil')
    #sys.argv.append('recife')
    main()
