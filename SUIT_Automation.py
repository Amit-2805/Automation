import os
import shutil

def Environment_variable_setting():
    var_project_name = input("Project name is DCU (Y/N): ")
    if var_project_name.upper() == "Y":
        os.environ["Environment_Name_for_file"] = "DCU"
    else:
        Environment_Name = input("Enter the Project Name : ")
        os.environ["Environment_Name_for_file"] = Environment_Name

    var_unit_name = input("Unit name is CtApASW_FailSafe (Y/N) : ")
    if var_unit_name.upper() == "Y":
        os.environ["Unit_Name"] = "CtApASW_FailSafe"
    else:
        Unit_Name = input("Enter the Unit Name : ")
        os.environ["Unit_Name"] = Unit_Name
def Move_Html_Report(Reports_Name_local_html,folder_path_for_report_move_local_html):
    current_directory = os.getcwd()
    Source_Path_html = os.path.join(current_directory,Reports_Name_local_html+".html")
    Destination_Path = os.path.join(current_directory,folder_path_for_report_move_local_html)
    shutil.move(Source_Path_html,Destination_Path)

def Move_Tst_Report(Reports_Name_local_tst,folder_path_for_report_move_local_tst):
    current_directory = os.getcwd()
    Source_Path_tst = os.path.join(current_directory,Reports_Name_local_tst+".tst")
    Destination_Path = os.path.join(current_directory,folder_path_for_report_move_local_tst)
    shutil.move(Source_Path_tst,Destination_Path)

def Reports_Folder_Name_Generation(path):
    Requirement_Report_Name_back_folder = os.path.dirname(path)
    Requirement_Report_Name = os.path.basename(Requirement_Report_Name_back_folder)
    return Requirement_Report_Name


def Commands_For_Execution_And_Report_Generation(Path_of_tsts_local,folder_path_for_report_move_local):
    for tst_path_requirements,folder_path_move_tst in zip(Path_of_tsts_local,folder_path_for_report_move_local):
        Reports_Name = Reports_Folder_Name_Generation(tst_path_requirements)
        os.system(r'C:\VCAST\clicast.exe -lc -e {} TESt Script Run {}'.format(os.environ["Environment_Name_for_file"],tst_path_requirements))
        os.system(r'C:\VCAST\clicast.exe -lc -e {} EXecute Batch [--update_coverage_data]'.format(os.environ["Environment_Name_for_file"]))
        os.system(r'C:\VCAST\clicast.exe -lc -e {} -u {} Reports Custom Full {}.html'.format(os.environ["Environment_Name_for_file"], os.environ["Unit_Name"], Reports_Name))
        Move_Html_Report(Reports_Name,folder_path_move_tst)
        os.system(r'C:\VCAST\clicast.exe -lc -e {}  TEST Script Create {}.tst'.format(os.environ["Environment_Name_for_file"],Reports_Name))
        Move_Tst_Report(Reports_Name,folder_path_move_tst)
        os.system(r'C:\VCAST\clicast.exe -lc -e {} TESt Delete yes'.format(os.environ["Environment_Name_for_file"]))


def Sending_tst_path():
    Tst_path = input("Enter the path of tsts : ")
    Path_Array = []
    folder_path_report_move = []
    for root, dirs, files in os.walk(Tst_path):
        for file in files:
            if file.endswith('.tst'):
                file_path = os.path.join(root, file)
                Path_Array.append(file_path)
                target_dir = os.path.relpath(root, Tst_path)
                folder_path = os.path.join("Tsts_Report",target_dir)
                folder_path_report_move.append(folder_path)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
    return Path_Array,folder_path_report_move


if __name__ == "__main__":
    Environment_variable_setting()
    Path_of_tsts,folder_path_for_report_move = Sending_tst_path()
    Commands_For_Execution_And_Report_Generation(Path_of_tsts,folder_path_for_report_move)
