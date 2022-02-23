library(geobr)
library(dplyr)
pacman::p_load(terra, spData)

#Filepath
filepath = "/Users/rafaellincoln/Desktop/PUC-Rio/Estatística/Trabalho_Chile_PUCRio/Assignment 4"  

# importando os dados 
# arquivo tif de cobertura vegetal
my_rast = rast(file.path(filepath,"brasil_coverage_2020.tif"))

# arquivos de municipalidades
mun = read_municipality(year =2020)
SP = mun %>% 
  filter(name_muni == "São Paulo") 

## crop and maks
cr = crop(my_rast, SP)
ms = mask(cr, vect(SP))

extrair_SP = terra::extract(my_rast,vect(SP))

pixels_SP = extrair_SP %>%
  group_by(brasil_coverage_2020) %>% 
  summarise(sum(brasil_coverage_2020))

area_sp = sum(pixels_SP$`sum(brasil_coverage_2020)`)

# Fração de cada classe em relação ao total
pixels_SP$fracao = pixels_SP$`sum(brasil_coverage_2020)`/area_sp

#Colocando a legenda na tabela

pixels_SP = pixels_SP %>% 
  rename(categoryValue = "brasil_coverage_2020") %>% 
  rename(area = "sum(brasil_coverage_2020)")

# Legenda mapbiomas

legend_mapbiomas = read.csv(file.path(filepath,"legend_table.csv"))

pixels_SP = left_join(pixels_SP,
                      legend_mapbiomas,
                      by = 'categoryValue',
                      na.rm = TRUE)

# Treemap of the fraction of the area
library(treemap)

treemap(pixels_SP,
        index = "Aggregated_class",
        vSize = "fracao")




