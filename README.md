# TamGramCheck - Neural-based Tamil Grammar Error Detector and Suggestor

This is the development of a grammar error detector for the Tamil language using the state-of-the-art deep neural-based approach. This proposed checker captures a vital grammar error called subject-predicate agreement errors. In this case, we specifically target the agreement error between nominal subjects and verbal predicates. We also created the first-ever grammar error annotated corpus for Tamil. We have found way to create error corpus in automatic way. In addition, we experimented with different multi-lingual pre-trained language models to capture syntactic information and found that IndicBERT gives better performance for our tasks. We implemented this grammar checker as a multi-class classification on top of the IndicBERT pre-trained model, which we fine-tuned using our grammar-error annotated data. This final model gives an F1 Score of 97.4.

## Data Augmentation 
The data augmentation mechanism is very useful to create lots of error sentences from error-less sentences within a shortened time period. This section explained how to generate error sentences from grammatical sentences using a tool called [ThamizhiLIP](https://sarves.github.io/thamizhilip/) which was developed by Mr.Sarveswaran. It has the following functionalities Part of Speech tagging, dependency parsing[^1], and morphological anaysis[^2]. And it is open source. We get the source code from GitHub and change it for our task.

Files 
1. revised_artificial_multiclass.py - This is grammar error generation python script for multiclass. 
2. revised_artificial_for_colab.py, revised_artificial_for_colab2.py, revised_artificial_for_ds1.py, revised_artificial_for_ds2.py, revised_artificial_for_local.py revised_artificial_memory_optimized.py - This is grammar error generation python script for multilabel. These are same code but used in different platform to generate the sentences.
4. multi_class_classification.ipynp - Finetuning process for grammar error detector using IndicBERT[^3] pretrained model.
5. grammatical sentences/ - It contained grammatically correct sentences in the tsv file format.
6. error-annotated_corpus/multiclass - It contained artificial error sentences for multiclass classfication task.
7. error-annotated_corpus/multilabel - It contained artificical error sentences for the multilabel classification task.

[^1]: K. Sarveswaran and G. Dias, “ThamizhiUDp: A dependency parser for Tamil,” in Proceedings of the 17th International Conference on Natural Language
Processing (ICON). Indian Institute of Technology Patna, Patna, India: NLP Association of India (NLPAI), Dec. 2020, pp. 200–207.
[^2]: K. Sarveswaran, G. Dias, and M. Butt, “ThamizhiMorph: A morphological parser for the Tamil language,” Machine Translation, vol. 35, no. 1, pp. 37–70, 2021.
[^3]:D. Kakwani, A. Kunchukuttan, S. Golla, N. Gokul, A. Bhattacharyya, M. M. Khapra, and P. Kumar, “inlpsuite: Monolingual corpora, evaluation benchmarks and pre-trained multilingual language models for indian languages,” in Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: Findings, 2020, pp. 4948–4961.
