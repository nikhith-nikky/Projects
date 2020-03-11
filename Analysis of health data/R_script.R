library(tidyverse)
library(corrplot)
data<- read.csv("C:/Users/Owner/Downloads/Ait 580 project/500_Cities__Local_Data_for_Better_Health__2019_release.csv")
data$Data_Value[is.na(data$Data_Value)] = mean(data$Data_Value, na.rm=TRUE)
data$Low_Confidence_Limit[is.na(data$Low_Confidence_Limit)]=mean(data$Low_Confidence_Limit,na.rm = TRUE)
data$High_Confidence_Limit[is.na(data$High_Confidence_Limit)]=mean(data$High_Confidence_Limit,na.rm = TRUE)
any(is.na(data$Year))
any(is.na(data$PopulationCount))
na.omit(data$Latitude)
na.omit(data$Longitude)
summary(data)
set.seed(100)  # setting seed to reproduce results of random sampling
trainingRowIndex <- sample(1:nrow(data), 0.8*nrow(data))  # row indices for training data
trainData <- data[trainingRowIndex, ]  # model training data
testData  <- data[-trainingRowIndex, ] 

data.lm<-lm(Data_Value ~ Low_Confidence_Limit + High_Confidence_Limit + Year + PopulationCount, data=data)
DataPred <- predict(data.lm, testData) 

actuals_preds <- data.frame(cbind(actuals=testData$Data_Value, predicteds=DataPred))
correlation_accuracy <- cor(actuals_preds)
head(actuals_preds)
min_max_accuracy <- mean(apply(actuals_preds, 1, min) / apply(actuals_preds, 1, max))
min_max_accuracy
DMwR::regr.eval(actuals_preds$actuals, actuals_preds$predicteds)
plot(data.lm)
summary(data.lm)
data1<-data.frame(data$Data_Value,data$Low_Confidence_Limit,data$High_Confidence_Limit,data$Year,data$PopulationCount)
corr_mat<-cor(data1)
corrplot(corr_mat,method = "circle")
head(corr_mat)
Text_data=which(data$Short_Question_Text=='Teeth Loss')
Text_data1=which(data$Short_Question_Text=='High Cholesterol')
t.test(data$Data_Value[Text_data],data$Data_Value[Text_data1],
       alternative="less")
Text_data=which(data$Short_Question_Text=='Obesity')
Text_data1=which(data$Short_Question_Text=='High Cholesterol')
t.test(data$Data_Value[Text_data],data$Data_Value[Text_data1],
       alternative="less")
Text_data=which(data$Short_Question_Text=='Teeth Loss')
Text_data1=which(data$Short_Question_Text=='Mental Health')
t.test(data$Data_Value[Text_data],data$Data_Value[Text_data1],
       alternative="less")
Text_data=which(data$Short_Question_Text=='Cancer (except skin)')
Text_data1=which(data$Short_Question_Text=='Stroke')
t.test(data$Data_Value[Text_data],data$Data_Value[Text_data1],
       alternative="less")



