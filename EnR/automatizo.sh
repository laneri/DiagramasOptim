###Este es un archivo bash que me automatiza todos los pasos para obtener los diagramas de riesgo
###uso: 
##> bash automatizo.sh

###### pongo todos los archivos en el directorio del repositorio github
#cd /path_directorio_con_estos_archivos
##borro file viejo
#rm Covid19Casos.csv
#bajo la nueva base de datos del Ministerio
#wget https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv
#### corro el programa que me selecciona los datos de CABA
R CMD BATCH SeleccionDatosCABA.R

### corro el programa que me calcula los ejes del diagrama de riesgo a partir de los datos seleccionados
R CMD BATCH DiagramaRiesgoCABA.R

###### subo al repositorio los archivos Riesgo y datos_crudos
git pull
git add Riesgo* datos_crudos
git commit -m "actualizacion"
git push

#####hago graficos 
###corro script python que me lee el archivo Riesgo y hace el grafico etc...

