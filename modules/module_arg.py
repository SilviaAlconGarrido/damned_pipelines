#import library
import argparse

#filtrar el df por el nombre del lab 
def name_lab(df):
    name_lab =str(input('Input the name of the lab: '))
    df_filtro = DF_CSV['Lab Name'] == 'advanced-mysql'
    df_name = DF_CSV[df_filtro]
 


#argument parser functions
def argument_parser(df_csv,):
    parser = argparse.ArgumentParser(description= 'new table with labs advanced-mysql' )
    help_message ='select the name of the lab' 
    parser.add_argument('-l', '--function', help=help_message, type=str)
    args = parser.parse_args()
    return args

