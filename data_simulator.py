import numpy as np
import pandas as pd

class HealthDataSimulator:
    def __init__(self, num_samples, feature_details, bias_config, groups_config, disease_config):
        self.num_samples = num_samples
        self.feature_details = feature_details
        self.bias_config = bias_config
        self.groups_config = groups_config
        self.disease_config = disease_config
        self.data = pd.DataFrame()

    def generate_data(self):
        # Generate unbiased data
        for feature, f_type in self.feature_details.items():
            if f_type == 'numerical':
                self.data[feature] = np.random.normal(loc=50, scale=10, size=self.num_samples)
            elif f_type == 'ordinal':
                self.data[feature] = np.random.choice([1, 2, 3, 4, 5], size=self.num_samples, p=[0.1, 0.2, 0.4, 0.2, 0.1])
            elif f_type == 'categorical':
                self.data[feature] = np.random.choice(['low', 'medium', 'high'], size=self.num_samples, p=[0.3, 0.4, 0.3])

        # Assign groups
        self.data['Group'] = np.random.choice(list(self.groups_config.keys()), size=self.num_samples, p=[1/len(self.groups_config)]*len(self.groups_config))

        # Introduce biased variables
        self.introduce_bias()

        # Generate disease state
        self.generate_disease_state()

        # Censor data
        self.censor_data()

    def introduce_bias(self):
        for bias_type, settings in self.bias_config.items():
            for i in range(settings['count']):
                for group, params in self.groups_config.items():
                    group_indices = self.data[self.data['Group'] == group].index
                    bias_name = f"{bias_type}_biased_{i+1}_{group}"
                    if bias_type == 'numerical':
                        base_data = self.data.loc[group_indices, settings['base_feature']] + np.random.normal(loc=params['mean_shift'], scale=params['variance_factor'], size=len(group_indices))
                    elif bias_type == 'ordinal':
                        base_probs = np.array([0.1, 0.2, 0.4, 0.2, 0.1]) * params['variance_factor']
                        normalized_probs = base_probs / base_probs.sum()
                        base_data = np.random.choice([1, 2, 3, 4, 5], size=len(group_indices), p=normalized_probs)
                    elif bias_type == 'categorical':
                        base_probs = np.array([0.3, 0.4, 0.3]) * params['variance_factor']
                        normalized_probs = base_probs / base_probs.sum()
                        base_data = np.random.choice(['low', 'medium', 'high'], size=len(group_indices), p=normalized_probs)
                    self.data.loc[group_indices, bias_name] = base_data

    def generate_disease_state(self):
        self.data['DiseaseLiability'] = np.random.normal(loc=0, scale=1, size=self.num_samples)
        for group, params in self.groups_config.items():
            group_indices = self.data[self.data['Group'] == group].index
            self.data.loc[group_indices, 'DiseaseLiability'] += np.random.normal(loc=params.get('disease_mean_shift', 0), scale=params.get('disease_variance_factor', 1), size=len(group_indices))
        prevalence_threshold = np.percentile(self.data['DiseaseLiability'], 100 - self.disease_config['prevalence'])
        self.data['DiseaseState'] = (self.data['DiseaseLiability'] >= prevalence_threshold).astype(int)

    def censor_data(self):
        drop_indices = []
        for group, params in self.groups_config.items():
            group_indices = self.data[self.data['Group'] == group].index
            for index in group_indices:
                income = self.data.at[index, 'Income']
                education = self.data.at[index, 'EducationLevel']
                censor_prob = self.smooth_censoring_function(income, education, params['censor_shape'])
                if np.random.rand() < censor_prob:
                    drop_indices.append(index)

        self.data_censored = self.data.drop(index=drop_indices).reset_index(drop=True)
        if len(self.data_censored) > self.num_samples:
            self.data_censored = self.data_censored.sample(n=self.num_samples, random_state=1).reset_index(drop=True)

    def smooth_censoring_function(self, income, education, shape):
        max_income = self.data['Income'].max()
        max_education = self.data['EducationLevel'].max()
        normalized_income = income / max_income
        normalized_education = education / max_education
        censor_prob = 1 - np.exp(-shape * (1 - normalized_income) * (1 - normalized_education))
        return min(censor_prob, 1)

    def get_data(self):
        return self.data

    def get_censored_data(self):
        return self.data_censored
