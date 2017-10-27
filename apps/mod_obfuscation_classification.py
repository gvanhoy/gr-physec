from physec.file_based_fam import file_based_fam
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import logging
import numpy as np


NUM_SAMPLES_PER_SNR = 50
SNR_RANGE = range(0, 30, 3)
FIGURE_FILENAME = '../results/pcc_v_snr_{0}'.format(time.strftime("%Y%m%d-%H%M%S"))


class Classifier:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.classes = [file_based_fam("/home/ece411/gr-physec/apps/sources/bpsk2qam16.bin"),
                        file_based_fam('/home/ece411/gr-physec/apps/sources/qam16.bin')]
        self.accuracy = np.zeros(len(SNR_RANGE), dtype=np.float32)
        self.features = np.ndarray((len(SNR_RANGE)*len(self.classes)*NUM_SAMPLES_PER_SNR, 2 * self.classes[0].specest_cyclo_fam_0.get_N()))
        self.labels = np.zeros(len(SNR_RANGE)*len(self.classes)*NUM_SAMPLES_PER_SNR, dtype=np.int32)
        self.clf = Pipeline([
            ('normalizer', Normalizer(norm='max')),
            ('PCA', PCA(n_components=25)),
            ('SVM', SVC(kernel='linear', decision_function_shape='ovo'))
        ])
        self.generate_features()
        self.compare_features()
        # self.cross_validation()
        self.pcc_v_snr()

    def generate_features(self):
        for snr_index, snr in enumerate(SNR_RANGE):
            for tb_index, top_block in enumerate(self.classes):
                top_block.set_snr_db(snr)
                top_block.start()
                logging.info("Generating features for tb:{0} snr: {1}".format(tb_index, snr))
                for x in range(NUM_SAMPLES_PER_SNR + 1): # The first sample is being ignored here because the resulting FAM is unstable
                    old_sample = np.max(np.abs(top_block.specest_cyclo_fam_0.get_estimate()), axis=1)
                    new_sample = old_sample
                    while new_sample[0] == old_sample[0]:
                        new_sample = np.max(np.abs(top_block.specest_cyclo_fam_0.get_estimate()), axis=1)
                    if x != 0:
                        self.features[(x - 1) + tb_index*NUM_SAMPLES_PER_SNR + snr_index*len(self.classes)*NUM_SAMPLES_PER_SNR, :] = new_sample
                        self.labels[(x - 1) + tb_index*NUM_SAMPLES_PER_SNR + snr_index*len(self.classes)*NUM_SAMPLES_PER_SNR] = tb_index
                top_block.stop()
                top_block.wait()
        train_features, _, train_labels, _ = train_test_split(self.features, self.labels, test_size=0.33, random_state=42)
        self.clf.fit(train_features, train_labels)

    def pcc_v_snr(self):
        for snr_index in range(len(SNR_RANGE)):
            step = NUM_SAMPLES_PER_SNR*len(self.classes)
            y_pred = self.clf.predict(self.features[snr_index*step:(snr_index + 1)*step, :])
            self.accuracy[snr_index] = accuracy_score(self.labels[snr_index*step:(snr_index + 1)*step], y_pred)
        plt.figure(1)
        plt.plot(SNR_RANGE,
                 100*self.accuracy,
                 color='blue',
                 linewidth=3.0,
                 linestyle='--')
        self.save_figure(1, 'Percent Correct Classification', FIGURE_FILENAME)

    def cross_validation(self):
        logging.info("Cross Validation Scores: " + str(cross_val_score(self.clf, self.train_features, self.train_labels)))

    def save_figure(self, figure_number, figure_title, file_name):
        plt.figure(figure_number)
        plt.xlabel('SNR (dB)', fontsize=18)
        plt.ylabel('Percent Correct Classification', fontsize=16)
        plt.xlim((min(SNR_RANGE), max(SNR_RANGE)))
        plt.ylim((0, 100))
        plt.title(figure_title)
        plt.grid(True)
        # plt.show()
        plt.savefig(file_name + '.eps', format='eps', dpi=1000)
        plt.savefig(file_name + '.png', format='png', dpi=300)
        plt.clf()

    def compare_features(self):
        plt.figure(1)
        for snr_index, snr in enumerate(SNR_RANGE):
            for tb_index, top_block in enumerate(self.classes):
                plt.subplot(1, len(self.classes), tb_index + 1)
                plt.plot(self.features[tb_index*NUM_SAMPLES_PER_SNR + snr_index * len(self.classes) * NUM_SAMPLES_PER_SNR, :])
                plt.grid()
            plt.show()


if __name__ == '__main__':
    main_class = Classifier()

