#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cálculos de prefactibilidad - Sistema Fotovoltaico Net Billing con batería de litio
Cliente: Cesar Barria Oyarzo | Puerto Montt | Tarifa BT1 | Distribuidora SAESA
Base: Boleta electrónica N° 76633459 (período 23/04/2026 - 22/05/2026)

Este script reproduce todos los cálculos del informe:
  1. Análisis de consumo (boleta)
  2. Recurso solar y dimensionamiento del generador FV
  3. Dimensionamiento de inversor y batería
  4. Balance energético anual con net billing
  5. Evaluación económica: VAN, TIR, PRI
"""

# =====================================================================
# 1. CONSUMO ENERGÉTICO (extraído de la boleta SAESA)
# =====================================================================
# Consumo mensual de los últimos 13 meses [kWh] (gráfico de la boleta)
consumo_mensual = {
    "May-25": 76, "Jun-25": 106, "Jul-25": 93, "Ago-25": 56, "Sep-25": 91,
    "Oct-25": 85, "Nov-25": 61, "Dic-25": 120, "Ene-26": 134, "Feb-26": 116,
    "Mar-26": 112, "Abr-26": 88, "May-26": 87,
}
# Consumo de los 12 meses móviles (Jun-25 a May-26)
ultimos_12 = list(consumo_mensual.values())[1:]
consumo_anual = sum(ultimos_12)                      # kWh/año (suma real 12 meses)
promedio_boleta = 93.53                               # kWh/mes (dato oficial boleta)
consumo_anual_oficial = round(promedio_boleta * 12)   # kWh/año según promedio boleta
consumo_diario = consumo_anual / 365.0
consumo_max_mes = max(ultimos_12)
consumo_min_mes = min(ultimos_12)

print("=" * 68)
print("1. ANÁLISIS DE CONSUMO")
print("=" * 68)
print(f"Consumo anual (suma 12 meses móviles)   : {consumo_anual} kWh/año")
print(f"Consumo anual (prom. boleta 93,53x12)   : {consumo_anual_oficial} kWh/año")
print(f"Consumo diario promedio                 : {consumo_diario:.2f} kWh/día")
print(f"Mes de mayor consumo (Ene)              : {consumo_max_mes} kWh")
print(f"Mes de menor consumo (Ago)              : {consumo_min_mes} kWh")

# Se adopta como consumo de diseño el promedio oficial de la boleta
CONSUMO_DISENO = consumo_anual_oficial  # 1122 kWh/año

# =====================================================================
# 2. RECURSO SOLAR Y DIMENSIONAMIENTO DEL GENERADOR FV
# =====================================================================
# Recurso solar Puerto Montt (lat -41,47°). Fuente: Explorador Solar (Min. Energía)
# HSP = Horas Solar Pico sobre plano inclinado ~35° (equivalente a kWh/m2/día)
HSP_anual_prom = 3.3          # kWh/m2/día promedio anual (plano inclinado)
HSP_verano = 5.5              # kWh/m2/día (Dic-Ene)
HSP_invierno = 1.3            # kWh/m2/día (Jun-Jul)

# Rendimiento específico (Performance Ratio incluido) para Puerto Montt
PR = 0.78                     # Performance Ratio (pérdidas por temp, cableado, inversor, suciedad)
yield_especifico = HSP_anual_prom * 365 * PR   # kWh generados por kWp instalado al año
print("\n" + "=" * 68)
print("2. RECURSO SOLAR Y DIMENSIONAMIENTO FV")
print("=" * 68)
print(f"HSP promedio anual (plano 35°)          : {HSP_anual_prom} kWh/m2/día")
print(f"Performance Ratio (PR)                  : {PR}")
print(f"Rendimiento específico (yield)          : {yield_especifico:.0f} kWh/kWp/año")

# Potencia FV teórica para cubrir el 100% del consumo anual
potencia_teorica = CONSUMO_DISENO / yield_especifico
print(f"Potencia FV teórica (100% consumo)      : {potencia_teorica:.2f} kWp")

# Selección comercial de paneles
pot_panel = 550               # W por panel (monocristalino)
# Se adopta un pequeño sobredimensionamiento para cubrir pérdidas de
# batería (round-trip), degradación y estacionalidad -> 3 paneles
n_paneles = 3
potencia_instalada = n_paneles * pot_panel / 1000.0   # kWp
generacion_anual = potencia_instalada * yield_especifico
print(f"Paneles seleccionados                   : {n_paneles} x {pot_panel} W")
print(f"Potencia instalada                      : {potencia_instalada:.2f} kWp")
print(f"Generación anual estimada (año 1)       : {generacion_anual:.0f} kWh/año")
print(f"Cobertura vs consumo                    : {generacion_anual/CONSUMO_DISENO*100:.0f} %")

# =====================================================================
# 3. DIMENSIONAMIENTO DE INVERSOR Y BATERÍA
# =====================================================================
# Inversor híbrido: se recomienda ratio DC/AC entre 1,0 y 1,3
pot_inversor = 3.0            # kW (híbrido, apto litio, con MPPT)
ratio_dc_ac = potencia_instalada / pot_inversor
# Batería de litio (LiFePO4) para autoconsumo nocturno + respaldo
bateria_kwh_nominal = 5.12    # 48V x 100Ah
DoD = 0.90                    # profundidad de descarga LiFePO4
bateria_util = bateria_kwh_nominal * DoD
autonomia = bateria_util / consumo_diario
print("\n" + "=" * 68)
print("3. INVERSOR Y BATERÍA")
print("=" * 68)
print(f"Inversor híbrido                        : {pot_inversor:.1f} kW")
print(f"Ratio DC/AC                             : {ratio_dc_ac:.2f}")
print(f"Batería LiFePO4 nominal                 : {bateria_kwh_nominal:.2f} kWh (48V/100Ah)")
print(f"Energía útil batería (DoD {DoD*100:.0f}%)        : {bateria_util:.2f} kWh")
print(f"Autonomía aprox. (sin sol)              : {autonomia:.1f} días de consumo")

# =====================================================================
# 4. BALANCE ENERGÉTICO ANUAL - NET BILLING
# =====================================================================
# Con batería, la fracción de consumo cubierta directamente por FV es alta
frac_autoconsumo = 0.90       # % del consumo cubierto por FV+batería
energia_autoconsumida = CONSUMO_DISENO * frac_autoconsumo
energia_desde_red = CONSUMO_DISENO - energia_autoconsumida
energia_inyectada = generacion_anual - energia_autoconsumida
print("\n" + "=" * 68)
print("4. BALANCE ENERGÉTICO ANUAL (NET BILLING)")
print("=" * 68)
print(f"Energía autoconsumida (FV+batería)      : {energia_autoconsumida:.0f} kWh/año")
print(f"Energía importada de la red             : {energia_desde_red:.0f} kWh/año")
print(f"Energía inyectada (excedente)           : {energia_inyectada:.0f} kWh/año")

# =====================================================================
# 5. VALORIZACIÓN (CAPEX): materiales + recursos humanos
# =====================================================================
materiales = {
    "Paneles 550W monocristalino (x3)":        3 * 75000,
    "Inversor híbrido 3 kW (MPPT, apto litio)": 650000,
    "Batería LiFePO4 48V 100Ah (5,12 kWh)":     1400000,
    "Estructura de montaje aluminio":           150000,
    "Cableado solar, MC4 y canalización":       120000,
    "Tablero + protecciones DC/AC (fusibles, breakers, DPS, diferencial)": 180000,
    "Puesta a tierra (SPT)":                    120000,
    "Medidor bidireccional / adecuaciones":     80000,
    "Materiales menores y ferretería":          80000,
}
recursos_humanos = {
    "Proyecto eléctrico + tramitación TE4/SEC (ing. autorizado)": 350000,
    "Instalación (instalador SEC clase D, 2 pers. x 3 días)":     600000,
    "Puesta en marcha, pruebas y capacitación":                   150000,
}
subtotal_materiales = sum(materiales.values())
subtotal_rrhh = sum(recursos_humanos.values())
contingencia = round((subtotal_materiales + subtotal_rrhh) * 0.05)
CAPEX = subtotal_materiales + subtotal_rrhh + contingencia
costo_bateria = materiales["Batería LiFePO4 48V 100Ah (5,12 kWh)"]

print("\n" + "=" * 68)
print("5. VALORIZACIÓN (CAPEX) [CLP]")
print("=" * 68)
print("-- Materiales y equipos --")
for k, v in materiales.items():
    print(f"   {k:<58}: $ {v:>10,.0f}")
print(f"   {'SUBTOTAL MATERIALES':<58}: $ {subtotal_materiales:>10,.0f}")
print("-- Recursos humanos --")
for k, v in recursos_humanos.items():
    print(f"   {k:<58}: $ {v:>10,.0f}")
print(f"   {'SUBTOTAL RECURSOS HUMANOS':<58}: $ {subtotal_rrhh:>10,.0f}")
print(f"   {'Contingencia (5%)':<58}: $ {contingencia:>10,.0f}")
print(f"   {'INVERSIÓN TOTAL (CAPEX)':<58}: $ {CAPEX:>10,.0f}")

# =====================================================================
# 6. EVALUACIÓN ECONÓMICA: VAN, TIR, PRI
# =====================================================================
precio_red = 230        # CLP/kWh evitado (autoconsumo, IVA incl.)
precio_inyeccion = 80   # CLP/kWh (valorización net billing)
escalacion = 0.04       # alza anual real de tarifa eléctrica
degradacion = 0.007     # pérdida anual de generación FV
oym_anual = 50000       # O&M año 1 (limpieza, inspección)
oym_escal = 0.03
tasa_descuento = 0.08   # tasa de descuento
horizonte = 20          # años
reemplazo_bateria_ano = 10
costo_reemplazo_bateria = 1200000  # menor por baja de precios

def beneficio_anual(anio):
    """Ahorro + ingreso por inyección - O&M, en el año dado (año 1..N)."""
    factor_precio = (1 + escalacion) ** (anio - 1)
    factor_gen = (1 - degradacion) ** (anio - 1)
    autoc = energia_autoconsumida * factor_gen
    iny = energia_inyectada * factor_gen
    ahorro = autoc * precio_red * factor_precio
    ingreso = iny * precio_inyeccion * factor_precio
    oym = oym_anual * (1 + oym_escal) ** (anio - 1)
    return ahorro + ingreso - oym

# Flujo de caja
flujos = [-CAPEX]
for anio in range(1, horizonte + 1):
    fc = beneficio_anual(anio)
    if anio == reemplazo_bateria_ano:
        fc -= costo_reemplazo_bateria
    flujos.append(fc)

# VAN
def van(tasa, flujos):
    return sum(fc / (1 + tasa) ** i for i, fc in enumerate(flujos))

VAN = van(tasa_descuento, flujos)

# TIR (bisección)
def tir(flujos, low=-0.9, high=1.0, tol=1e-6):
    f_low = van(low, flujos)
    f_high = van(high, flujos)
    if f_low * f_high > 0:
        return None  # no hay cambio de signo en el rango
    for _ in range(200):
        mid = (low + high) / 2
        f_mid = van(mid, flujos)
        if abs(f_mid) < tol:
            return mid
        if f_low * f_mid < 0:
            high = mid
        else:
            low = mid
            f_low = f_mid
    return (low + high) / 2

TIR = tir(flujos)

# PRI simple (no descontado) y descontado
acum = 0
pri_simple = None
for i in range(1, len(flujos)):
    prev = acum
    acum += flujos[i]
    if prev < CAPEX <= acum:  # cruce
        frac = (CAPEX - prev) / flujos[i]
        pri_simple = (i - 1) + frac
        break

acum_desc = 0
pri_desc = None
inv = -flujos[0]
for i in range(1, len(flujos)):
    prev = acum_desc
    acum_desc += flujos[i] / (1 + tasa_descuento) ** i
    if prev < inv <= acum_desc:
        frac = (inv - prev) / (flujos[i] / (1 + tasa_descuento) ** i)
        pri_desc = (i - 1) + frac
        break

print("\n" + "=" * 68)
print("6. EVALUACIÓN ECONÓMICA (net billing con batería)")
print("=" * 68)
print(f"Precio energía evitada (autoconsumo)    : $ {precio_red}/kWh")
print(f"Precio inyección (net billing)          : $ {precio_inyeccion}/kWh")
print(f"Escalación tarifaria                    : {escalacion*100:.0f}% anual")
print(f"Tasa de descuento                       : {tasa_descuento*100:.0f}%")
print(f"Horizonte                               : {horizonte} años")
print(f"Beneficio neto año 1                    : $ {beneficio_anual(1):,.0f}")
print(f"VAN (8%)                                : $ {VAN:,.0f}")
print(f"TIR                                     : {TIR*100:.1f} %" if TIR else "TIR: n/a")
print(f"PRI simple                              : {pri_simple:.1f} años" if pri_simple else "PRI simple: > horizonte")
print(f"PRI descontado                          : {pri_desc:.1f} años" if pri_desc else "PRI descontado: > horizonte")

# --------- Escenario B: FV SIN batería (referencia) -----------------
CAPEX_sin_bat = CAPEX - costo_bateria - 200000  # sin batería y con inversor on-grid más barato
# Sin batería, autoconsumo instantáneo menor (día): ~45% del consumo
frac_autoconsumo_sb = 0.45
autoc_sb = CONSUMO_DISENO * frac_autoconsumo_sb
iny_sb = generacion_anual - autoc_sb

def beneficio_sb(anio):
    fp = (1 + escalacion) ** (anio - 1)
    fg = (1 - degradacion) ** (anio - 1)
    return (autoc_sb * fg * precio_red * fp + iny_sb * fg * precio_inyeccion * fp
            - oym_anual * (1 + oym_escal) ** (anio - 1))

flujos_sb = [-CAPEX_sin_bat] + [beneficio_sb(a) for a in range(1, horizonte + 1)]
VAN_sb = van(tasa_descuento, flujos_sb)
TIR_sb = tir(flujos_sb)
acum = 0; pri_sb = None
for i in range(1, len(flujos_sb)):
    prev = acum; acum += flujos_sb[i]
    if prev < CAPEX_sin_bat <= acum:
        pri_sb = (i - 1) + (CAPEX_sin_bat - prev) / flujos_sb[i]; break

print("\n" + "-" * 68)
print("ESCENARIO B (referencia): FV SIN batería")
print("-" * 68)
print(f"CAPEX                                   : $ {CAPEX_sin_bat:,.0f}")
print(f"Beneficio neto año 1                    : $ {beneficio_sb(1):,.0f}")
print(f"VAN (8%)                                : $ {VAN_sb:,.0f}")
print(f"TIR                                     : {TIR_sb*100:.1f} %" if TIR_sb else "TIR: n/a")
print(f"PRI simple                              : {pri_sb:.1f} años" if pri_sb else "PRI: > horizonte")

print("\n[Cálculos completados]")
