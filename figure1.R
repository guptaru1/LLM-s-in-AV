library(ggplot2)
library(reshape2)
library(dplyr)
library(tidyr)
library(AER)
library(sandwich)
library(multiwayvcov)
library(data.table)

source("chat_bot_shared.R")

# Loading data as a data.table
# e.g., GPT-3.5
#profiles <- fread(input="merged_file_gemma-2b-it.csv")
profiles <- fread(input="llm_model_scenarios.csv")
profiles <- PreprocessProfiles(profiles)

# Compute ACME values
Coeffs.main <- GetMainEffectSizes(profiles,T,11)
plotdata.main <- GetPlotData(Coeffs.main,T,11)

# Compute additional ACME values
#Coeffs.util <- GetMainEffectSizes.Util(profiles)
#plotdata.util <- GetPlotData.Util(Coeffs.util)

## plot and save
#PlotAndSave(plotdata.main, T, "MainChangePr", plotdata.util)

PlotAndSaveTesting(plotdata.main,plotdata.util )