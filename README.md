# Overview

The Bias Simulation Package is designed to generate synthetic datasets that include both unbiased and biased data. This package can be used for bias mitigation studies, allowing researchers and practitioners to test and evaluate various bias mitigation techniques. The package outputs two versions of the dataset: one without bias and one with simulated biases based on user-defined parameters.
How the Program Works

The program generates a dataset with specified features and introduces biases according to user-defined configurations. It allows for:

    Feature Generation: Creating numerical, ordinal, and categorical features.
    Bias Introduction: Applying biases to these features based on groups with specific mean shifts and variance adjustments.
    Disease State Simulation: Generating a disease liability score and a binary disease state based on a specified prevalence.
    Censoring: Removing data points from the biased dataset based on a smooth censoring function that depends on income and education levels as well as racial group.

The program outputs two datasets:

    Full Dataset: Includes all generated data points with applied biases.
    Censored Dataset: A subset of the full dataset with certain data points removed based on the censoring criteria.

## Input Parameters

The program accepts several parameters to control the data generation and bias introduction processes. These parameters are provided in JSON format and passed as command-line arguments to the main script.
### 1. Bias Configuration (bias_config)

This parameter specifies the number and characteristics of biased variables.

    numerical: Configuration for numerical biased variables.
        count: Number of numerical biased variables.
        base_feature: The feature on which the biased variable is based.
        mean_shift: Mean shift applied to the biased variable.
        variance_factor: Factor by which the variance is adjusted.

### 2. Groups Configuration (groups_config)

This parameter specifies the characteristics of different groups in the dataset.

    Group Name: A dictionary for each group specifying:
        mean_shift: Mean shift applied to features for this group.
        variance_factor: Factor by which the variance is adjusted for this group.
        censor_threshold: Threshold below which data points are considered for censoring.
        censor_probability: Probability of censoring a data point below the threshold.
        censor_shape: Shape parameter for the smooth censoring function.
        disease_mean_shift: Mean shift for the disease liability score.
        disease_variance_factor: Variance factor for the disease liability score.
        censor_<variable>_probability: Censoring probability for each new variable by racial group.

### 3. Disease Configuration (disease_config)

This parameter specifies the characteristics of the disease state.

    prevalence: Prevalence of the disease in the population (as a percentage).

### 4. Correlated Variables Configuration (correlated_config)

This parameter specifies the variables that need to be correlated with the disease liability.

    Variable Name: A dictionary for each variable specifying:
        type: The type of the variable (categorical or continuous).
        mean: (Optional) Mean of the variable if continuous.
        std: (Optional) Standard deviation of the variable if continuous.
        correlation: The desired correlation with disease liability.

## Example Command

The following command demonstrates how to run the script with example configurations for bias, groups, disease, and correlated variables:

bash

