#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe en formato Word (.docx) sin dependencias externas.
Un .docx es un contenedor ZIP con XML (Office Open XML / WordprocessingML).
"""
import zipfile

AZUL = "1B3A6B"
AZUL2 = "2B5AA0"
ROJO = "B02A2A"

def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))

# ---- helpers para construir XML de WordprocessingML ----
def run(text, bold=False, color=None, size=None):
    rpr = ""
    props = ""
    if bold:
        props += "<w:b/>"
    if color:
        props += f'<w:color w:val="{color}"/>'
    if size:
        props += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
    if props:
        rpr = f"<w:rPr>{props}</w:rPr>"
    # preservar espacios
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def para(runs, style=None, spacing_after=120):
    if isinstance(runs, str):
        runs = [run(runs)]
    ppr = "<w:pPr>"
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    ppr += f'<w:spacing w:after="{spacing_after}"/>'
    ppr += "</w:pPr>"
    return f"<w:p>{ppr}{''.join(runs)}</w:p>"

def bullet(text_runs):
    if isinstance(text_runs, str):
        text_runs = [run(text_runs)]
    ppr = ('<w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="60"/></w:pPr>')
    return f"<w:p>{ppr}{''.join(text_runs)}</w:p>"

def cell(runs, fill=None, width=None, bold=False, color=None):
    if isinstance(runs, str):
        runs = [run(runs, bold=bold, color=color)]
    tcpr = "<w:tcPr>"
    if width:
        tcpr += f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if fill:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    tcpr += '<w:vAlign w:val="center"/></w:tcPr>'
    body = f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>{"".join(runs)}</w:p>'
    return f"<w:tc>{tcpr}{body}</w:tc>"

def table(rows, widths, header=True):
    total = sum(widths)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    borders = ("<w:tblBorders>"
               '<w:top w:val="single" w:sz="4" w:color="D6DBE3"/>'
               '<w:left w:val="single" w:sz="4" w:color="D6DBE3"/>'
               '<w:bottom w:val="single" w:sz="4" w:color="D6DBE3"/>'
               '<w:right w:val="single" w:sz="4" w:color="D6DBE3"/>'
               '<w:insideH w:val="single" w:sz="4" w:color="D6DBE3"/>'
               '<w:insideV w:val="single" w:sz="4" w:color="D6DBE3"/>'
               "</w:tblBorders>")
    tblpr = (f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/>'
             f'{borders}<w:tblLook w:val="04A0"/></w:tblPr>')
    trs = []
    for i, r in enumerate(rows):
        cells = []
        is_head = header and i == 0
        for j, c in enumerate(r):
            if isinstance(c, tuple):
                txt, cbold = c
            else:
                txt, cbold = c, False
            if is_head:
                cells.append(cell([run(txt, bold=True, color="FFFFFF")],
                                  fill=AZUL, width=widths[j]))
            else:
                fill = "F4F6F9" if i % 2 == 0 else None
                cells.append(cell([run(txt, bold=cbold)], fill=fill, width=widths[j]))
        trs.append(f"<w:tr>{''.join(cells)}</w:tr>")
    return f"<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>" \
           + '<w:p><w:pPr><w:spacing w:after="80"/></w:pPr></w:p>'

# ============ CONTENIDO DEL INFORME ============
B = []  # body elements
B.append(para([run("INFORME DE PREFACTIBILIDAD", bold=True, color=AZUL, size=20)], spacing_after=40))
B.append(para([run("Sistema de Generación Fotovoltaica Residencial con Configuración Net Billing y Respaldo con Batería de Litio", bold=True, color=AZUL2, size=13)], spacing_after=200))

# Ficha
ficha = [
    ["Campo", "Detalle"],
    ["Ubicación", "Colono María Seidel 2504, Puerto Montt, Región de Los Lagos"],
    ["Cliente", "Cesar Barria Oyarzo | N° Cliente SAESA 10982361 | Medidor 3101198"],
    ["Tarifa actual", "BT1 (baja tensión residencial) | Potencia conectada 6,0 kW"],
    ["Distribuidora", "Sociedad Austral de Electricidad S.A. (SAESA)"],
    ["Fecha / Nivel", "Julio 2026 | Prefactibilidad (Clase 4, ±25–30 %)"],
]
B.append(table(ficha, [2400, 6600]))

B.append(para([run("1. Resumen Ejecutivo", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para("Se evalúa la instalación de un sistema fotovoltaico (FV) conectado a la red bajo modalidad Net Billing (Ley 21.118), con batería de litio (LiFePO4) para autoconsumo nocturno y respaldo, en una vivienda de Puerto Montt cuyo consumo promedio es de 93,53 kWh/mes (aprox. 1.122 kWh/año)."))
resumen = [
    ["Parámetro", "Valor"],
    ["Potencia FV recomendada", ("1,65 kWp (3 paneles de 550 W)", True)],
    ["Inversor", "Híbrido 3 kW (apto litio, con MPPT)"],
    ["Batería", ("LiFePO4 48 V / 100 Ah (5,12 kWh)", True)],
    ["Generación estimada", "1.550 kWh/año (138 % del consumo)"],
    ["Inversión total (CAPEX)", ("$ 4.310.250 CLP", True)],
    ["VAN (8 %, 20 años)", ("-$ 2.032.020 CLP", True)],
    ["TIR", ("1,4 %", True)],
    ["PRI (simple)", ("18,2 años", True)],
]
B.append(table(resumen, [4200, 4800]))
B.append(para([run("Conclusión anticipada: ", bold=True),
               run("el proyecto es técnicamente viable y cumple la normativa vigente, pero no es rentable financieramente con el consumo actual. El bajo consumo del cliente y el alto costo de la batería producen un VAN negativo. La batería se justifica como inversión de respaldo/resiliencia (continuidad ante interrupciones frecuentes en la zona sur), no como inversión de retorno económico.")]))

B.append(para([run("2. Objetivo y Alcance", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para("Diseñar a nivel de prefactibilidad un sistema de generación en base al recurso solar, dimensionando paneles, inversor, batería, materiales y protecciones; valorizar los componentes físicos y los recursos humanos; y evaluar la inversión mediante los indicadores VAN, TIR y PRI, conforme a la normativa chilena vigente y a las buenas prácticas del mercado."))

B.append(para([run("3. Análisis del Recurso Natural Renovable Disponible", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para([run("3.1 Localización", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(bullet("Comuna: Puerto Montt, Región de Los Lagos."))
B.append(bullet("Latitud: -41,47° | Longitud: -72,94°."))
B.append(bullet("Clima: templado lluvioso oceánico, con alta nubosidad y estacionalidad marcada."))
B.append(para([run("3.2 Recurso solar (Explorador Solar - Min. Energía / metodología PVGIS)", bold=True, color=AZUL2, size=12)], spacing_after=60))
recurso = [
    ["Indicador", "Valor estimado"],
    ["Irradiación / HSP promedio anual (plano 35°)", ("3,3 kWh/m²/día", True)],
    ["HSP verano (Dic-Ene)", "aprox. 5,5 kWh/m²/día"],
    ["HSP invierno (Jun-Jul)", "aprox. 1,3 kWh/m²/día"],
    ["Ángulo de inclinación óptimo", "aprox. 35-40° (~ latitud)"],
    ["Orientación óptima", "Norte franco (azimut 0°)"],
]
B.append(table(recurso, [5400, 3600]))
B.append(para([run("3.3 Requerimientos mínimos de viabilidad", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(bullet("Irradiación mínima recomendada: > 3,0 kWh/m²/día -> se cumple (3,3)."))
B.append(bullet("Superficie de techo: aprox. 10 m² con orientación norte, libre de sombras (a verificar en visita técnica)."))
B.append(bullet("Estructura de soporte: capacidad para aprox. 15 kg/panel."))
B.append(para([run("Veredicto del recurso: VIABLE. ", bold=True, color=AZUL),
               run("Recurso modesto pero suficiente. La fuerte estacionalidad hace recomendable el net billing para banquear excedentes de verano.")]))

B.append(para([run("4. Determinación del Consumo Energético", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para("Datos obtenidos de la boleta electrónica SAESA N° 76633459."))
B.append(para([run("4.1 Consumo histórico (últimos 13 meses)", bold=True, color=AZUL2, size=12)], spacing_after=60))
consumo = [
    ["Mes", "kWh", "Mes", "kWh"],
    ["May-25", "76", "Dic-25", "120"],
    ["Jun-25", "106", "Ene-26", "134 (máx)"],
    ["Jul-25", "93", "Feb-26", "116"],
    ["Ago-25", "56 (mín)", "Mar-26", "112"],
    ["Sep-25", "91", "Abr-26", "88"],
    ["Oct-25", "85", "May-26", "87"],
    ["Nov-25", "61", "", ""],
]
B.append(table(consumo, [2250, 2250, 2250, 2250]))
B.append(para([run("4.2 Parámetros de diseño", bold=True, color=AZUL2, size=12)], spacing_after=60))
params = [
    ["Parámetro", "Valor"],
    ["Consumo promedio mensual (boleta)", ("93,53 kWh/mes", True)],
    ["Consumo anual de diseño", ("1.122 kWh/año", True)],
    ["Consumo diario promedio", "aprox. 3,1 kWh/día"],
    ["Mes de mayor consumo", "Enero (134 kWh)"],
    ["Mes de menor consumo", "Agosto (56 kWh)"],
    ["Costo variable de energía (referencia boleta)", "aprox. $222-255 /kWh"],
]
B.append(table(params, [5400, 3600]))

B.append(para([run("5. Diseño de Prefactibilidad del Sistema", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para([run("5.1 Normativa y marco regulatorio", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(bullet("Ley 21.118 (Net Billing / Generación Distribuida): autogeneración con ERNC e inyección de excedentes, hasta 300 kW."))
B.append(bullet("NCh Elec. 4/2003: instalaciones eléctricas de consumo en baja tensión."))
B.append(bullet("Pliego técnico RGR N°02 (SEC) para generación distribuida."))
B.append(bullet("Declaración TE-4 ante la SEC por instalador eléctrico autorizado."))
B.append(bullet("Solicitud de conexión y medidor bidireccional ante SAESA."))
B.append(bullet("Equipos con certificación SEC obligatoria."))
B.append(para([run("5.2 Dimensionamiento del generador fotovoltaico", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(para([run("Rendimiento específico (yield) = HSP x 365 x PR = 3,3 x 365 x 0,78 = 940 kWh/kWp/año", bold=True)]))
B.append(para([run("Potencia teórica (100% consumo) = 1.122 / 940 = 1,19 kWp")]))
B.append(para([run("Potencia adoptada = 3 x 550 W = 1,65 kWp")]))
B.append(para([run("Generación anual = 1,65 x 940 = 1.550 kWh/año (138% del consumo)", bold=True)]))
B.append(para("El sobredimensionamiento (1,65 vs 1,19 kWp) cubre pérdidas de batería (round-trip aprox. 90 %), degradación de paneles (0,7 %/año) y la estacionalidad invernal."))
B.append(para([run("5.3 Inversor", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(para("Inversor híbrido monofásico 3 kW, con MPPT integrado, gestión de batería de litio y función de respaldo (backup) ante corte de red. Ratio DC/AC conservador que permite ampliación futura."))
B.append(para([run("5.4 Batería de litio", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(para([run("Batería LiFePO4 48V/100Ah = 5,12 kWh nominales | Energía útil (DoD 90%) = 4,61 kWh | Autonomía aprox. 1,5 días de consumo.", bold=True)]))
B.append(para("Química LiFePO4 por seguridad, vida útil (> 6.000 ciclos) y tolerancia al clima frío. Función: desplazar el autoconsumo al horario nocturno y dar respaldo ante cortes."))
B.append(para([run("5.5 Balance energético anual (Net Billing)", bold=True, color=AZUL2, size=12)], spacing_after=60))
balance = [
    ["Flujo", "kWh/año"],
    ["Generación FV", "1.550"],
    ["Autoconsumo (directo + batería)", "1.010"],
    ["Importación desde la red", "112"],
    ["Excedente inyectado a la red", ("540", True)],
]
B.append(table(balance, [5400, 3600]))
B.append(para([run("5.6 Materiales y protecciones (NCh Elec 4/2003)", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(bullet("Estructura de aluminio anodizado + tornillería inoxidable."))
B.append(bullet("Cable solar 4-6 mm² (DC), conectores MC4."))
B.append(bullet("Protecciones DC: fusibles gPV, seccionador DC, descargador (DPS)."))
B.append(bullet("Protecciones AC: interruptor automático, diferencial, DPS AC."))
B.append(bullet("Puesta a tierra (SPT) de estructura y equipos."))
B.append(bullet("Medidor bidireccional (habilitado por la distribuidora)."))

B.append(para([run("6. Valorización de Componentes Físicos (CAPEX de equipos)", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para("Valores referenciales de mercado chileno 2025-2026 (IVA incluido), en CLP."))
mat = [
    ["Ítem", "Total CLP"],
    ["Panel solar 550 W monocristalino (x3)", "225.000"],
    ["Inversor híbrido 3 kW (MPPT, apto litio)", "650.000"],
    ["Batería LiFePO4 48V/100Ah (5,12 kWh)", "1.400.000"],
    ["Estructura de montaje de aluminio", "150.000"],
    ["Cableado solar, conectores MC4 y canalización", "120.000"],
    ["Tablero + protecciones DC/AC", "180.000"],
    ["Puesta a tierra (SPT)", "120.000"],
    ["Medidor bidireccional / adecuaciones", "80.000"],
    ["Materiales menores y ferretería", "80.000"],
    ["Subtotal materiales y equipos", ("3.005.000", True)],
]
B.append(table(mat, [6000, 3000]))
B.append(para([run("Referencias: ", bold=True),
               run("kits híbridos con inversor 3.000 W desde aprox. $990.000 (Solares Center Chile); paneles 550-585 W aprox. $60.000-90.000 c/u; baterías LiFePO4 48V/100Ah aprox. $1,2-1,8 MM.")]))

B.append(para([run("7. Valorización de Recursos Humanos", bold=True, color=AZUL, size=15)], spacing_after=80))
rrhh = [
    ["Ítem", "Total CLP"],
    ["Proyecto eléctrico + tramitación TE-4/SEC (ing. autorizado)", "350.000"],
    ["Instalación (instalador SEC clase D + ayudante, 2 pers. x 3 días)", "600.000"],
    ["Puesta en marcha, pruebas y capacitación", "150.000"],
    ["Subtotal recursos humanos", ("1.100.000", True)],
]
B.append(table(rrhh, [6000, 3000]))
B.append(para([run("7.1 Inversión total del proyecto (CAPEX)", bold=True, color=AZUL2, size=12)], spacing_after=60))
capex = [
    ["Concepto", "CLP"],
    ["Materiales y equipos", "3.005.000"],
    ["Recursos humanos", "1.100.000"],
    ["Contingencia (5 %)", "205.250"],
    ["INVERSIÓN TOTAL", ("4.310.250", True)],
]
B.append(table(capex, [6000, 3000]))

B.append(para([run("8. Indicadores de Evaluación (VAN, TIR, PRI)", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(para([run("8.1 Supuestos", bold=True, color=AZUL2, size=12)], spacing_after=60))
sup = [
    ["Parámetro", "Valor"],
    ["Horizonte de evaluación", "20 años"],
    ["Tasa de descuento", "8 %"],
    ["Precio energía evitada (autoconsumo)", "$230 /kWh"],
    ["Precio de inyección (net billing)", "$80 /kWh"],
    ["Escalación tarifaria real", "4 % anual"],
    ["Degradación FV", "0,7 % anual"],
    ["O&M (año 1)", "$50.000, +3 % anual"],
    ["Reemplazo de batería (año 10)", "$1.200.000"],
]
B.append(table(sup, [5400, 3600]))
B.append(para([run("8.2 Resultados - Escenario base (FV + batería)", bold=True, color=AZUL2, size=12)], spacing_after=60))
res = [
    ["Indicador", "Resultado", "Criterio", "Evaluación"],
    ["Beneficio neto año 1", "$225.485", "-", "-"],
    ["VAN (8 %)", ("-$2.032.020", True), "VAN > 0", "No conviene"],
    ["TIR", ("1,4 %", True), "TIR > 8 %", "Inferior a la tasa"],
    ["PRI simple", ("18,2 años", True), "< vida útil", "Muy largo"],
    ["PRI descontado", "> 20 años", "-", "No se recupera"],
]
B.append(table(res, [2600, 2200, 2000, 2200]))
B.append(para([run("8.3 Resultados - Escenario B de referencia (FV sin batería)", bold=True, color=AZUL2, size=12)], spacing_after=60))
resb = [
    ["Indicador", "Resultado"],
    ["CAPEX", "$2.710.250"],
    ["VAN (8 %)", "-$823.699"],
    ["TIR", "4,0 %"],
    ["PRI simple", "14,4 años"],
]
B.append(table(resb, [5400, 3600]))
B.append(para([run("8.4 Interpretación", bold=True, color=AZUL2, size=12)], spacing_after=60))
B.append(bullet("El VAN negativo en ambos escenarios indica que, con el consumo actual, el proyecto no genera valor económico al 8 %."))
B.append(bullet("La batería agrega aprox. $1,6 MM (compra + reemplazo) que no se recupera: destruye aprox. $1,2 MM de VAN adicional."))
B.append(bullet("El problema es de escala: el consumo es demasiado bajo para amortizar el costo fijo de un sistema con almacenamiento."))

B.append(para([run("9. Conclusiones y Recomendaciones", bold=True, color=AZUL, size=15)], spacing_after=80))
B.append(bullet("Recurso solar: viable (3,3 kWh/m²/día). Proyecto técnicamente factible y conforme a la normativa."))
B.append(bullet("Económicamente NO es rentable para el consumo actual: VAN negativo, TIR < tasa de descuento, PRI > 18 años."))
B.append(bullet("La batería es una inversión de respaldo/resiliencia, no de retorno. Si el objetivo es puramente económico, se recomienda omitirla."))
B.append(bullet("Para mejorar la viabilidad: evaluar si aumenta el consumo (calefacción eléctrica, VE); priorizar eficiencia energética; dimensionar la batería solo a cargas críticas; cotizar en firme con 3 proveedores certificados SEC."))

B.append(para([run("Documento a nivel de prefactibilidad. Los valores de equipos y mano de obra son referenciales de mercado y deben confirmarse con cotizaciones formales. El recurso solar debe validarse con el Explorador Solar del Ministerio de Energía para las coordenadas exactas y con visita técnica de sombreado.", color="7A7A7A", size=8)]))

body = "".join(B)
sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
        'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>')

document_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    f'<w:body>{body}{sect}</w:body></w:document>')

# ---- styles.xml ----
styles_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="es-CL"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/></w:style>'
    '</w:styles>')

# ---- numbering.xml (viñetas) ----
numbering_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
    '<w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="454" w:hanging="284"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>'
    '</w:lvl></w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    '</w:numbering>')

content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
    '</Types>')

rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>')

doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
    '</Relationships>')

OUT = "Informe_Prefactibilidad_FV_PuertoMontt.docx"
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/numbering.xml", numbering_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)

print(f"Generado {OUT}")
