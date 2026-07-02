# INFORME DE PREFACTIBILIDAD
## Sistema de Generación Fotovoltaica Residencial con Configuración Net Billing y Respaldo con Batería de Litio

**Ubicación:** Colono María Seidel 2504, Puerto Montt, Región de Los Lagos
**Cliente:** Cesar Barria Oyarzo — N° Cliente SAESA 10982361 — Medidor N° 3101198
**Tarifa actual:** BT1 (baja tensión residencial) — Potencia conectada 6,0 kW
**Distribuidora:** Sociedad Austral de Electricidad S.A. (SAESA)
**Fecha del informe:** Julio 2026
**Nivel:** Prefactibilidad (Clase 4 — precisión ±25 a ±30 %)

---

## 1. Resumen Ejecutivo

Se evalúa la instalación de un sistema fotovoltaico (FV) conectado a la red bajo modalidad
**Net Billing** (Ley 21.118), con **batería de litio (LiFePO4)** para autoconsumo nocturno y
respaldo, en una vivienda de Puerto Montt cuyo **consumo promedio es de 93,53 kWh/mes
(≈ 1.122 kWh/año)**.

| Parámetro | Valor |
|---|---|
| Potencia FV recomendada | **1,65 kWp** (3 paneles de 550 W) |
| Inversor | Híbrido 3 kW (apto litio, con MPPT) |
| Batería | LiFePO4 48 V / 100 Ah (**5,12 kWh**) |
| Generación estimada | **1.550 kWh/año** (138 % del consumo) |
| Inversión total (CAPEX) | **$ 4.310.250 CLP** |
| VAN (8 %, 20 años) | **–$ 2.032.020 CLP** |
| TIR | **1,4 %** |
| PRI (simple) | **18,2 años** |

> **Conclusión anticipada:** el proyecto es **técnicamente viable** y cumple la normativa
> vigente, pero **no es rentable financieramente** con el consumo actual. El bajo consumo
> del cliente y el alto costo de la batería producen un VAN negativo. La batería se
> justifica como **inversión de respaldo/resiliencia** (continuidad de servicio ante
> interrupciones frecuentes en la zona sur), no como una inversión de retorno económico.
> En el punto 8 se entregan recomendaciones para mejorar la viabilidad.

---

## 2. Objetivo y Alcance

Diseñar a nivel de prefactibilidad un sistema de generación en base al recurso solar,
dimensionando paneles, inversor, batería, materiales y protecciones; valorizar los
componentes físicos y los recursos humanos; y evaluar la inversión mediante los
indicadores VAN, TIR y PRI, conforme a la normativa chilena vigente y a las buenas
prácticas del mercado.

---

## 3. Análisis del Recurso Natural Renovable Disponible

### 3.1 Localización
- **Comuna:** Puerto Montt, Región de Los Lagos.
- **Latitud aproximada:** −41,47° ; **Longitud:** −72,94°.
- **Clima:** templado lluvioso oceánico, con **alta nubosidad y estacionalidad marcada**.

### 3.2 Recurso solar (Explorador Solar — Ministerio de Energía / metodología PVGIS)
Puerto Montt presenta uno de los recursos solares más bajos del país por su latitud y
nubosidad, pero **suficiente para un proyecto FV viable**, especialmente con net billing
que permite compensar el déficit invernal con excedentes estivales.

| Indicador | Valor estimado |
|---|---|
| Irradiación / HSP promedio anual (plano inclinado 35°) | **3,3 kWh/m²/día** |
| HSP verano (Dic–Ene) | ≈ 5,5 kWh/m²/día |
| HSP invierno (Jun–Jul) | ≈ 1,3 kWh/m²/día |
| Ángulo de inclinación óptimo | ≈ 35–40° (≈ latitud) |
| Orientación óptima | Norte franco (azimut 0°) |

### 3.3 Requerimientos mínimos de viabilidad
- **Irradiación mínima recomendada:** > 3,0 kWh/m²/día → **se cumple** (3,3).
- **Superficie de techo disponible y sombreado:** se requiere ≈ 10 m² con orientación
  norte y libre de sombras (chimeneas, árboles, edificaciones). *A verificar en visita técnica.*
- **Estructura de soporte:** techo con capacidad estructural para ≈ 15 kg/panel.

> **Veredicto del recurso:** VIABLE. El recurso solar de Puerto Montt es modesto pero
> suficiente. La fuerte estacionalidad hace **recomendable la modalidad net billing** para
> "banquear" excedentes de verano y usarlos en invierno.

---

## 4. Determinación del Consumo Energético (base de dimensionamiento)

Datos obtenidos de la boleta electrónica SAESA N° 76633459.

### 4.1 Consumo histórico (últimos 13 meses)

| Mes | kWh | Mes | kWh |
|---|---|---|---|
| May-25 | 76 | Dic-25 | 120 |
| Jun-25 | 106 | Ene-26 | **134** (máx) |
| Jul-25 | 93 | Feb-26 | 116 |
| Ago-25 | **56** (mín) | Mar-26 | 112 |
| Sep-25 | 91 | Abr-26 | 88 |
| Oct-25 | 85 | May-26 | 87 |
| Nov-25 | 61 | | |

