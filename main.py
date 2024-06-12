import sys
import json
from data_simulator import HealthDataSimulator
from utils import save_data_to_csv, summarize_data, plot_data_distribution, plot_biased_scatter, plot_disease_liability_histograms

def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py '<bias_config>' '<groups_config>' '<disease_config>'")
        sys.exit(1)

    # Parse the JSON strings for bias configuration, groups configuration, and disease configuration from command-line arguments
    bias_config = json.loads(sys.argv[1])
    groups_config = json.loads(sys.argv[2])
    disease_config = json.loads(sys.argv[3])

    # Define basic feature details that will be used to generate unbiased data
    feature_details = {
        'Income': 'numerical',
        'EducationLevel': 'ordinal',
        'Employment': 'categorical'
    }

    # Initialize the simulator with the number of samples, feature details, and bias configuration
    simulator = HealthDataSimulator(num_samples=10000, feature_details=feature_details, bias_config=bias_config, groups_config=groups_config, disease_config=disease_config)
    simulator.generate_data()
    data = simulator.get_data()
    data_censored = simulator.get_censored_data()

    # Save generated data to a CSV file
    save_data_to_csv(data, 'generated_data_with_bias.csv')
    save_data_to_csv(data_censored, 'generated_data_with_bias_censored.csv')
    summarize_data(data)
    summarize_data(data_censored)

    # Visualize data distributions and biased scatter plots for each biased numerical variable
    for feature in data.columns:
        plot_data_distribution(data, feature)
        if 'numerical_biased' in feature:
            plot_biased_scatter(data, feature)
    
    # Plot histograms of disease liability for each group using censored data
    plot_disease_liability_histograms(data_censored)

if __name__ == '__main__':
    main()
