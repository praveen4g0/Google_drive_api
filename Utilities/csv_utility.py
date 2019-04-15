import pandas as pd
import os
import logging
import csv

logger = logging.getLogger(__name__)
def write_to_csv(args):
    df=pd.DataFrame(args)
    cwd_dir = os.getcwd()
    credential_dir = os.path.join(cwd_dir, 'resources')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    csv_path = os.path.join(credential_dir,
                                   'AllFilesData.json')
    logger.debug(f'Writing into csv file to the path : {csv_path}')
    try:
        df.to_csv(path_or_buf=csv_path,sep=",",header=True,mode='w',chunksize=1000,index=False)
        logger.debug(f'Data Frame written to csv successfully..')
    except Exception as e:
        logger.error(f'Unable to do write operation ... {e}')


def read_from_csv(size):
    cwd_dir = os.getcwd()
    credential_dir = os.path.join(cwd_dir, 'resources')
    csv_path = os.path.join(credential_dir,
                            'AllFilesData.json')
    try:
        df=pd.read_csv(csv_path,chunksize=size)
        logger.debug("datafarme is read successfully ..")
        return df
    except Exception as e:
        logger.error('Couldnt Read chunksize file into dataframe')






# Function to convert a csv file to a list of dictionaries.  Takes in one variable called &quot;variables_file&quot;

def csv_dict_list():
    # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs
    cwd_dir = os.getcwd()
    credential_dir = os.path.join(cwd_dir, 'resources')
    csv_path = os.path.join(credential_dir,
                            'AllFilesData.json')
    try:
        reader = csv.DictReader(open(csv_path, 'r',buffering=100))
    except Exception as e:
         logger.error('couldnt read csv ')
    dict_list = []
    for line in reader:
        dict_list.append(line)
    if dict is None:
        logger.debug("Nothing to read from csv")
    return dict_list

def read_csv_get_Fileid(name):
    df=csv_dict_list()
    return getFileId(df,name)

def getFileId(df,name):
    ls = [(d['id'], d['mimeType']) for d in df if str(d['name']).__contains__(name)]
    if ls is None:
        logger.error('No File found with that name')
        return None
    else:
        return ls[0]

if __name__=='__main__':
    # write_to_csv()
    print(read_csv_get_Fileid('Blue Jeans'))