### 4.2 Parámetros de diseño

| Parámetro | Valor |
|---|---|
| Consumo promedio mensual (boleta) | **93,53 kWh/mes** |
| **Consumo anual de diseño** | **1.122 kWh/año** |
| Consumo diario promedio | **≈ 3,1 kWh/día** |
| Mes de mayor consumo | Enero (134 kWh — verano) |
| Mes de menor consumo | Agosto (56 kWh) |
| Costo variable de energía (referencia boleta) | ≈ $ 222–255 /kWh |

> **Observación clave:** el consumo es **bajo** y presenta un patrón inverso al recurso
> solar en parte del año (alto consumo en verano por refrigeración/iluminación prolongada,
> pero también picos invernales). El sistema se dimensiona sobre el promedio anual y se
> apoya en net billing + batería para el desfase horario diario.

---

## 5. Diseño de Prefactibilidad del Sistema

### 5.1 Normativa y marco regulatorio aplicable
- **Ley 21.118 (Net Billing / Generación Distribuida):** permite a clientes regulados
  autogenerar con ERNC e inyectar excedentes, con capacidad de hasta 300 kW.
- **NCh Elec. 4/2003:** instalaciones eléctricas de consumo en baja tensión.
- **Pliego técnico normativo RGR N°02 (SEC)** para generación distribuida.
- **Declaración TE-4 ante la SEC**, ejecutada por instalador eléctrico autorizado.
- **Solicitud de conexión y medidor bidireccional** ante la distribuidora (SAESA).
- Equipos con **certificación SEC** obligatoria (paneles, inversor, protecciones).

### 5.2 Dimensionamiento del generador fotovoltaico

```
Rendimiento específico (yield) = HSP × 365 × PR
                               = 3,3 kWh/m²/día × 365 × 0,78
                               = 940 kWh/kWp/año

Potencia teórica (100 % consumo) = Consumo anual / yield
                                 = 1.122 / 940 = 1,19 kWp
```

Se adopta **1,65 kWp (3 paneles de 550 W)** para cubrir:
- Pérdidas de ciclo de la batería (round-trip ≈ 90 %),
- Degradación de los paneles (0,7 %/año), y
- La estacionalidad invernal (déficit compensado por excedentes de verano).

```
Generación anual estimada = 1,65 kWp × 940 = 1.550 kWh/año  (138 % del consumo)
```

### 5.3 Inversor
- **Inversor híbrido monofásico 3 kW**, con MPPT integrado, gestión de batería de litio
  y función de respaldo (backup) ante corte de red.
- Ratio DC/AC conservador (permite ampliación futura a más paneles).

### 5.4 Batería de litio
```
Batería LiFePO4 48 V / 100 Ah = 5,12 kWh nominales
Energía útil (DoD 90 %)       = 4,61 kWh
Autonomía ≈ 4,61 / 3,1 kWh/día ≈ 1,5 días de consumo
```
- Química **LiFePO4** por seguridad, vida útil (> 6.000 ciclos) y tolerancia a clima frío.
- Función: **desplazar el autoconsumo al horario nocturno** y dar **respaldo** ante cortes.

### 5.5 Balance energético anual (Net Billing)

| Flujo | kWh/año |
|---|---|
| Generación FV | 1.550 |
| Autoconsumo (directo + batería) | 1.010 |
| Importación desde la red | 112 |
| **Excedente inyectado a la red** | **540** |

### 5.6 Materiales y protecciones (buenas prácticas / NCh Elec 4/2003)
- Estructura de montaje de aluminio anodizado + tornillería inoxidable.
- Cable solar 4–6 mm² (DC), conectores MC4.
- Protecciones DC: fusibles gPV, seccionador DC, descargador de sobretensión (DPS).
- Protecciones AC: interruptor automático, diferencial, DPS AC.
- **Puesta a tierra (SPT)** de estructura y equipos.
- Medidor bidireccional (provisto/habilitado por la distribuidora).

---

## 6. Valorización de Componentes Físicos (CAPEX de equipos)

Valores referenciales de mercado chileno 2025–2026 (IVA incluido), en CLP.

| Ítem | Cantidad | Total CLP |
|---|---|---|
| Panel solar 550 W monocristalino | 3 | 225.000 |
| Inversor híbrido 3 kW (MPPT, apto litio) | 1 | 650.000 |
| Batería LiFePO4 48 V/100 Ah (5,12 kWh) | 1 | 1.400.000 |
| Estructura de montaje de aluminio | 1 | 150.000 |
| Cableado solar, conectores MC4 y canalización | — | 120.000 |
| Tablero + protecciones DC/AC (fusibles, breakers, DPS, diferencial) | — | 180.000 |
| Puesta a tierra (SPT) | — | 120.000 |
| Medidor bidireccional / adecuaciones | — | 80.000 |
| Materiales menores y ferretería | — | 80.000 |
| **Subtotal materiales y equipos** | | **3.005.000** |

