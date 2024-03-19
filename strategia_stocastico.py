//@version=5
//------------------------------------------------------- CONFIGURACION GESTION CAPITAL--------------------------------------------------
strategy("My Stochastic Strategy v2 with Time Filter",
         overlay=true,
         initial_capital=10000, // Establece el capital inicial X unidades de la divisa de tu cuenta
         commission_type="percent", // Tipo de comisión como porcentaje
         pyramiding=10, // Esto permite hacer entradas adicionales en la misma dirección mientras una posición está abierta. 
         commission_value=0.01) // Comisión del 0.01% por orden


// Configuracion del size de compra
currentPrice = close // El precio actual del activo
amount_to_invest = 500 
qty_to_buy = amount_to_invest / currentPrice // Calcula la cantidad a comprar con 'amount_to_invest'


//------------------------------------------------------------------------------------------------------------------
//--------------------------------------------------- EMAS ---------------------------------------------------------
//------------------------------------------------------------------------------------------------------------------
longEmaPeriod = 55
shortEmaPeriod = 10


// Cálculo de las EMAs
longEma = ta.ema(close, longEmaPeriod)
shortEma = ta.ema(close, shortEmaPeriod)


// Dibujar las EMAs en el gráfico
plot(longEma, color=color.rgb(255, 174, 0), title="EMA 55", linewidth=2)
plot(shortEma, color=color.rgb(0, 119, 255), title="EMA 10", linewidth=2)


// -----------------------------------------------------------------------------------------------------------
// -----------------------------------Configuracion ----------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------




// Entradas para habilitar o deshabilitar operaciones largas y cortas
allowLongs = true
allowShorts = false


// Periodo de tiempo activo para la estrategia
start_date = timestamp("2023-01-01 00:00 +0000")
end_date = timestamp("2024-12-01 12:00 +0000")


tendencia = "alcista"   // tendencia puede ser "alcista", "bajista", "lateral"
temporalidad = "1h"       // temporalidad puede ser "1m", "5m", "30m", "1h", "4m", "D", "S", "M".


//---------------------------------------------------------------------------------------------------------
//----------------------------------------------- Script --------------------------------------------------
//---------------------------------------------------------------------------------------------------------


// Inicializa variables para niveles de sobrecompra y sobrevendido
float overbought_level = na
float oversold_level = na


// Ajusta los niveles de sobre compra y sobreventa basándote en la tendencia
if tendencia == "alcista"
    if temporalidad == "1m"
        overbought_level := 80
        oversold_level := 50
    if temporalidad == "1h"
        overbought_level := 80
        oversold_level := 50
else if tendencia == "bajista"
    if temporalidad == "1m"
        overbought_level := 60
        oversold_level := 30
    if temporalidad == "1h"
        overbought_level := 50
        oversold_level := 35    
else if tendencia == "lateral"
    if temporalidad == "1h"
        overbought_level := 53
        oversold_level := 38
else
    overbought_level := 80
    oversold_level := 30


// Define el periodo del estocástico
k_period = input(14, title="K Period")
d_period = input(3, title="D Period")
smooth = input(3, title="Smoothing")


// Verifica si el tiempo actual está dentro del rango especificado
time_filter = (time >= start_date) and (time <= end_date)


// Calcula el estocástico
sto_k = ta.sma(ta.stoch(close, high, low, k_period), smooth)
sto_d = ta.sma(sto_k, d_period)


// Condiciones para entrar y salir de una operación, incluyendo el filtro de tiempo
enterLong = ta.crossover(sto_k, sto_d) and sto_k < oversold_level and time_filter and (close > longEma)
exitLong = (ta.crossunder(sto_k, sto_d) and (sto_k > overbought_level) and time_filter) 
enterShort = ta.crossunder(sto_k, sto_d) and sto_k > overbought_level and time_filter and (close < longEma)
exitShort = (ta.crossover(sto_k, sto_d) and (sto_k < oversold_level) and time_filter) 


// Visualización mejorada
bgcolor(sto_k < oversold_level ? color.new(color.green, 90) : na)
bgcolor(sto_k > overbought_level ? color.new(color.red, 90) : na)
plotshape(series=enterLong, location=location.belowbar, color=color.green, style=shape.labelup, text="Buy")
plotshape(series=enterShort, location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell")


// Define una variable que será true solo en 'start_date'
start_date_highlight = (time == start_date)


// Usa esa variable como condición para 'bgcolor()'
bgcolor(start_date_highlight ? color.new(#ffffff, 36) : na, title="Start Date Highlight")

// Ejecutar las órdenes de la estrategia
if (allowLongs and enterLong)
    strategy.entry("Long", strategy.long, qty=qty_to_buy)
if (allowLongs and exitLong)
    strategy.close("Long")
if (allowShorts and enterShort)
    strategy.entry("Short", strategy.short, qty=qty_to_buy)
if (allowShorts and exitShort)
    strategy.close("Short")
