This project implements a self-supervised learning based approach for detecting phishing emails. The system combines two models, a Transformer and a CNN, using an ensemble method to improve detection performance.

# PPT Link:
https://drive.google.com/drive/folders/1W4vGmwhvckmb87lDbXYHRhSmEMJIJ7w3?usp=drive_link

#Overview

The goal of this project is to reduce dependence on large labelled datasets by using self-supervised learning techniques. Two methods are used:

- MP-SSL (Masked Prediction) using a Transformer to learn contextual features
- TP-SSL (Transformation Prediction) using a CNN to learn structural patterns

The outputs of both models are combined using an ensemble approach for final classification.

# Datasets Used

- Enron Dataset (normal emails)
  https://www.kaggle.com/datasets/wcukierski/enron-email-dataset
- Nazario Dataset (phishing emails)
  https://www.monkey.org/~jose/phishing/

The final dataset is balanced and used for training and testing.

 # Project Structure

- data_preprocessing.py
- text_preprocessing.py
- embedding_1d.py
- embedding_2d.py
- transformer_model.py
- cnn_model.py
- ensemble_model.py
- mp_ssl_transformer.py
- tp_ssl_cnn.py

## Methodology

1. Data preprocessing and cleaning
2. Text embedding using 1D and 2D representations
3. Training Transformer model (MP-SSL)
4. Training CNN model (TP-SSL)
5. Combining models using ensemble
6. Final classification of emails as phishing or normal

## Results

The model achieves high accuracy on the current dataset. The ensemble approach improves performance by combining contextual and structural features.

## Future Work

- Train on larger datasets
- Use GPU for faster training
- Improve ensemble techniques
- Extend for real-time applications

# Accuracy:
<img width="1811" height="423" alt="Screenshot 2026-04-13 055953" src="https://github.com/user-attachments/assets/ec4e42c7-accb-441d-9b98-03ba63b465d9" />
