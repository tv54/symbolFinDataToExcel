class Constants():
# ---- Modificables
    # ---- API constants
    # FMP_API_KEY='023d421360a161d2cdea04f24b8f6b9e'
    FMP_API_KEY='0817e69b87e9fb8bbe1ca4c4d47626e6'
    FMP_API_KEY_ALT='584df76f6744caf976b9140305b95dbd'

    # File constants
    OUTPUT_FOLDER='output'
    DISPLAYED_LINES_FILE="Registros de la ultima sesión.txt"

    # ---- Style constants ----
    ROUND_DECIMALS=2
    SHOW_GRIDLINES=False
    SUMMARY_FIRST_COLUMN_WIDTH=3
    FINANCIAL_STATEMENTS_FIRST_COL_WIDTH=47
    FINANCIAL_STATEMENTS_OTHER_COL_WIDTH=24.43
    HISTORICAL_SHEET_COL_WIDTH=11.3
    SUMMARY_NUMBER_COLUMN_WIDTH=50
    CHART_LEGEND_POSITION="b"
    CHART_WIDTH=30
    CHART_HEIGHT=10

    # Funtionality constants
    LOG_DATA=False
    DIV_OF_VALUES=1000

# ---- No modificables
    # ---- API constants
    # EOD_API_KEY='625c17ab4da411.45817193'
    # EOD_API_URL=''
    FMP_API_URL='https://financialmodelingprep.com/api/v3'

    # File constants
    LOG_FILE="./log.txt"
    WORKBOOK_NAME='DefaultOutputSpreadsheet.xlsx'

    # ---- Style constants ----
    DARK_BLUE_COLOR="002060"
    DARK_GRAY_COLOR="6F6F6F"
    DARK_BROWN_COLOR="5F3F1F"
    LIGHT_GRAY_COLOR="F2F2F2"
    NUMBER_FORMAT_ACCOUNTING='_(* #,##0.{0}_);_(* (#,##0.{0});_(* \"-\"??_);_(@_)'.format("0" * ROUND_DECIMALS)

    # Funtionality constants
    COLUMN_NAMES=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', ]
    HIST_PRICES_COLUMNS=["open", "close", "low", "high"]
    BENCHMARK_PRICE_BASE_VALUE=100
    SLEEP_SECONDS_BETWEEN_PETITIONS=1
    PROFILE_ROW_NAMES=["Datos básicos a la fecha", "", "Beta (5Y)", "Volumen operado promedio", "Capitalización de mercado (En miles)", "Industria", "Sector", "Página web", "Prev. De rentabilidad y dividendo", "", "Ratios de valuación", "", "P/E (TTM)", "BPA (TTM)", "Precio a CFO", "Valor a EBITDA", "", "Ratios de liquidéz", "", "Current Ratio", "Quick Ratio", "Cash Ratio", "Ciclo Operativo", "", "Ratios de rentabilidad", "", "Márgen de rentabilidad operativa", "Márgen de rentabilidad bruta", "Márgen de rentabilidad neta", "ROE", "ROA", "", "Ratios de endeudamiento", "", "Deuda sobre equity", "Cobertura de intereses", "CFO sobre deuda"]
    CFS_ROW_NAMES=["Flujo de actividad de operación", "Ingreso neto", "Depreciación y amortización", "Impuesto sobre beneficios diferidos", "Cambio en capital de trabajo", "...", "", "Flujo de actividad de inversión", "Inversiones en activos fijos", "...", "", "Flujo de actividad de financiamiento", "Pago de deuda", "Acciones ordinarias emitidas", "Acciones ordinarias readquiridas", "Pago de dividendos", "Otras actividades de financiación", "...", "", "Cambio neto de caja", "", "Flujo de caja libre"]
    BSS_ROW_NAMES=["Activo", "Activo corriente", "Efectivo y activos líquidos", "Cuentas pendientes netas", "Inventario", "...", "Activo no corriente", "Activos fijos brutos", "...", "", "Pasivo", "Pasivo corriente", "Deuda corriente", "Cuentas por pagar", "...", "Pasivo no corriente", "Deuda a largo plazo", "Pasivo por impuestos diferidos", "...", "", "Patrimonio neto", "Acción ordinaria", "Ganancias acumuladas", "Otro resultado integral acumulado"]
    IS_ROW_NAMES=["Resultado bruto", "Ingresos totales", "Costo de ingresos", "", "Ingreso operativo", "Gastos operativos", "", "EBT", "Ingreso por intereses", "Egreso por intereses", "...", "", "Resultado neto", "Impuesto sobre ingresos", "", "EBITDA"]
    ENABLE_SUMMARY_SHEET = True
    ENABLE_SYMBOL_HIST_DATA_SHEET = True
    ENABLE_CFS_SHEET = True
    ENABLE_BSS_SHEET = True
    ENABLE_IS_SHEET = True
    