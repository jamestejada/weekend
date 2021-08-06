from modules.data import DATA_LIST, SATELLITE_DATA_LIST
import pytest
from modules.settings import check_flags

def main():

    if check_flags('test', 'tests'):
        pytest.main(['-vv'])




if __name__ == '__main__':
    main()