*Referencias de cotización:* kits híbridos con inversor 3.000 W desde ≈ $990.000
(Solares Center Chile); paneles monocristalinos 550–585 W ≈ $60.000–90.000 c/u;
baterías LiFePO4 48 V/100 Ah ≈ $1,2–1,8 MM.

---

## 7. Valorización de los Recursos Humanos (trabajo técnico)

| Ítem | Detalle | Total CLP |
|---|---|---|
| Proyecto eléctrico + tramitación TE-4/SEC | Ingeniero/instalador autorizado | 350.000 |
| Instalación | Instalador SEC clase D + ayudante, 2 pers. × 3 días | 600.000 |
| Puesta en marcha, pruebas y capacitación | Configuración inversor/batería | 150.000 |
| **Subtotal recursos humanos** | | **1.100.000** |

### 7.1 Inversión total del proyecto (CAPEX)

| Concepto | CLP |
|---|---|
| Materiales y equipos | 3.005.000 |
| Recursos humanos | 1.100.000 |
| Contingencia (5 %) | 205.250 |
| **INVERSIÓN TOTAL** | **4.310.250** |

---

## 8. Indicadores de Evaluación de Proyectos (VAN, TIR, PRI)

### 8.1 Supuestos de la evaluación

| Parámetro | Valor |
|---|---|
| Horizonte de evaluación | 20 años |
| Tasa de descuento | 8 % |
| Precio energía evitada (autoconsumo) | $ 230 /kWh |
| Precio de inyección (net billing) | $ 80 /kWh |
| Escalación tarifaria real | 4 % anual |
| Degradación FV | 0,7 % anual |
| O&M (año 1) | $ 50.000, +3 % anual |
| Reemplazo de batería (año 10) | $ 1.200.000 |

### 8.2 Resultados — Escenario base (FV + batería)

| Indicador | Resultado | Criterio | Evaluación |
|---|---|---|---|
| Beneficio neto año 1 | $ 225.485 | — | — |
| **VAN (8 %)** | **–$ 2.032.020** | VAN > 0 | ❌ No conviene |
| **TIR** | **1,4 %** | TIR > 8 % | ❌ Inferior a la tasa |
| **PRI simple** | **18,2 años** | < vida útil | ⚠️ Muy largo |
| PRI descontado | > 20 años | — | ❌ No se recupera |

### 8.3 Resultados — Escenario B de referencia (FV **sin** batería)

| Indicador | Resultado |
|---|---|
| CAPEX | $ 2.710.250 |
| VAN (8 %) | –$ 823.699 |
| TIR | 4,0 % |
| PRI simple | 14,4 años |

### 8.4 Interpretación
- El **VAN negativo** en ambos escenarios indica que, con el consumo actual
  (≈ 1.122 kWh/año), el proyecto **no genera valor económico** al costo de capital del 8 %.
- La **batería agrega ≈ $1,6 MM de inversión** (compra + reemplazo) que **no se recupera**
  con el ahorro marginal en un consumo tan bajo: destruye ≈ $1,2 MM de VAN adicional.
- El principal problema es de **escala**: el consumo es demasiado bajo para amortizar el
  costo fijo de un sistema con almacenamiento.

---

## 9. Conclusiones y Recomendaciones

1. **Recurso solar:** viable (3,3 kWh/m²/día). El proyecto es **técnicamente factible** y
   cumple la normativa (Ley 21.118, NCh Elec 4/2003, declaración TE-4 SEC).
2. **Económicamente NO es rentable** para el consumo actual: VAN negativo, TIR < tasa de
   descuento y PRI superior a 18 años.
3. **La batería** debe entenderse como inversión de **respaldo/resiliencia** (continuidad
   ante interrupciones de suministro, frecuentes en la zona), **no** como inversión de
   retorno. Si el objetivo es puramente económico, se recomienda **omitir la batería**.
4. **Recomendaciones para mejorar la viabilidad:**
   - Evaluar el sistema solo si aumenta el consumo (p. ej., electrificación de calefacción
     o vehículo eléctrico), lo que mejora sustancialmente el autoconsumo y el VAN.
   - Priorizar primero **eficiencia energética** (iluminación LED, buen aislamiento).
   - Si se requiere respaldo, dimensionar la batería a lo mínimo necesario para las
     cargas críticas, no para autonomía de días.
   - Cotizar en firme con al menos 3 proveedores certificados SEC antes de la factibilidad.

---

## Anexos
- **Anexo A:** `calculos_fv.py` — script reproducible con todos los cálculos (consumo,
  dimensionamiento, balance energético y evaluación económica VAN/TIR/PRI).
- **Anexo B:** `resultados_calculos.txt` — salida numérica completa del modelo.

*Documento a nivel de prefactibilidad. Los valores de equipos y mano de obra son
referenciales de mercado y deben confirmarse con cotizaciones formales. El recurso solar
debe validarse con el Explorador Solar del Ministerio de Energía para las coordenadas
exactas y con visita técnica de sombreado.*
