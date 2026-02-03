import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
import locale

# Configuração da página
st.set_page_config(page_title="Calendário de Pagamentos", layout="wide", page_icon="💰")

# Tentar configurar locale para português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass

# CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .calendar-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .calendar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        border-radius: 8px 8px 0 0;
        margin-bottom: 20px;
    }
    .day-header {
        background-color: #667eea;
        color: white;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #5568d3;
    }
    .calendar-day {
        border: 1px solid #e0e0e0;
        padding: 8px;
        min-height: 120px;
        background-color: white;
        position: relative;
    }
    .day-number {
        font-weight: bold;
        font-size: 16px;
        color: #333;
        margin-bottom: 5px;
        position: sticky;
        top: 0;
        background-color: white;
        padding: 2px 0;
    }
    .today {
        background-color: #fff9c4 !important;
    }
    .item-pagar {
        background-color: #ffebee;
        border-left: 3px solid #f44336;
        padding: 6px;
        margin: 3px 0;
        border-radius: 3px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .item-pagar:hover {
        background-color: #ffcdd2;
        transform: translateX(2px);
    }
    .item-pago {
        background-color: #e8f5e9;
        border-left: 3px solid #4caf50;
        padding: 6px;
        margin: 3px 0;
        border-radius: 3px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .item-pago:hover {
        background-color: #c8e6c9;
        transform: translateX(2px);
    }
    .fornecedor {
        font-weight: bold;
        color: #1976d2;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .valor {
        font-weight: bold;
        color: #d32f2f;
        font-size: 12px;
    }
    .valor-pago {
        font-weight: bold;
        color: #388e3c;
        font-size: 12px;
    }
    .documento {
        color: #666;
        font-size: 10px;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .stats-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stats-value {
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    .stats-label {
        color: #666;
        font-size: 14px;
    }
    .pagar-color {
        color: #f44336;
    }
    .pago-color {
        color: #4caf50;
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

# Título
st.title("📅 Calendário de Pagamentos")

# Upload de arquivo
uploaded_file = st.file_uploader("📂 Faça upload do arquivo CSV", type=['csv'])

if uploaded_file is not None:
    # Ler o CSV
    df = pd.read_csv(uploaded_file)
    
    # Converter datas
    df['data_vencimento'] = pd.to_datetime(df['data_vencimento'], errors='coerce')
    df['data_pagamento'] = pd.to_datetime(df['data_pagamento'], errors='coerce')
    
    # Filtrar apenas registros com data de vencimento válida
    df = df[df['data_vencimento'].notna()]
    
    # Seleção de mês e ano
    col1, col2 = st.columns(2)
    
    # Obter range de datas disponíveis
    min_date = df['data_vencimento'].min()
    max_date = df['data_vencimento'].max()
    
    with col1:
        anos_disponiveis = sorted(df['data_vencimento'].dt.year.unique())
        ano_selecionado = st.selectbox("📅 Ano", anos_disponiveis, 
                                        index=len(anos_disponiveis)-1 if anos_disponiveis else 0)
    
    with col2:
        mes_selecionado = st.selectbox("📅 Mês", range(1, 13), 
                                        format_func=lambda x: nome_mes_pt(x),
                                        index=datetime.now().month - 1)
    
    # Filtrar dados do mês selecionado
    df_mes = df[
        (df['data_vencimento'].dt.year == ano_selecionado) & 
        (df['data_vencimento'].dt.month == mes_selecionado)
    ].copy()
    
    # Estatísticas
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_a_pagar = df_mes[df_mes['status_consolidado'] == 'A'].groupby('data_vencimento')['valor_em_aberto'].sum().sum()
    total_pago = df_mes[df_mes['status_consolidado'] == 'F']['valor_pago_total'].sum()
    qtd_a_pagar = len(df_mes[df_mes['status_consolidado'] == 'A'])
    qtd_pago = len(df_mes[df_mes['status_consolidado'] == 'F'])
    
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
            <div class="stats-label">Contas a Pagar</div>
            <div class="stats-value pagar-color">{qtd_a_pagar}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Contas Pagas</div>
            <div class="stats-value pago-color">{qtd_pago}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Criar calendário
    cal = calendar.monthcalendar(ano_selecionado, mes_selecionado)
    
    # Header do calendário
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
    
    # Renderizar semanas
    for semana in cal:
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
                    lancamentos_dia = df_mes[df_mes['data_vencimento'].dt.date == data_dia]
                    
                    # Construir HTML do dia
                    html_dia = f'<div class="calendar-day {classe_hoje}">'
                    html_dia += f'<div class="day-number">{dia}</div>'
                    
                    for _, lanc in lancamentos_dia.iterrows():
                        fornecedor = str(lanc['fornecedor_nome'])[:25]
                        documento = str(lanc['numero_documento']) if pd.notna(lanc['numero_documento']) else ""
                        
                        if lanc['status_consolidado'] == 'F':  # Pago
                            valor = formatar_real(lanc['valor_pago_total'])
                            html_dia += f'''
                            <div class="item-pago" title="{fornecedor} - {documento}">
                                <span class="fornecedor">{fornecedor}</span>
                                <span class="documento">Doc: {documento}</span>
                                <span class="valor-pago">{valor}</span>
                            </div>
                            '''
                        else:  # A Pagar
                            valor = formatar_real(lanc['valor_em_aberto'])
                            html_dia += f'''
                            <div class="item-pagar" title="{fornecedor} - {documento}">
                                <span class="fornecedor">{fornecedor}</span>
                                <span class="documento">Doc: {documento}</span>
                                <span class="valor">{valor}</span>
                            </div>
                            '''
                    
                    html_dia += '</div>'
                    st.markdown(html_dia, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Legenda
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 20px; height: 20px; background-color: #ffebee; border-left: 3px solid #f44336; margin-right: 10px;"></div>
            <span>Contas a Pagar</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 20px; height: 20px; background-color: #e8f5e9; border-left: 3px solid #4caf50; margin-right: 10px;"></div>
            <span>Contas Pagas</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabela detalhada
    st.markdown("---")
    st.subheader("📊 Detalhes do Mês")
    
    # Preparar dados para exibição
    df_display = df_mes[[
        'data_vencimento', 'fornecedor_nome', 'numero_documento', 
        'valor_em_aberto', 'valor_pago_total', 'status_consolidado'
    ]].copy()
    
    df_display['data_vencimento'] = df_display['data_vencimento'].dt.strftime('%d/%m/%Y')
    df_display['valor_em_aberto'] = df_display['valor_em_aberto'].apply(formatar_real)
    df_display['valor_pago_total'] = df_display['valor_pago_total'].apply(formatar_real)
    df_display['status_consolidado'] = df_display['status_consolidado'].map({
        'A': '⏳ A Pagar',
        'F': '✅ Pago'
    })
    
    df_display.columns = ['Data Vencimento', 'Fornecedor', 'Documento', 
                          'Valor a Pagar', 'Valor Pago', 'Status']
    
    # Ordenar por data
    df_display = df_display.sort_values('Data Vencimento')
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

else:
    st.info("👆 Por favor, faça upload de um arquivo CSV para visualizar o calendário de pagamentos.")
    
    st.markdown("""
    ### 📋 Formato esperado do CSV
    
    O arquivo deve conter as seguintes colunas principais:
    - `fornecedor_nome`: Nome do fornecedor
    - `numero_documento`: Número do documento
    - `data_vencimento`: Data de vencimento
    - `valor_em_aberto`: Valor a pagar
    - `valor_pago_total`: Valor pago
    - `status_consolidado`: Status (A = A Pagar, F = Pago)
    """)
