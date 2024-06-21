library(dplyr)

# add data

data <- read.csv('PAS_ward_level_FY_19_20.csv')

# filter to only important columns

simple_data <- data %>% select(Q60, Q61, NQ62C, NQ62D)

na_rows_count <- sum(apply(simple_data, 1, function(row) any(is.na(row))))
na_rows_count

# Only 885 rows are missing a value in at least 1 of the 4 columns, removing them for accuracy

clean_simple_data <- na.omit(simple_data)

# Convert to integer values for question responses

Q60_61_map <- c("Excellent" = 5, "Good" = 4, "Fair" = 3, "Poor" = 2, "Very poor" = 1)
NQ62C_D_map <- c("Strongly agree" = 5, "Tend to agree" = 4, "Neither agree nor disagree" = 3, "Tend to disagree" = 2, "Strongly disagree" = 1)

mapped_simple_data <- clean_simple_data %>% mutate(
  Q60_numeric = Q60_61_map[Q60],
  Q61_numeric = Q60_61_map[Q61],
  NQ62C_numeric = NQ62C_D_map[NQ62C],
  NQ62D_numeric = NQ62C_D_map[NQ62D]
)

### Q60 used as local independent variable, Q61 used as global independent variable

## NQ62C, obligation to follow police orders, used as a dependent variable

# Regression 1: only local

reg1_c <- lm(NQ62C_numeric ~ Q60_numeric, mapped_simple_data)
summary(reg1_c)

# Regression 2: only global

reg2_c <- lm(NQ62C_numeric ~ Q61_numeric, mapped_simple_data)
summary(reg2_c)

# Regression 3: local and global, no interaction

reg3_c <- lm(NQ62C_numeric ~ Q60_numeric + Q61_numeric, mapped_simple_data)
summary(reg3_c)

# Regression 4: local and global, including interaction term

reg4_c <- lm(NQ62C_numeric ~ Q60_numeric + Q61_numeric + Q60_numeric*Q61_numeric, mapped_simple_data)
summary(reg4_c)

## NQ62D, belief that police have same sense of right and wrong, used as a dependent variable

# Regression 1: only local

reg1_d <- lm(NQ62D_numeric ~ Q60_numeric, mapped_simple_data)
summary(reg1_d)

# Regression 2: only global

reg2_d <- lm(NQ62D_numeric ~ Q61_numeric, mapped_simple_data)
summary(reg2_d)

# Regression 3: local and global, no interaction

reg3_d <- lm(NQ62D_numeric ~ Q60_numeric + Q61_numeric, mapped_simple_data)
summary(reg3_d)

# Regression 4: local and global, including interaction term

reg4_d <- lm(NQ62D_numeric ~ Q60_numeric + Q61_numeric + Q60_numeric*Q61_numeric, mapped_simple_data)
summary(reg4_d)