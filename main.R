data <- read.csv(file.choose())

data$AppointmentHour <- substr(data$AppointmentTime, 1, 2)

# bar chart data
hour_counts <- table(data$AppointmentHour)

hour_df <- data.frame(
  Hour = names(hour_counts),
  Count = as.numeric(hour_counts)
)

hour_df

# bar plot
barplot(hour_df$Count,
        names.arg = hour_df$Hour,
        col = "lightblue",
        main = "Appointments by Hour",
        ylab = "Number of Appointments")


# pie chart data
status_counts <- table(data$ArrivalStatus)

status_df <- data.frame(
  Status = names(status_counts),
  Count = as.numeric(status_counts)
)

status_df

# pie chart
pie(status_df$Count,
    labels = status_df$Status,
    col = c("green", "yellow", "red"),
    main = "Appointment Status Distribution")

# summary table listing patient status

summary_table <- table(data$PatientName, data$ArrivalStatus)

summary_table

write.csv(summary_table, "attendance_summary.csv")

