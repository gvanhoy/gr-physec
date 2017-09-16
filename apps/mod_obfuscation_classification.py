from file_based_fam import file_based_fam
from random_source_fam import random_source_fam
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt

NUM_SAMPLES_PER_CLASS = 500


class Classifier:
    def __init__(self):
        self.mod_obfuscator = file_based_fam()
        self.normal_modulator = random_source_fam()
        self.features = np.ndarray((2*NUM_SAMPLES_PER_CLASS, 2 * self.mod_obfuscator.specest_cyclo_fam_0.get_N()))
        self.labels = np.zeros(2*NUM_SAMPLES_PER_CLASS, dtype=np.int32)
        self.generate_mod_obfuscation_matrices()
        self.generate_random_source_matrices()
        # self.compare_features()
        self.classify()

    def generate_mod_obfuscation_matrices(self):
        self.mod_obfuscator.start()
        for x in range(0, NUM_SAMPLES_PER_CLASS):
            old_sample = np.max(np.abs(self.mod_obfuscator.specest_cyclo_fam_0.get_estimate()), axis=1)
            new_sample = old_sample
            while new_sample[0] == old_sample[0]:
                new_sample = np.max(np.abs(self.mod_obfuscator.specest_cyclo_fam_0.get_estimate()), axis=1)
            self.features[x, :] = new_sample
            self.labels[x] = 0

        # plt.figure(1)
        # plt.plot(self.features[0, :])
        # plt.draw()

        self.mod_obfuscator.stop()

    def generate_random_source_matrices(self):
        self.normal_modulator.start()
        for x in range(NUM_SAMPLES_PER_CLASS + 1, 2*NUM_SAMPLES_PER_CLASS):
            old_sample = np.max(np.abs(self.normal_modulator.specest_cyclo_fam_0.get_estimate()), axis=1)
            new_sample = old_sample
            while new_sample[0] == old_sample[0]:
                new_sample = np.max(np.abs(self.normal_modulator.specest_cyclo_fam_0.get_estimate()), axis=1)
            self.features[x, :] = new_sample
            self.labels[x] = 1

        # plt.figure(2)
        # plt.plot(self.features[NUM_SAMPLES_PER_CLASS + 1, :])
        # plt.draw()

        self.normal_modulator.stop()

    def classify(self):
        self.features = normalize(self.features, axis=1, norm='max')
        pca = PCA(n_components=25)
        pca.fit_transform(self.features, self.labels)
        clf_alpha = SVC(kernel='linear', decision_function_shape='ovo')
        # clf_alpha = AdaBoostClassifier(
        #             base_estimator=None,
        #             n_estimators=100,
        #             learning_rate=.5,
        #             algorithm='SAMME.R',
        #             random_state=None)
        print cross_val_score(clf_alpha, self.features, self.labels)

    def compare_features(self):
        for x in range(NUM_SAMPLES_PER_CLASS):
            plt.figure(1)
            plt.subplot(121)
            plt.plot(self.features[x, :])
            plt.subplot(122)
            plt.plot(self.features[x + NUM_SAMPLES_PER_CLASS, :])
            plt.show()

    def calculate_error(self, vec_y, vec_y_hat):
        num_errors = 0
        for test_index in range(len(vec_y)):
            if vec_y_hat[test_index] != vec_y[test_index]:
                num_errors += 1.0
        percent_error = 100*num_errors/float(len(vec_y))
        print "Percent error: ", percent_error


if __name__ == '__main__':
    main_class = Classifier()
    main_class.generate_mod_obfuscation_matrices()

