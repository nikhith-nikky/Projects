library(corrplot)
library(tidyverse)
library(randomForest)
library(dplyr)
airbnb<-read.csv('C:/Users/Owner/Downloads/Stat Final Project/data/listings.csv') # reading the data
airbnb_corr<-data.frame(airbnb$latitude,airbnb$longitude,airbnb$price,airbnb$number_of_reviews,airbnb$availability_365,airbnb$minimum_nights)
corr<-cor(airbnb_corr) #correlation matrix
corrplot(corr,method = "circle") #correlation plot


#linear regression
trainingRowIndex <- sample(1:nrow(airbnb), 0.8*nrow(airbnb))  # row indices for the training data
trainingData <- airbnb[trainingRowIndex, ]  # model training data
testData  <- airbnb[-trainingRowIndex, ]  #creating test data

airbnb.lm <- lm(price ~ room_type + neighbourhood_group
                   + latitude + longitude + number_of_reviews + availability_365
                   + calculated_host_listings_count + minimum_nights, data = trainingData) #generating the linear regression model
pricePred <- predict(airbnb.lm, testData) #Prediction of price
AIC(airbnb.lm) #Akaike Information Criterion
actuals_preds <- data.frame(cbind(actuals=testData$price, predicteds=pricePred)) #actual values
correlation_accuracy <- cor(actuals_preds) #calculating correlation accuracy with the help of actual and predicted
head(actuals_preds) #prints the head of the actuals_preds
min_max_accuracy <- mean(apply(actuals_preds, 1, min) / apply(actuals_preds, 1, max)) #calculates the MinMax Accuracy
min_max_accuracy
DMwR::regr.eval(actuals_preds$actuals, actuals_preds$predicteds) #calculates mse, mape,rmse,mae values
plot(airbnb.lm) #plotting the linear model  
plot(airbnb.lm,which=4) # plotting the cook's distance
summary(airbnb.lm) # summary statistics
#linear model 2
airbnb1 <- airbnb %>% filter(price > 0) #filtering the data for applying log function
airbnb1.lm <- lm(log(price) ~ room_type + neighbourhood_group
                + latitude + longitude + number_of_reviews + availability_365
                + reviews_per_month + calculated_host_listings_count + minimum_nights, data = airbnb1)
plot(airbnb1.lm)
plot(airbnb1.lm,which=4)
summary(airbnb1.lm)


#clustering
set.seed(7777)

airbnb$cluster <- kmeans(airbnb %>% 
                               dplyr:: select(longitude, latitude), 10)$cluster #creates a column cluster in airbnb data frame

airbnb %>% 
  ggplot(aes(longitude, latitude, colour = as.factor(cluster))) + 
  geom_point() + 
  guides(colour = F) + 
  labs(x = 'Longitude', y = 'Latitude') # plotting the cluster

# Plotting
hcluster <- left_join(airbnb, airbnb %>% 
                    group_by(cluster, room_type) %>% 
                    summarise(median_price = median(price))) #using group by to form clusters with respect to room_type
hcluster1 <- left_join(airbnb, airbnb %>% 
                        group_by(cluster, neighbourhood_group) %>% 
                        summarise(median_price = median(price))) #using group by to form clusters with respect to room_type

hcluster %>% 
  ggplot(aes(longitude, latitude, colour = median_price)) + 
  geom_point(size = 0.75) + 
  scale_colour_gradient(low = 'yellow', high = 'red') + 
  labs(x = 'Longitude', y = 'Latitude', colour = 'Median_Price') + 
  facet_wrap(~ room_type) + 
  theme(legend.position = 'bottom') #plotting the cluster by room_type

hcluster1 %>% 
  ggplot(aes(longitude, latitude, colour = median_price)) + 
  geom_point(size = 0.75) + 
  scale_colour_gradient(low = 'yellow', high = 'red') + 
  labs(x = 'Longitude', y = 'Latitude', colour = 'Median_Price') + 
  facet_wrap(~ neighbourhood_group) + 
  theme(legend.position = 'bottom') #plotting the cluster by room_type
summary(hcluster)

#RandomForest
airbnb_rf <- randomForest(price ~ neighbourhood_group + neighbourhood + latitude + longitude + room_type + minimum_nights+ availability_365 ,data= trainingData) # creates random forest model
test_rf <- predict(airbnb_rf, testData)  #predicts the airbnb data
airbnb_frame <- data.frame(cbind(actual= airbnb$price, predicted=test_rf)) #creates a data frame using the cbind function
airbnb_frame$error <- airbnb_frame$actual - airbnb_frame$predicted #calculates the error
rmse_rf <- sqrt(mean(airbnb_frame$error^2)) #calculates the rmse value from the above created column
print(rmse_rf) #prints the rmse value
importance(airbnb_rf) #calculates the importance
varImpPlot(airbnb_rf) #plots the model
plot(airbnb_rf)
summary(airbnb_rf)