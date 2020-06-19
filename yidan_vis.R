solo_data <- read.csv("solo.csv")
head(solo_data)

freq_per_player <- data.frame(table(solo_data$player_id))
head(freq_per_player)

# install.packages("ggplot2")
library(ggplot2)
ggplot(freq_per_player, aes(x=Freq)) + 
    geom_histogram(binwidth=1, colour="darkblue", fill="lightblue", alpha=0.5, linetype="dashed")+
    labs(title="Distribution of solo player's gaming frequency",x="Total games", y = "# of players") + 
    scale_x_continuous(breaks=seq(min(freq_per_player$Freq), max(freq_per_player$Freq), by=5))+
    scale_y_continuous(breaks=seq(0, 999, by=5))+ # max freq unknown: 999
    theme_classic() +
    theme(plot.title = element_text(hjust = 0.5), aspect.ratio=2/(1+sqrt(5))) # aspect: golden ratio


library(plyr)
data_per_player <- dlply(solo_data, "player_id", function(solo_data) 
solo_data[order(as.Date(solo_data$time_end, format="%Y-%m-%d %H:%M:%S")),])

# for data of each player: mark the index of games & preserve the first 10
add_index <- function(item){
    item$index_id <- seq.int(nrow(item))
    item <- head(item,20)
    return(item)
}

data_per_player <- ldply(data_per_player, add_index)
meaned_data <- aggregate(data_per_player$mean, by=list(index_id=data_per_player$index_id), FUN=mean)  # get averge socre

ggplot(meaned_data, aes(x=index_id, y=x)) + 
    geom_point(shape=18, color="darkred", size = 4)+
    geom_smooth(method=lm, formula = y ~ poly(x, 2), linetype="dashed", color="darkblue", fill="lightblue", alpha=0.5) +
    labs(title="Learning curve of solo player",x="Games played", y = "Skill score") + 
    scale_x_continuous(breaks=seq(0, min(freq_per_player$Freq), by=1))+
    scale_y_continuous(breaks=seq(0, 999, by=0.5))+ # range unknown: (0,999)
    theme_classic() +
    theme(plot.title = element_text(hjust = 0.5), aspect.ratio=2/(1+sqrt(5))) # aspect: golden ratio

ggsave("lcurve.png")
