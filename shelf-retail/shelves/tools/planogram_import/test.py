import pandas as pd
from main import configure_logging, connect_db, import_planogram_csv, export_planogram_csv, planogram_csv_dtype


DB = "postgres://planogram_test:planogram_test@127.0.0.1:5432/planogram_test"

def test(import_csv, export_csv):
    configure_logging(None)
        
    connect_db(DB)
    planogram_ids = import_planogram_csv(import_csv)

    planogram_id = planogram_ids[0]
    export_planogram_csv(export_csv, planogram_id)

    df1 = pd.read_csv(import_csv, dtype=dict(planogram_csv_dtype), skiprows=2, sep=';')
    df2 = pd.read_csv(export_csv, dtype=dict(planogram_csv_dtype), sep=';')
    
    for x, y in zip(df1.columns, df2.columns):
        assert x == y, (x, y)

    print('headers identical')

    # every entry in original must be present in export
    print()
    print(df1.info())
    print()
    print(df2.info())
    print()


    for i,row1 in df1.iterrows():
        # assert row1 in df2
        for j, row2 in df2.iterrows():
            if (row1 == row2).all():
                break
        else:
            print(f"row {i} in {import_csv} is not present in {export_csv}")
            print(row1)
            import pdb; pdb.set_trace()
            assert 0




    #assert (df1 == df2).all().all(), (df1 == df2).all()

    print('data identical')


if __name__ == '__main__':
    test('test_data/import1.csv', 'test_data/export1.csv')
    #test('test_data/import2.csv', 'test_data/export2.csv')
    print('ok')

