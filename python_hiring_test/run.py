"""Main script for generating output.csv."""
import os
import pandas as pd


def read_csv_file():
    directory_name = os.path.dirname(os.path.realpath(__file__))
    csv_data = pd.read_csv(os.path.join(directory_name, 'data', 'raw', 'pitchdata.csv'))
    return csv_data


def pitcher(csv_data):
    temp_pitcher_list = []
    temp_hitter_list = []
    pitcher = csv_data.groupby(['PitcherTeamId', 'HitterSide'],
                               as_index=False)['PA', 'AB', 'H', '2B', '3B', 'HR', 'TB', 'BB', 'SF', 'HBP'].sum()
    pitcher['Subject'] = 'PitcherTeamId'
    for i, j in enumerate(pitcher.columns):
        if j == 'PitcherTeamId':
            temp_pitcher_list.append('SubjectId')
        else:
            temp_pitcher_list.append(j)
    pitcher.columns = temp_pitcher_list
    for i in pitcher.HitterSide:
        if i == 'L':
            temp_hitter_list.append('vs LHH')
        elif i == 'R':
            temp_hitter_list.append('vs RHH')
    pitcher['Split'] = temp_hitter_list
    return pitcher


def hitter(csv_data):
    temp_pitcher_list = []
    temp_hitter_list = []
    hitter = csv_data.groupby(['HitterTeamId', 'PitcherSide'],
                              as_index=False)['PA', 'AB', 'H', '2B', '3B', 'HR', 'TB', 'BB', 'SF', 'HBP'].sum()
    hitter['Subject'] = 'HitterTeamId'
    for i, j in enumerate(hitter.columns):
        if j == 'HitterTeamId':
            temp_hitter_list.append('SubjectId')
        else:
            temp_hitter_list.append(j)
    hitter.columns = temp_hitter_list
    for i in hitter.PitcherSide:
        if i == 'L':
            temp_pitcher_list.append('vs LHP')
        elif i == 'R':
            temp_pitcher_list.append('vs RHP')
    hitter['Split'] = temp_pitcher_list
    return hitter


def calculation(data):
    data['AVG'] = (data.H / data.AB).round(3)
    data['OBP'] = ((data.H + data.BB + data.HBP) / (data.AB + data.BB + data.HBP + data.SF)).round(3)
    data['SLG'] = (data.TB / data.AB).round(3)
    data['OPS'] = data.SLG + data.OBP
    return data


def write_csv(result):
    directory_name = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(directory_name, 'data', 'processed', 'output.csv')
    headers = ['SubjectId', 'Stat', 'Split', 'Subject']
    csv = result.sort_values(headers, ascending=True)
    csv.to_csv(path_or_buf=file_path, index=False)


def main():
    csv_data = read_csv_file()
    concated_data = pd.concat([pitcher(csv_data), hitter(csv_data)], axis=0, ignore_index=True)
    data_frame = calculation(concated_data)

    result = pd.melt(data_frame, id_vars=['SubjectId', 'Split', 'Subject'],
                     value_vars=['AVG', 'OBP', 'SLG', 'OPS'], var_name='Stat', value_name='Value')
    write_csv(result)


if __name__ == '__main__':
    main()
