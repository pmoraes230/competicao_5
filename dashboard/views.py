from django.shortcuts import render, redirect
from django.contrib import messages
from home.views import get_user_profile
from home import models
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import numpy as np
import base64
import io

def dash(request):
    context = get_user_profile(request)
    
    event = None
    sectors = None
    types_of_sectors = []
    grafic_sectors = []
    
    if request.method == "POST":
        result_search = request.POST.get("event")
        try:
            event = models.Evento.objects.get(nome=result_search)
            sectors = models.Setor.objects.filter(evento=event)
            types_of_sectors = [sector.nome for sector in sectors]
            tickets = models.Ingresso.objects.filter(evento=event)

            issued_by_sector = {t: tickets.filter(setor__nome=t, status='emitido').count() for t in types_of_sectors}
            validation_by_sector = {t: tickets.filter(setor__nome=t, status='validado').count() for t in types_of_sectors}
            sector_capacity = {setor.nome: setor.quantidade_ingresso for setor in sectors}
            
            for name_sector in types_of_sectors:
                labels = [f"Capacidade ({name_sector})", f"Emitido ({name_sector})", f"Validados ({name_sector})"]
                data = [sector_capacity[name_sector], issued_by_sector[name_sector], validation_by_sector[name_sector]]
                filtered_labels = [labels[i] for i in range(len(data)) if data[i] > 0]
                filtered_data = [d for d in data if d > 0]
                
                if filtered_data:
                    fig, ax = plt.subplots(figsize=(6,4))
                    colors = ['#ff9999', '#99ccff', '#ffff99'][:len(filtered_data)]
                    
                    x_pos = np.arange(len(filtered_data))
                    bars = ax.bar(x_pos, filtered_data, color=colors)
                    
                    ax.set_xticks(x_pos)
                    ax.set_xticklabels(filtered_labels, rotation=30, ha='right')
                    
                    # Adiciona valores em cima das barras
                    for bar in bars:
                        height = bar.get_height()
                        ax.annotate(f'{height}',
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3),  # 3 points de deslocamento para cima
                                    textcoords="offset points",
                                    ha='center', va='bottom')
                    
                    plt.tight_layout()
                    
                    buf = io.BytesIO()
                    plt.savefig(buf, format="png", bbox_inches='tight')
                    plt.close(fig)
                    grafic_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    buf.close()
                    
                    grafic_sectors.append({'sector': name_sector, 'grafic': grafic_base64})
                    
        except models.Evento.DoesNotExist:
            messages.error(request, "Evento não encontrado")
            return redirect("dash")
        
    context.update({
        'event': event,
        'type_sector': types_of_sectors,
        'grafic_sector': grafic_sectors
    })
    
    return render(request, "dash.html",context)
