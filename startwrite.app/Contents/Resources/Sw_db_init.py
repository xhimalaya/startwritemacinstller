import SWdb
import desktop_short_cut


def first_table_create():
    SWdb.create_db()
    SWdb.create_license_table()
    SWdb.insert_data_into_license_table()
    desktop_short_cut.create_short_cut_desktop()


try:
    a, b, c, d = SWdb.fetching_data_from_license_table()
    if d == -1:
        first_table_create()
        print("No Data Till Now")
    else:
        print(a, b, c, d)

except:
    print("Some Error in DB_Init")
