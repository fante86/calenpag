import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
import locale

# Configuração da página
st.set_page_config(page_title="Calendário de Pagamentos", layout="wide", page_icon="💰")

# CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        padding-top: 1rem;
    }
    .calendar-container {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .calendar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .day-header {
        background-color: #667eea;
        color: white;
        padding: 8px 4px;
        text-align: center;
        font-weight: bold;
        font-size: 13px;
        border: 1px solid #5568d3;
    }
    .calendar-day {
        border: 1px solid #dee2e6;
        padding: 6px;
        min-height: 80px;
        max-height: 80px;
        background-color: white;
        cursor: pointer;
        transition: all 0.2s;
        overflow: hidden;
    }
    .calendar-day:hover {
        background-color: #f8f9fa;
        border-color: #667eea;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
    }
    .day-number {
        font-weight: bold;
        font-size: 14px;
        color: #333;
        margin-bottom: 4px;
    }
    .today {
        background-color: #fff9e6 !important;
        border: 2px solid #ffc107 !important;
    }
    .day-summary {
        font-size: 10px;
        margin-top: 4px;
    }
    .summary-pagar {
        background-color: #ffebee;
        color: #c62828;
        padding: 2px 4px;
        border-radius: 3px;
        display: block;
        margin: 2px 0;
        font-weight: 600;
    }
    .summary-pago {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 2px 4px;
        border-radius: 3px;
        display: block;
        margin: 2px 0;
        font-weight: 600;
    }
    .stats-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .stats-value {
        font-size: 24px;
        font-weight: bold;
        margin: 8px 0;
    }
    .stats-label {
        color: #666;
        font-size: 13px;
        font-weight: 500;
    }
    .pagar-color {
        color: #d32f2f;
    }
    .pago-color {
        color: #388e3c;
    }
    .conta-item {
        background-color: #f8f9fa;
        padding: 10px;
        margin: 8px 0;
        border-radius: 6px;
        border-left: 4px solid;
    }
    .conta-pagar {
        border-left-color: #f44336;
        background-color: #ffebee;
    }
    .conta-paga {
        border-left-color: #4caf50;
        background-color: #e8f5e9;
    }
</style>
""", unsafe_allow_html=True)

# Função para formatar valor em reais
def formatar_real(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

# Função para obter nome do mês em português
def nome_mes_pt(mes):
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    return meses.get(mes, "")

# Função para obter nomes dos dias da semana
def nomes_dias_semana():
    return ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

# Título compacto
st.title("💰 Calendário de Pagamentos")

# Upload de arquivo
uploaded_file = st.file_uploader("📂 Upload do CSV", type=['csv'], label_visibility="collapsed")

if uploaded_file is not None:
    # Ler o CSV
    df = pd.read_csv(uploaded_file)
    
    # Converter datas
    df['data_vencimento'] = pd.to_datetime(df['data_vencimento'], errors='coerce')
    df['data_pagamento'] = pd.to_datetime(df['data_pagamento'], errors='coerce')
    
    # Filtrar apenas registros válidos (não cancelados e com data de vencimento)
    # O status está como "A Pagar", "Pago", "Cancelado" (por extenso)
    df = df[
        (df['data_vencimento'].notna()) & 
        (df['status_consolidado'] != 'Cancelado')  # Excluir cancelados
    ].copy()
    
    # Seleção de mês e ano em uma linha
    col1, col2, col3 = st.columns([1, 1, 3])
    
    anos_disponiveis = sorted(df['data_vencimento'].dt.year.unique())
    
    with col1:
        ano_selecionado = st.selectbox("Ano", anos_disponiveis, 
                                        index=len(anos_disponiveis)-1 if anos_disponiveis else 0)
    
    with col2:
        mes_selecionado = st.selectbox("Mês", range(1, 13), 
                                        format_func=lambda x: nome_mes_pt(x),
                                        index=datetime.now().month - 1)
    
    # Filtrar dados do mês selecionado
    df_mes = df[
        (df['data_vencimento'].dt.year == ano_selecionado) & 
        (df['data_vencimento'].dt.month == mes_selecionado)
    ].copy()
    
    # Calcular estatísticas CORRETAS
    # A Pagar: status_consolidado = 'A Pagar' e usar valor_em_aberto
    df_a_pagar = df_mes[df_mes['status_consolidado'] == 'A Pagar']
    total_a_pagar = df_a_pagar['valor_em_aberto'].sum()
    qtd_a_pagar = len(df_a_pagar)
    
    # Pago: status_consolidado = 'Pago' e usar valor_pago_total
    df_pago = df_mes[df_mes['status_consolidado'] == 'Pago']
    total_pago = df_pago['valor_pago_total'].sum()
    qtd_pago = len(df_pago)
    
    # Estatísticas em cards compactos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Total a Pagar</div>
            <div class="stats-value pagar-color">{formatar_real(total_a_pagar)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Total Pago</div>
            <div class="stats-value pago-color">{formatar_real(total_pago)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Títulos a Pagar</div>
            <div class="stats-value pagar-color">{qtd_a_pagar}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Títulos Pagos</div>
            <div class="stats-value pago-color">{qtd_pago}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Criar calendário
    cal = calendar.monthcalendar(ano_selecionado, mes_selecionado)
    
    # Container do calendário
    st.markdown(f"""
    <div class="calendar-container">
        <div class="calendar-header">
            {nome_mes_pt(mes_selecionado)} de {ano_selecionado}
        </div>
    """, unsafe_allow_html=True)
    
    # Dias da semana
    dias_semana = nomes_dias_semana()
    cols_header = st.columns(7)
    for i, dia in enumerate(dias_semana):
        with cols_header[i]:
            st.markdown(f'<div class="day-header">{dia}</div>', unsafe_allow_html=True)
    
    # Data de hoje
    hoje = datetime.now().date()
    
    # Inicializar session state para dia selecionado
    if 'dia_selecionado' not in st.session_state:
        st.session_state.dia_selecionado = None
    
    # Renderizar semanas
    for idx_semana, semana in enumerate(cal):
        cols = st.columns(7)
        
        for i, dia in enumerate(semana):
            with cols[i]:
                if dia == 0:
                    st.markdown('<div class="calendar-day"></div>', unsafe_allow_html=True)
                else:
                    # Criar data do dia
                    data_dia = datetime(ano_selecionado, mes_selecionado, dia).date()
                    
                    # Verificar se é hoje
                    classe_hoje = "today" if data_dia == hoje else ""
                    
                    # Filtrar lançamentos do dia
                    lanc_dia = df_mes[df_mes['data_vencimento'].dt.date == data_dia]
                    
                    # Calcular totais do dia
                    lanc_pagar = lanc_dia[lanc_dia['status_consolidado'] == 'A Pagar']
                    lanc_pago = lanc_dia[lanc_dia['status_consolidado'] == 'Pago']
                    
                    total_dia_pagar = lanc_pagar['valor_em_aberto'].sum()
                    qtd_dia_pagar = len(lanc_pagar)
                    
                    total_dia_pago = lanc_pago['valor_pago_total'].sum()
                    qtd_dia_pago = len(lanc_pago)
                    
                    # Construir HTML do dia
                    html_dia = f'<div class="calendar-day {classe_hoje}">'
                    html_dia += f'<div class="day-number">{dia}</div>'
                    html_dia += '<div class="day-summary">'
                    
                    if qtd_dia_pagar > 0:
                        html_dia += f'<span class="summary-pagar">🔴 {qtd_dia_pagar} • {formatar_real(total_dia_pagar)}</span>'
                    
                    if qtd_dia_pago > 0:
                        html_dia += f'<span class="summary-pago">🟢 {qtd_dia_pago} • {formatar_real(total_dia_pago)}</span>'
                    
                    html_dia += '</div></div>'
                    
                    st.markdown(html_dia, unsafe_allow_html=True)
                    
                    # Botão invisível para capturar clique (posicionado sobre o dia)
                    if st.button("📅", key=f"btn_{ano_selecionado}_{mes_selecionado}_{dia}", 
                                help=f"Ver detalhes do dia {dia}", use_container_width=True):
                        st.session_state.dia_selecionado = data_dia
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mostrar detalhes do dia selecionado
    if st.session_state.dia_selecionado:
        data_sel = st.session_state.dia_selecionado
        
        st.markdown("---")
        
        col_titulo, col_fechar = st.columns([5, 1])
        with col_titulo:
            st.subheader(f"📅 Detalhes de {data_sel.strftime('%d/%m/%Y')}")
        with col_fechar:
            if st.button("✖ Fechar", key="fechar_detalhes"):
                st.session_state.dia_selecionado = None
                st.rerun()
        
        # Filtrar contas do dia
        contas_dia = df_mes[df_mes['data_vencimento'].dt.date == data_sel]
        
        if len(contas_dia) > 0:
            for _, conta in contas_dia.iterrows():
                status = conta['status_consolidado']
                classe = "conta-pagar" if status == 'A Pagar' else "conta-paga"
                
                fornecedor = conta['fornecedor_nome']
                documento = conta['numero_documento'] if pd.notna(conta['numero_documento']) else "Sem documento"
                
                if status == 'Pago':
                    valor = formatar_real(conta['valor_pago_total'])
                    status_texto = "✅ PAGO"
                    cor_status = "#4caf50"
                else:
                    valor = formatar_real(conta['valor_em_aberto'])
                    status_texto = "⏳ A PAGAR"
                    cor_status = "#f44336"
                
                observacao = conta['observacao'] if pd.notna(conta['observacao']) else ""
                
                st.markdown(f"""
                <div class="conta-item {classe}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <div style="font-weight: bold; color: #1976d2; font-size: 16px;">{fornecedor}</div>
                            <div style="color: #666; font-size: 13px; margin-top: 4px;">
                                📄 Doc: {documento}
                            </div>
                            {f'<div style="color: #666; font-size: 12px; margin-top: 4px; font-style: italic;">{observacao}</div>' if observacao else ''}
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 12px; color: {cor_status}; font-weight: 600;">{status_texto}</div>
                            <div style="font-size: 20px; font-weight: bold; color: {cor_status}; margin-top: 4px;">{valor}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma conta neste dia.")

else:
    st.info("👆 Faça upload do arquivo CSV para visualizar o calendário")
    
    st.markdown("""
    ### 📋 Colunas necessárias no CSV:
    - `fornecedor_nome`
    - `numero_documento`
    - `data_vencimento`
    - `valor_em_aberto` (para contas a pagar)
    - `valor_pago_total` (para contas pagas)
    - `status_consolidado` ("A Pagar", "Pago", "Cancelado")
    - `observacao` (opcional)
    """)
