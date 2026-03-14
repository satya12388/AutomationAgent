import pandas as pd

def export_to_csv(testcases):

    rows = []

    for tc in testcases.testcases:

        rows.append({
            "requirement ID":tc.requirement_id,
            "Test Case ID": tc.test_case_id,
            "Title": tc.title,
            "Preconditions": tc.preconditions,
            "Steps": " | ".join(tc.steps),
            "Expected Result": tc.expected_result,
            "Priority": tc.priority
        })

    df = pd.DataFrame(rows)

    os.makedirs("output", exist_ok=True)

    df.to_csv("output/generated_testcases.csv", index=False)

    return "output/generated_testcases.csv"