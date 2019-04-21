***************************************************************************************************************************
This repository is currently under reconstruction, and we are refactoring the code for higher efficiency and better readability. We will provide detailed running instructions of our system.
***************************************************************************************************************************


This is the system for the paper "Context-Sensitive Malicious Spelling Error Correction" to appear in the Web Conference 2019. 

Code structure:
1. add_errors/: the module to add malicious errors;
2. domain_corpus_generation/: the module to process domain corpus such as Perspective data or spam data;
3. context_based_selection/: the module to correct spelling errors based on context;
4. perspective_evaluation/: the module to run baselines spell checkers on Perspective data;
5. spam/: the module on error generation and correction on spam data.
