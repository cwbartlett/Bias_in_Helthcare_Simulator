import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def save_data_to_csv(data, filename):
    data.to_csv(filename, index=False)

def summarize_data(data):
    print("Summary Statistics:")
    print(data.describe())

def plot_data_distribution(data, feature):
    plt.figure(figsize=(10, 6))
    if data[feature].dtype == 'O':  # Categorical data
        sns.countplot(x=data[feature])
    else:
        sns.histplot(data[feature], kde=True)
    plt.title(f'Distribution of {feature}')
    plt.grid(True)
    plt.show()
    plt.close()  # Ensure the figure is closed after being shown

def plot_biased_scatter(data, biased_variable):
    plt.figure(figsize=(12, 6))

    # Income as x-axis, biased variable as y-axis, color by EducationLevel
    plt.subplot(1, 2, 1)
    sns.scatterplot(x='Income', y=biased_variable, hue='EducationLevel', palette='viridis', data=data)
    plt.title(f'{biased_variable} vs Income, colored by EducationLevel')
    plt.xlabel('Income')
    plt.ylabel(biased_variable)
    plt.legend(title='Education Level')

    # Income as x-axis, biased variable as y-axis, color by Employment
    plt.subplot(1, 2, 2)
    sns.scatterplot(x='Income', y=biased_variable, hue='Employment', palette='cool', data=data)
    plt.title(f'{biased_variable} vs Income, colored by Employment')
    plt.xlabel('Income')
    plt.ylabel(biased_variable)
    plt.legend(title='Employment')

    plt.tight_layout()
    plt.show()
    plt.close()

def plot_disease_liability_histograms(data):
    groups = data['Group'].unique()
    
    # Compute the global min and max for the DiseaseLiability
    min_val = data['DiseaseLiability'].min()
    max_val = data['DiseaseLiability'].max()
    abs_max = max(abs(min_val), abs(max_val))
    xlim = (-abs_max, abs_max)
    
    plt.figure(figsize=(15, len(groups) * 4))
    
    for i, group in enumerate(groups):
        plt.subplot(len(groups), 1, i + 1)
        sns.histplot(data=data[data['Group'] == group], x='DiseaseLiability', kde=True, bins=30)
        plt.title(f'Histogram of Disease Liability for {group}')
        plt.xlabel('Disease Liability')
        plt.ylabel('Frequency')
        plt.xlim(xlim)
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    plt.close()