python main.py \
'{"numerical": {"count": 2, "base_feature": "Income", "mean_shift": 5, "variance_factor": 1.2}}' \
'{
    "WhiteNonHispanic": {"mean_shift": 5, "variance_factor": 1.2, "censor_threshold": 40, "censor_probability": 0.05, "censor_shape": 1.0, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.1, "censor_PatientRace_probability": 0.1},
    "WhiteHispanic": {"mean_shift": 7, "variance_factor": 1.3, "censor_threshold": 35, "censor_probability": 0.07, "censor_shape": 1.2, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.1, "censor_PatientRace_probability": 0.1},
    "BlackNonHispanic": {"mean_shift": 3, "variance_factor": 1.4, "censor_threshold": 30, "censor_probability": 0.10, "censor_shape": 1.4, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.15, "censor_PatientRace_probability": 0.15},
    "BlackHispanic": {"mean_shift": 4, "variance_factor": 1.5, "censor_threshold": 25, "censor_probability": 0.15, "censor_shape": 1.6, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.15, "censor_PatientRace_probability": 0.15},
    "Asian": {"mean_shift": 6, "variance_factor": 1.1, "censor_threshold": 50, "censor_probability": 0.02, "censor_shape": 0.8, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.05, "censor_PatientRace_probability": 0.05},
    "Mixed": {"mean_shift": 2, "variance_factor": 1.2, "censor_threshold": 45, "censor_probability": 0.05, "censor_shape": 1.0, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.1, "censor_PatientRace_probability": 0.1}
}' \
'{"prevalence": 5}' \
'{
    "PatientSex": {"type": "categorical", "correlation": 0.7},
    "PatientRace": {"type": "categorical", "correlation": 0.7},
    "PatientEthnicity": {"type": "categorical", "correlation": 0.7},
    "PatientAge": {"type": "continuous", "mean": 10, "std": 5, "correlation": 0.7},
    "ChildOpportunityIndex": {"type": "continuous", "mean": 50, "std": 20, "correlation": 0.7},
    "CommunitySleepDuration": {"type": "continuous", "mean": 50, "std": 20, "correlation": 0.7},
    "Snoring": {"type": "categorical", "correlation": 0.7},
    "Insomnia": {"type": "categorical", "correlation": 0.7},
    "InsomniaSeverityIndex": {"type": "continuous", "mean": 15, "std": 10, "correlation": 0.7},
    "EpworthSleepinessScale": {"type": "continuous", "mean": 12, "std": 6, "correlation": 0.7},
    "SleepDisordersChecklist_Insomnia": {"type": "continuous", "mean": 6, "std": 4, "correlation": 0.7},
    "SleepDisordersChecklist_Circadian": {"type": "continuous", "mean": 3, "std": 2, "correlation": 0.7},
    "SleepDisordersChecklist_Narcolepsy": {"type": "continuous", "mean": 3, "std": 2, "correlation": 0.7},
    "SleepDisordersChecklist_ObstructiveSleepApnea": {"type": "continuous", "mean": 6, "std": 4, "correlation": 0.7},
    "SleepDisordersChecklist_RestlessLegSyndrome": {"type": "continuous", "mean": 4.5, "std": 3, "correlation": 0.7},
    "SleepDisordersChecklist_Parasomnias": {"type": "continuous", "mean": 4.5, "std": 3, "correlation": 0.7},
    "CaffeineUse": {"type": "categorical", "correlation": 0.7},
    "ElectronicUseAtNight": {"type": "categorical", "correlation": 0.7},
    "SleepDuration": {"type": "categorical", "correlation": 0.7},
    "SleepRelatedReferral": {"type": "categorical", "correlation": 0.7}
}'

## Detailed Example Code Explanation

Here is a detailed breakdown of the example command:

bash

