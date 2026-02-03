# 💰 Calendário de Pagamentos - Streamlit

Aplicativo web interativo para visualização de pagamentos em formato de calendário mensal.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Instale as dependências:**
```bash
pip install streamlit pandas
```

2. **Execute o aplicativo:**
```bash
streamlit run calendario_pagamentos.py
```

3. **Acesse no navegador:**
   - O aplicativo abrirá automaticamente em `http://localhost:8501`

## 📊 Funcionalidades

### ✅ Principais Recursos

- **Calendário Mensal Interativo**: Visualize todos os pagamentos organizados dia a dia
- **Distinção Visual**: Cores diferentes para pagamentos pendentes (vermelho) e pagos (verde)
- **Upload de CSV**: Carregue seus dados diretamente no aplicativo
- **Estatísticas em Tempo Real**: 
  - Total a pagar
  - Total pago
  - Quantidade de pendentes
  - Quantidade de pagos
- **Navegação por Período**: Selecione mês e ano para visualizar
- **Totais por Dia**: Veja resumos financeiros de cada dia
- **Tabelas Detalhadas**: Acesse informações completas em formato tabular
- **Responsivo**: Adapta-se a diferentes tamanhos de tela

### 📝 Formato do Arquivo CSV

O arquivo CSV deve conter as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `fornecedor_nome` | Nome do fornecedor | ENEL SP |
| `numero_documento` | Número do documento/nota fiscal | 12345 |
| `data_vencimento` | Data de vencimento | 2026-12-30 |
| `data_pagamento` | Data do pagamento (NULL se pendente) | 2026-12-28 |
| `valor_em_aberto` | Valor pendente | 4385.10 |
| `valor_pago_total` | Valor já pago | 4385.10 |
| `status_consolidado` | Status do pagamento | A Pagar / Pago |

## 🎨 Interface

### Calendário
- **Dias vazios**: Cinza claro
- **Dia atual**: Destaque com borda vermelha
- **Pagamentos pendentes**: Card vermelho
- **Pagamentos pagos**: Card verde
- **Hover**: Efeito de sombra ao passar o mouse

### Cards de Pagamento
Cada card exibe:
- Nome do fornecedor (negrito)
- Valor (formatado em R$)
- Número do documento

### Resumo Diário
Ao final de cada dia, mostra:
- Total a pagar (vermelho)
- Total pago (verde)

## 📱 Navegação

### Filtros
- **Seletor de Ano**: Escolha o ano desejado
- **Seletor de Mês**: Escolha o mês desejado

### Abas de Detalhes
1. **📊 Resumo**: Divisão entre pagamentos pendentes e pagos
2. **📄 Tabela Completa**: Todos os dados em formato tabular

## 💡 Dicas de Uso

1. **Primeira vez**: Faça upload do seu arquivo CSV no campo indicado
2. **Navegação**: Use os seletores de mês/ano para navegar entre períodos
3. **Detalhes**: Role a página para ver estatísticas e tabelas detalhadas
4. **Exportação**: Use as tabelas para copiar dados específicos

## 🔧 Personalização

### Cores
As cores podem ser ajustadas no CSS customizado no início do código:
- Pagamentos pendentes: `#f56565` (vermelho)
- Pagamentos pagos: `#48bb78` (verde)
- Cabeçalho: Gradiente roxo

### Formatação de Valores
Os valores são formatados automaticamente para o padrão brasileiro (R$):
- Exemplo: `4385.10` → `R$ 4.385,10`

## 📊 Estatísticas Exibidas

### Dashboard Principal
- Total geral a pagar
- Total geral pago
- Quantidade de pagamentos pendentes
- Quantidade de pagamentos realizados

### Por Mês
- Total a pagar no mês
- Total pago no mês
- Lista detalhada de cada pagamento

## ⚠️ Observações

- O aplicativo processa apenas registros com data de vencimento válida
- Datas no formato ISO (YYYY-MM-DD) são recomendadas
- Valores devem ser numéricos (decimais com ponto)
- O arquivo CSV deve usar vírgula como separador

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicativos web
- **Pandas**: Manipulação e análise de dados
- **Python Calendar**: Geração de calendários
- **HTML/CSS**: Customização visual

## 📞 Suporte

Se encontrar algum problema:
1. Verifique se todas as colunas necessárias estão presentes no CSV
2. Confirme que as datas estão em formato válido
3. Verifique se os valores numéricos estão corretos

---

**Desenvolvido com ❤️ usando Streamlit**
