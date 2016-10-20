from src.prototype.lib import file_util
from src import paths

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot

def plot_roc_general(fpr, tpr, label, output_file):
    pyplot.figure()
    pyplot.plot(fpr, tpr, label='ROC curve -- %s' % label)
    pyplot.plot([0, 1], [0, 1], 'k--')
    pyplot.xlim([0.0, 1.0])
    pyplot.ylim([0.0, 1.0])
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.legend(loc="lower right")
    pyplot.savefig(output_file)

def plot_roc(fpr, tpr, auc, prefix, relation, relation_name):
    d = paths.CHARTS_PATH + "/train-roc/" + relation
    file_util.ensure_dir(d)
    label = '%s %s (area = %0.4f)' % (relation, relation_name, auc)
    plot_roc_general(
        fpr, tpr,
        label = label,
        output_file = d + "/" + "roc-%s.png" % prefix
    )
