Approach Note – BigMart Sales Prediction Hackathon

Problem Statement
The goal of this competition was to predict the sales of products across various outlets using historical sales data, item characteristics, and outlet metadata.

1. Understanding the Data
We began by carefully analyzing the provided training dataset which contained:
- Item-level attributes: Item_Identifier, Item_Weight, Item_Fat_Content, Item_Type, Item_MRP
- Outlet-level attributes: Outlet_Identifier, Outlet_Size, Outlet_Location_Type, Outlet_Type
- Target variable: Item_Outlet_Sales

EDA (Exploratory Data Analysis) revealed issues such as:
- Inconsistent labels (low fat vs Low Fat)
- Missing values (Item_Weight, Outlet_Size)
- Outliers in Item_MRP and Item_Outlet_Sales

2. Feature Engineering
To enhance model performance, the following transformations were performed:
- Standardized inconsistent categorical labels (e.g., LF, low fat → Low Fat)
- Created new features:
  - Outlet_Age = Current year - Outlet_Establishment_Year
  - Item_Category derived from the first 2 letters of Item_Identifier
- One-hot encoding for all categorical features
- Imputation of missing Item_Weight using median values by Item_Identifier
- Label encoding and ordinal mappings for ordered categories

3. Modeling
Several models were tested:
- Linear Regression and Ridge Regression as baselines
- Random Forest and Gradient Boosting Regressor for tree-based ensembles
- MLP (Multi-Layer Perceptron) built using PyTorch, with progressively deeper architectures for capturing non-linear patterns

Best performance was achieved using a deep MLP architecture with:
- 9+ layers
- ReLU activation
- StandardScaler normalization
- Dropout regularization
- Final output clamped to prevent negative sales predictions

4. Evaluation
Models were evaluated using RMSE and MAPE on validation sets. Stratified KFold validation was used for robustness. Outliers were removed before final training to reduce prediction error.

5. Results
Our best performing MLP model achieved a leaderboard score of X.XXXX with a rank of ###, significantly outperforming baseline models.
