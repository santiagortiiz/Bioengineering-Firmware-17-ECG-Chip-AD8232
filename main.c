/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include "project.h"
#include <stdio.h>                                      // Standard Input-Output

typedef struct Variables{
    uint16 ADC:16;
    uint16 Bandera_Rx:1;
} Variable;
Variable variable;

char ADC_en_ASCII[5];

void sensar(void);

CY_ISR_PROTO(UART_Rx);
CY_ISR_PROTO(conexion_LO_mas);
CY_ISR_PROTO(conexion_LO_menos);

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    /***Inicializacion de Interrupciones***/
    isr_RX_StartEx(UART_Rx);
    isr_LO_mas_StartEx(conexion_LO_mas);
    isr_LO_menos_StartEx(conexion_LO_menos);
    
    /***Inicializacion de Componentes***/
    ADC_Start();
    UART_Start();
    LCD_Start();
    
    LCD_Position(0,0);
    LCD_PrintString("Conexion Electrodos");
    variable.Bandera_Rx = 0;
    
    for(;;)
    {
        if (variable.Bandera_Rx == 1){                  // Sí la bandera Rx esta activa, entonces se grafica el ECG 
            sensar();                           
            sprintf(ADC_en_ASCII, "%u", variable.ADC);  // Conversión de número a ASCII: ADC_en_ASCII <--  str(variable.ADC)                     
                    
            UART_PutString(ADC_en_ASCII);               // Envia el valor de ADC por Comunicacion Serial
            UART_PutCRLF(' ');
            CyDelay(1);
        }
        
    }
}

void sensar(void){                                      // Cuantiza el voltaje del ECG en un valor digital
    ADC_StartConvert();
    ADC_IsEndConversion(ADC_WAIT_FOR_RESULT);
    variable.ADC = ADC_GetResult16();
}

CY_ISR(conexion_LO_mas){
    if (LO_mas_Read() == 1){                            // Sí el electrodo Izquierdo que esta conectado
        LCD_Position(1,0);                              // a IN+ se desconecta, entonces LOD+ se pone
        LCD_PrintString("Electrodo IZQ suelto");        // en alto y se advierte que esta suelto, de 
    }                                                   // lo contrario, LOD+ estará en bajo y se
    else {                                              // notifica que el electrodo esta "OK"
        LCD_Position(1,0);
        LCD_PrintString("Electrodo IZQ OK    ");
    }
}

CY_ISR(conexion_LO_menos){                              // Sí el electrodo Derecho que esta conectado
    if (LO_menos_Read() == 1){                          // a IN- se desconecta, entonces LOD- se pone
        LCD_Position(2,0);                              // en alto y se advierte que esta suelto, de 
        LCD_PrintString("Electrodo DER suelto");        // lo contrario, LOD- estará en bajo y se
    }                                                   // notifica que el electrodo esta "OK"
    else {
        LCD_Position(2,0);
        LCD_PrintString("Electrodo DER OK    ");
    }
}

CY_ISR(UART_Rx){                                        // Al enviar un dato al Psoc por Comun. Serial
    variable.Bandera_Rx = ~variable.Bandera_Rx;         // se cambia el estado de la bandera Rx, el 
}                                                       // cual se alterna entre 0 y 1

/* [] END OF FILE */
