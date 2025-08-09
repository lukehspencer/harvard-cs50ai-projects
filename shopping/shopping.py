import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    print(predictions)

    sensitivity, specificity = evaluate(y_test, predictions)
    
    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open(filename, "r", newline='') as f:
        reader = csv.DictReader(f) # read csv in as a dictionary

        # Initilize evidence list and labels list
        evidence = []
        labels = []
        # Categorize columns by what data type they need to be changed to 
        int_cols = ["Administrative", "Informational", "ProductRelated", "OperatingSystems", "Browser", "Region", "TrafficType"] 
        float_cols = ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]
        # Map all months to a number
        month_nums = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}

        # Add col values from each row in csv file into evidence and labels with the correct data types or normalization
        for row in reader:
            user_evidence = []
            for col in row:
                if col in int_cols:
                    user_evidence.append(int(row[col]))
                elif col in float_cols:
                    user_evidence.append(float(row[col]))
                elif col == "Month":
                    user_evidence.append(month_nums[row[col]])
                elif col == "VisitorType":
                    user_evidence.append(1 if row[col] == "Returning_Visitor" else 0)
                elif col == "Weekend":
                    user_evidence.append(1 if row[col] == "TRUE" else 0)
                else:
                    labels.append(1 if row[col] == "TRUE" else 0) # label = 1 if person purchased an item and label = 0 if person didn't purchase an item

            evidence.append(user_evidence)
            
    return (evidence, labels)

    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1) # build model with k=1 neighbors
    model.fit(evidence, labels) # fit model to training dataset 
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    predicted_positive = 0
    predicted_negative = 0
    false_positives = 0
    false_negatives = 0

    # Counts all the True Positives, False Positives, True Negatives, and False Negatives in predictions
    for labels in zip(predictions, labels):
        if labels[0] == 1:
            if labels[1] != 1:
                false_positives+=1
            else:
                predicted_positive+=1
        else:
            if labels[1] != 0:
                false_negatives+=1
            else:
                predicted_negative+=1

    sensitivity = predicted_positive / (predicted_positive + false_negatives) # calculates sensitivity (number of people that actually bought an item and that were classified correctly)
    specificity = predicted_negative / (predicted_negative + false_positives) # calculates specificity (number of people that didn't buy an item and that were classified correctly)

    return (sensitivity, specificity)

    raise NotImplementedError


if __name__ == "__main__":
    main()