python main.py \
'{"numerical": {"count": 2, "base_feature": "Income", "mean_shift": 5, "variance_factor": 1.2}}' \
'{
    "WhiteNonHispanic": {"mean_shift": 5, "variance_factor": 1.2, "censor_threshold": 40, "censor_probability": 0.05, "censor_shape": 1.0, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.1, "censor_PatientRace_probability": 0.1},
    "WhiteHispanic": {"mean_shift": 7, "variance_factor": 1.3, "censor_threshold": 35, "censor_probability": 0.07, "censor_shape": 1.2, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.1, "censor_PatientRace_probability": 0.1},
    "BlackNonHispanic": {"mean_shift": 3, "variance_factor": 1.4, "censor_threshold": 30, "censor_probability": 0.10, "censor_shape": 1.4, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.15, "censor_PatientRace_probability": 0.15},
    "BlackHispanic": {"mean_shift": 4, "variance_factor": 1.5, "censor_threshold": 25, "censor_probability": 0.15, "censor_shape": 1.6, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.15, "censor_PatientRace_probability": 0.15},
    "Asian": {"mean_shift": 6, "variance_factor": 1.1, "censor_threshold": 50, "censor_probability": 0.02, "censor_shape": 0.8, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.05, "censor_PatientRace_probability": 0.05},
    "Mixed": {"mean_shift": 2, "variance_factor": 1.2, "censor_threshold": 45, "censor_probability": 0.05, "censor_shape": 1.0, "disease_mean_shift": 0, "disease_variance_factor": 1, "censor_PatientSex_probability": 0.1, "censor_PatientRace_probability": 0.1}
}' \
'{"prevalence": 5}' \
'{
    "PatientSex": {"type": "categorical", "correlation": 0.7},
    "PatientRace": {"type": "categorical", "correlation": 0.7},
    "PatientEthnicity": {"type": "categorical", "correlation": 0.7},
    "PatientAge": {"type": "continuous", "mean": 10, "std": 5, "correlation": 0.7},
    "ChildOpportunityIndex": {"type": "continuous", "mean": 50, "std": 20, "correlation": 0.7},
    "CommunitySleepDuration": {"type": "continuous", "mean": 50, "std": 20, "correlation": 0.7},
    "Snoring": {"type": "categorical", "correlation": 0.7},
    "Insomnia": {"type": "categorical", "correlation": 0.7},
    "InsomniaSeverityIndex": {"type": "continuous", "mean": 15, "std": 10, "correlation": 0.7},
    "EpworthSleepinessScale": {"type": "continuous", "mean": 12, "std": 6, "correlation": 0.7},
    "SleepDisordersChecklist_Insomnia": {"type": "continuous", "mean": 6, "std": 4, "correlation": 0.7},
    "SleepDisordersChecklist_Circadian": {"type": "continuous", "mean": 3, "std": 2, "correlation": 0.7},
    "SleepDisordersChecklist_Narcolepsy": {"type": "continuous", "mean": 3, "std": 2, "correlation": 0.7},
    "SleepDisordersChecklist_ObstructiveSleepApnea": {"type": "continuous", "mean": 6, "std": 4, "correlation": 0.7},
    "SleepDisordersChecklist_RestlessLegSyndrome": {"type": "continuous", "mean": 4.5, "std": 3, "correlation": 0.7},
    "SleepDisordersChecklist_Parasomnias": {"type": "continuous", "mean": 4.5, "std": 3, "correlation": 0.7},
    "CaffeineUse": {"type": "categorical", "correlation": 0.7},
    "ElectronicUseAtNight": {"type": "categorical", "correlation": 0.7},
    "SleepDuration": {"type": "categorical", "correlation": 0.7},
    "SleepRelatedReferral": {"type": "categorical", "correlation": 0.7}
}'

    Bias Configuration:
        Creates 2 numerical biased variables based on the Income feature with a mean shift of 5 and a variance factor of 1.2.

    Groups Configuration:
        WhiteNonHispanic: Features are shifted by a mean of 5 and variance of 1.2. Censoring occurs below a threshold of 40 with a probability of 5%, shaped by 1.0. Specific censoring probabilities are set for PatientSex and PatientRace.
        WhiteHispanic: Features are shifted by a mean of 7 and variance of 1.3. Censoring occurs below a threshold of 35 with a probability of 7%, shaped by 1.2. Specific censoring probabilities are set for PatientSex and PatientRace.
        BlackNonHispanic: Features are shifted by a mean of 3 and variance of 1.4. Censoring occurs below a threshold of 30 with a probability of 10%, shaped by 1.4. Specific censoring probabilities are set for PatientSex and PatientRace.
        BlackHispanic: Features are shifted by a mean of 4 and variance of 1.5. Censoring occurs below a threshold of 25 with a probability of 15%, shaped by 1.6. Specific censoring probabilities are set for PatientSex and PatientRace.
        Asian: Features are shifted by a mean of 6 and variance of 1.1. Censoring occurs below a threshold of 50 with a probability of 2%, shaped by 0.8. Specific censoring probabilities are set for PatientSex and PatientRace.
        Mixed: Features are shifted by a mean of 2 and variance of 1.2. Censoring occurs below a threshold of 45 with a probability of 5%, shaped by 1.0. Specific censoring probabilities are set for PatientSex and PatientRace.

    Disease Configuration:
        Sets the disease prevalence in the population at 5%.

    Correlated Variables Configuration:
        Specifies the variables to be generated, their types, means, standard deviations, and correlations with disease liability.

## Conclusion

The Bias Simulation Package provides a flexible and powerful tool for generating synthetic datasets with controlled biases and disease states. By allowing detailed configuration of biases, disease prevalence, and censoring, users can create realistic datasets to test and evaluate bias mitigation techniques effectively. The provided example command demonstrates how to configure and run the simulation with the specified variables and their correlations, generating a dataset suitable for bias mitigation studies.
