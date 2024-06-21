library(dplyr)
library(car)
library(data.table)

# add data

data <- read.csv('PAS_ward_level_FY_19_20.csv')

# filter to only important columns

filtered_data <- data %>% select(NQ147r, NQ155r, NQ146, Q136r, XQ135r, Q62A, Q62B, Q62TI, NQ135BD, NQ135BH)

na_rows_count <- sum(apply(filtered_data, 1, function(row) any(is.na(row))))
na_rows_count

# 15% of rows contain a missing value for one or more columns
# also remove rows with 'other' education, as this level of this education is unclear

cleaned_data <- na.omit(filtered_data)
cleaned_data <- cleaned_data %>% 
  filter(NQ146 != "Other - please specify")

# rename columns for legibility

renamed_data <- cleaned_data %>% 
  rename(
    age = Q136r,
    male = XQ135r,
    education = NQ146, 
    ethnicity = NQ147r,
    nationality = NQ155r
  )

# aggregating education levels

education_aggregation <- c("No qualifications" = "No qualifications", "Trade apprenticeship" = "Apprenticeship", "NVQ/GNVQ" = "Apprenticeship", "O-levels/CSE/GCSEs" = "O-levels", "BTEC Level 1" = "O-levels", "BTEC level 2" = "O-levels", 
                           "A-levels" = "A-levels", "BTEC level 3" = "A-levels", "ONC, OND or City and Guilds" = "A-levels", "HNC or HND/BTEC level 4" = "HNC or HND/BTEC level 4", "University Degree (Bachelor degree)" = "University Degree (Bachelor degree)",
                           "Post-graduate degree or qualification" = "Post-graduate degree or qualification")

aggregated_data <- renamed_data %>% mutate(
  education = education_aggregation[education]
)

# one-hot encoding on education
unique(aggregated_data$education)

encoded_dataset <- mutate(aggregated_data, Apprenticeship = ifelse(education=="Apprenticeship", 1, 0))
encoded_dataset <- mutate(encoded_dataset, O_levels = ifelse(education=="O-levels", 1, 0))
encoded_dataset <- mutate(encoded_dataset, A_levels = ifelse(education=="A-levels", 1, 0))
encoded_dataset <- mutate(encoded_dataset, HNC_HND_BTEC4 = ifelse(education=="HNC or HND/BTEC level 4", 1, 0))
encoded_dataset <- mutate(encoded_dataset, Bachelor = ifelse(education=="University Degree (Bachelor degree)", 1, 0))
encoded_dataset <- mutate(encoded_dataset, Postgraduate = ifelse(education=="Post-graduate degree or qualification", 1, 0))

# mapping other responses to integers

age_map <- c("16-24" = 0, "25-34" = 1, "35-44" = 2, "45-54" = 3, "55-64" = 4, "65 or over" = 5)
male_map <- c("Male" = 0, "Female" = 1, "Other" = 1)
nationality_map <- c("UK" = 0, "Non-UK" = 1)
ethnicity_map <- c("White Other" = 0, "White British" = 0, "Asian" = 1, "Other" = 1, "Black" = 1, "Mixed" = 1)
dependent_map <- c("Strongly agree" = 4, "Tend to agree" = 3, "Neither agree nor disagree" = 2, "Tend to disagree" = 1, "Strongly disagree" = 0)

mapped_data <- encoded_dataset %>% mutate(
  age_numeric = age_map[age],
  male_numeric = male_map[male],
  nationality_numeric = nationality_map[nationality],
  ethnicity_numeric = ethnicity_map[ethnicity],
  Q62A_numeric = dependent_map[Q62A],
  Q62B_numeric = dependent_map[Q62B],
  Q62TI_numeric = dependent_map[Q62TI],
  NQ135BD_numeric = dependent_map[NQ135BD],
  NQ135BH_numeric = dependent_map[NQ135BH],
)

# Multivariate Multiple Regression

model <- lm(cbind(Q62A_numeric, Q62B_numeric, Q62TI_numeric, NQ135BD_numeric, NQ135BH_numeric) ~ Apprenticeship + O_levels + A_levels + HNC_HND_BTEC4 + Bachelor + Postgraduate + age_numeric + male_numeric + nationality_numeric + ethnicity_numeric, mapped_data)

summary(model)
summary(manova(model))
summary(Manova(model))