#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# - This script analyzes data from PyCity schools to provide a summary of performance metrics, including average scores, budget information, and passing rates.
# 
# ---

# In[69]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.
school_data_complete = pd.merge(student_data, school_data, how="left", on="school_name")
school_data_complete.head(10)


# ## District Summary

# In[71]:


# Calculate the total number of unique schools. Used method 'nunique',
# Could also use len(school_data_complete['school_name'].unique())
school_count = school_data_complete['school_name'].nunique()
school_count


# In[72]:


# Calculate the total number of students by counting unique 'Student ID's
student_count = school_data_complete['Student ID'].nunique()
student_count


# In[73]:


# Calculate the total budget by summing up the budgets of each school
school_budgets = school_data_complete.groupby('school_name')['budget'].first()
# Now sum up the unique budgets per school
total_budget = school_budgets.sum()
total_budget


# In[74]:


# Calculate the average (mean) math score
average_math_score = school_data_complete['math_score'].mean()
average_math_score


# In[75]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete['reading_score'].mean()
average_reading_score


# In[76]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[77]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)
# used matching varibles from math calculations and swapped out math for reading
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
# Double check output 
passing_reading_percentage


# In[78]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate


# In[79]:


# Create a high-level snapshot of the district's key metrics in a DataFrame

district_summary = pd.DataFrame({
    "Total Schools": [school_count],
    "Total Students": [student_count],
    "Total Budget": [total_budget],
    "Math Average": [average_math_score],
    "Reading Average": [average_reading_score],
    "Passing Math Percentage": [passing_math_percentage],
    "Passing Reading Percentage": [passing_reading_percentage],
    "Overall Passing": [overall_passing_rate]

})

# Format the 'Total Students' and 'Total Budget' columns for better readability
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)


# Display the district summary DataFrame
district_summary


# ## School Summary

# In[81]:


# Use the code provided to select the type per school from school_data
school_types = school_data.set_index(["school_name"])["type"]
school_data


# In[82]:


# Calculate the total student count per school from school_data
per_school_counts = school_data_complete.groupby('school_name')['Student ID'].count()
# Display the school name followed by the student count for that school
per_school_counts


# In[83]:


# Calculate the total school budget and per capita spending per school from school_data
per_school_budget = school_data.groupby('school_name')['budget'].first()
per_school_capita = per_school_budget / per_school_counts
per_school_capita


# In[143]:


# Calculate the average test scores per school - Used ".agg" to apply the mean function to the selected column grouped by schools
average_school_scores = school_data_complete.groupby('school_name').agg({
    'reading_score': 'mean',
    'math_score': 'mean'
})
#average_school_scores


# In[145]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[147]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)
# used matching varibles from math calculations and swapped out math for reading
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage

# Double check output 
passing_reading_percentage


# In[151]:


# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()
school_students_passing_math_and_reading


# In[163]:


# Calculate the number of students per school with math scores of 70 or higher from school_data_complete
per_school_math = passing_math_count / per_school_counts * 100
per_school_reading = passing_reading_count / per_school_counts * 100
overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100


# In[165]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above
per_school_summary = pd.DataFrame({
    "School Type": school_types,
    "Total Students": per_school_counts,
    "Total School Budget": per_school_budget,
    "Per Student Budget": per_school_capita,
    "Average Math Score": average_school_scores['math_score'],
    "Average Reading Score": average_school_scores['reading_score'],
    "% Passing Math": per_school_math,
    "% Passing Reading": per_school_reading,
    "% Overall Passing": overall_passing_rate
})

# Format the budget columns for better readability
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# ## Highest-Performing Schools (by % Overall Passing)

# In[167]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values('% Overall Passing', ascending=False)
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# In[169]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values('% Overall Passing', ascending=True)
bottom_schools.head(5)


# ## Math Scores by Grade

# In[171]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grader_math_scores = ninth_graders.groupby('school_name')['math_score'].mean()
tenth_grader_math_scores = tenth_graders.groupby('school_name')['math_score'].mean()
eleventh_grader_math_scores = eleventh_graders.groupby('school_name')['math_score'].mean()
twelfth_grader_math_scores = twelfth_graders.groupby('school_name')['math_score'].mean()

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({
    "9th": ninth_grader_math_scores,
    "10th": tenth_grader_math_scores,
    "11th": eleventh_grader_math_scores,
    "12th": twelfth_grader_math_scores
})
# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# ## Reading Score by Grade 

# In[173]:


# Use the code provided to separate the data by grade
# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_scores = ninth_graders.groupby('school_name')['reading_score'].mean()
tenth_grader_reading_scores = tenth_graders.groupby('school_name')['reading_score'].mean()
eleventh_grader_reading_scores = eleventh_graders.groupby('school_name')['reading_score'].mean()
twelfth_grader_reading_scores = twelfth_graders.groupby('school_name')['reading_score'].mean()

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({
    "9th": ninth_grade_reading_scores,
    "10th": tenth_grader_reading_scores,
    "11th": eleventh_grader_reading_scores,
    "12th": twelfth_grader_reading_scores
})
# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th", "10th", "11th", "12th"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# ## Scores by School Spending

# In[175]:


# Establish the bins
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[177]:


# Create a copy of the school summary for later aggregations
school_spending_df = per_school_summary.copy()
# Create a DataFrame (adjust name if necessary)
school_spending_df = pd.DataFrame({
    "Per Student Budget": per_school_capita
})
# Ensure 'Per Student Budget' is numeric
school_spending_df["Per Student Budget"] = pd.to_numeric(school_spending_df["Per Student Budget"])


# In[179]:


# Use `pd.cut` on the per_school_capita Series from earlier to categorize per student spending based on the bins

# Categorize per_student_spending using pd.cut
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(
    school_spending_df["Per Student Budget"], 
    bins=spending_bins, 
    labels=labels, 
    include_lowest=True
)

# Convert Spending Ranges (Per Student) to a string
school_spending_df["Spending Ranges (Per Student)"] = school_spending_df["Spending Ranges (Per Student)"].astype(str)
school_spending_df


# In[181]:


# Create a copy of the DataFrame
spending_ranges_df = per_school_summary.copy()
# Ensure 'Per Student Budget' is numeric
spending_ranges_df["Per Student Budget"] = pd.to_numeric(school_spending_df["Per Student Budget"])
# Define bins and labels
spending_bins = [0, 585, 615, 645, 675]  # Example bin edges
labels = ["$0-585", "$585-615", "$615-645", "$645-675"]

# Create the spending ranges column
spending_ranges_df["Spending Ranges (Per Student)"] = pd.cut(
    spending_ranges_df["Per Student Budget"], 
    bins=spending_bins, 
    labels=labels, 
    include_lowest=True
)

# Grouping by "Spending Ranges (Per Student)" and calculating mean values
spending_math_scores = spending_ranges_df.groupby("Spending Ranges (Per Student)", observed=False)["Average Math Score"].mean()
spending_reading_scores = spending_ranges_df.groupby("Spending Ranges (Per Student)", observed=False)["Average Reading Score"].mean()
spending_passing_math = spending_ranges_df.groupby("Spending Ranges (Per Student)", observed=False)["% Passing Math"].mean()
spending_passing_reading = spending_ranges_df.groupby("Spending Ranges (Per Student)", observed=False)["% Passing Reading"].mean()
overall_passing_spending = spending_ranges_df.groupby("Spending Ranges (Per Student)", observed=False)["% Overall Passing"].mean()


# In[183]:


# Assemble into DataFrame
# Create the summary DataFrame
spending_summary = pd.DataFrame({
    "Average Math Score": spending_math_scores,
    "Average Reading Score": spending_reading_scores,
    "% Passing Math": spending_passing_math,
    "% Passing Reading": spending_passing_reading,
    "% Overall Passing": overall_passing_spending
})
# Display results
spending_summary


# ## Scores by School Size

# In[188]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[190]:


# Create a copy of the school summary for later aggregations
school_size_df = per_school_summary.copy()


# In[192]:


# Use `pd.cut` on the per_school_counts Series from earlier to categorize school size based on the bins.
school_size_df["School Size"] = pd.cut(school_size_df["Total Students"], bins=size_bins, labels=labels, include_lowest=True)
# Convert School Size to a string

# Convert School Size to a string
school_size_df["School Size"] = school_size_df["School Size"].astype(str)


# In[194]:


# Calculate averages for the desired columns.
size_math_scores = school_size_df.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = school_size_df.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = school_size_df.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = school_size_df.groupby(["School Size"])["% Passing Reading"].mean()
size_overall_passing = school_size_df.groupby(["School Size"])["% Overall Passing"].mean()


# In[196]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({
    "Average Math Score": size_math_scores,
    "Average Reading Score": size_reading_scores,
    "% Passing Math": size_passing_math,
    "% Passing Reading": size_passing_reading,
    "% Overall Passing": size_overall_passing
})


# Display results
size_summary


# ## Scores by School Type

# In[199]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()


# In[201]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({
    "Average Math Score": average_math_score_by_type,
    "Average Reading Score": average_reading_score_by_type,
    "% Passing Math": average_percent_passing_math_by_type,
    "% Passing Reading": average_percent_passing_reading_by_type,
    "% Overall Passing": average_percent_overall_passing_by_type
})

# Display results
type_summary

