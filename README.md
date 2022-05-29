# TamGramCheck - Neural-based Tamil Grammar Error Detector and Suggestor

This is the development of a grammar error detector for the Tamil language using the state-of-the-art deep neural-based approach. This proposed checker captures a vital grammar error called subject-predicate agreement errors. In this case, we specifically target the agreement error between nominal subjects and verbal predicates. We also created the first-ever grammar error annotated corpus for Tamil. We have found way to create error corpus in automatic way. In addition, we experimented with different multi-lingual pre-trained language models to capture syntactic information and found that IndicBERT gives better performance for our tasks. We implemented this grammar checker as a multi-class classification on top of the IndicBERT pre-trained model, which we fine-tuned using our grammar-error annotated data. This final model gives an F1 Score of 97.4.
