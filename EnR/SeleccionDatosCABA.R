###Karina Laneri Junio de 2020####
###Leo base de datos Publica que me bajo de 
#### http://datos.salud.gob.ar/dataset/covid-19-casos-registrados-en-la-republica-argentina
#### y como es muy pesada selecciono los casos confirmados y sospechosos de CABA
#### los guardo  en un archivo ###########

##setwd(".")
### o directorio_del_repositorio_donde_estanlosdatos")
library(tidyverse)
library(dplyr)
library(readxl)
library(lubridate)
library(xts)
#Leo base de datos del MinSal que viene en formato .csv 
DatosPais<-read_csv("Covid19Casos.csv",col_names =TRUE)

DatosCABA<-DatosPais %>% filter(residencia_provincia_nombre == "CABA")

# DatosCABA<-DatosPais %>% filter((clasificacion_resumen =="Confirmado" | 
#                                    clasificacion_resumen =="Sospechoso"), 
#                                 residencia_provincia_nombre == "CABA", 
#                                 grepl("COMUNA",residencia_departamento_nombre)
# )

###grabo en el archivo CasosCABACompleto los Datos de CABA (todos, los confirmados y los que no etc.)
write.csv(DatosCABA,"CasosCABACompleto.csv",row.names = FALSE)
