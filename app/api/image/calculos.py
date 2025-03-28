
def PorcentajePositivos(data):
    labels = data['resultado']['labels']

    count_positivo = labels.count("Positivo")

    porcentaje_positivo = 0
    total_labels = len(labels)
    if total_labels > 0:
        porcentaje_positivo = (count_positivo / total_labels) * 100  
    
    interpretacion = ""
    if porcentaje_positivo < 10:
        interpretacion = "Bajo índice de proliferación"
    elif porcentaje_positivo >10 and porcentaje_positivo < 30:
        interpretacion ="Moderado índice de proliferación"
    else: interpretacion ="Alto índice de proliferación"

    return {'datos':{'porcentaje_positivo':porcentaje_positivo,
                     'interpretacion':interpretacion,
                     'IA total cells': total_labels,
                     'IA Positive Cells':count_positivo,
                     'IA Negative Cells':(total_labels-count_positivo)

                     },
                     'respuesta':data
            }