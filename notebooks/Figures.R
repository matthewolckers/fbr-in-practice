# Installs pacman ("package manager") if needed
if (!require("pacman")) install.packages("pacman")

# Use pacman to load add-on packages
pacman::p_load(pacman, rio, rstudioapi, ggplot2, svglite, ggthemes, gridExtra)



# Change the working directory
set_wd <- function() {
  library(rstudioapi) # make sure you have it installed
  current_path <- getActiveDocumentContext()$path
  setwd(dirname(current_path ))
  print( getwd() )
}
set_wd()


df <- import("../data/analysis.csv")


MyTheme_transparent <- theme(
  panel.background = element_rect(fill = "transparent"), # bg of the panel
  plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
  panel.grid.major = element_blank(), # get rid of major grid
  panel.grid.minor = element_blank(), # get rid of minor grid
  legend.background = element_rect(fill = "transparent"), # get rid of legend bg
  legend.box.background = element_rect(fill = "transparent"), # get rid of legend panel bg
  legend.key = element_rect(fill = "transparent", colour = NA), # get rid of key legend fill, and of the surrounding
  axis.text.y = element_blank(),
  axis.ticks.y = element_blank()
)

custom_theme_additions <- theme(axis.text.y = element_blank(),
                                    axis.ticks.y = element_blank())


p1 <- ggplot() +
  geom_histogram( aes(x = df[which(df$HodgeCBT_targets=="Included" & df$consumption<=2000),"consumption"], y = ..density..), binwidth = 50, fill="#bdbdbd" ) +
  geom_histogram( aes(x = df[which(df$tradCBT_targets=="Included" & df$consumption<=2000),"consumption"], y = -..density..), binwidth = 50,fill= "#000000") +
  xlab("") + ylab("Targeted") + xlim(c(0,2000)) + theme_minimal() +
  annotate(geom="text", x=1500, y=0.0015, label="Friend-based ranking", size=3) +
  annotate(geom="text", x=1500, y=-0.0015, label="Community-based targeting", size=3) +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank(),
        axis.text.y = element_blank(), axis.ticks.y = element_blank())

p1

#This actually save the plot in a image
#ggsave(file="included.svg", plot=p1, width=6, height=3, bg = "transparent")

p2 <- ggplot() +
  geom_histogram( aes(x = df[which(df$HodgeCBT_targets=="Excluded" & df$consumption<=2000),"consumption"], y = ..density..), binwidth = 50, fill="#bdbdbd" ) +
  geom_histogram( aes(x = df[which(df$tradCBT_targets=="Excluded" & df$consumption<=2000),"consumption"], y = -..density..), binwidth = 50, fill= "#000000") +
  xlab("Consumption") + ylab("Not targeted") + xlim(c(0,2000)) + theme_minimal() +
  annotate(geom="text", x=1500, y=0.0012, label="Friend-based ranking", size=3) +
  annotate(geom="text", x=1500, y=-0.0012, label="Community-based targeting", size=3) +
  theme(axis.ticks.y = element_blank(), axis.text.y = element_blank())

p2


#This actually save the plot in a image
# ggsave(file="excluded.svg", plot=p2, width=6, height=3, bg = "transparent")



p <- grid.arrange(p1, p2)
ggsave(plot=p, filename="../figures/fbr_vs_cbt.pdf", width=4, height=4)


# Histogram of inconsisitencies

dfh <- import("../data/analysis_hamlet_level.csv")

p3 <- ggplot() +
  geom_histogram( aes(x = dfh[,"local_incon"], y = ..density..), binwidth = 0.05, fill="#636363" ) +
  xlab("Cycle Ratio") + ylab("") + theme_minimal() + xlim(c(0,1)) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank())
p3

ggsave(file="../figures/cycle_ratio.pdf", plot=p3, width=4, height=2)
