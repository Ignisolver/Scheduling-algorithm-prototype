from test_files.set_parameters import change_param
from importlib import reload
import main as main_module


# całość
def run_test():
    input_data_test()
    reassign_test()
    fun_weights_test()
    sections_test()
    utime_test()


# grupy testów
def input_data_test():
    input_data1()
    input_data2()
    input_data3()
    input_data4()


def reassign_test():
    ignore_test()

    reconstruction_test()
    reconstruction_fail1_test()
    reconstruction_fail2_test()
    reconstruction_step1_test()
    reconstruction_step2_test()

    backtracking_test()
    backtracking_fail1_test()
    backtracking_fail2_test()
    backtracking_step1_test()
    backtracking_step2_test()

    # replacing_test()      # nie działa
    # replacing_fail1_test()
    # replacing_fail2_test()


def sections_test():
    sections1()
    sections2()


def fun_weights_test():
    FD_domination_test()
    FO_domination_test()
    FP_domination_test()
    FR_domination_test()


def utime_test():
    utime1()
    utime2()


# pojedyncze testy
def ignore_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 description="Test of ignoring of failed assignments",
                 folder="ignore",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def replacing_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="replace",
                 description="Test of replacing method of reassignment",
                 folder="replace",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def replacing_fail1_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="replacing",
                 max_fail=1,
                 description="Test of replacing method of reassignment, max_fail reduced",
                 folder="replf1",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def replacing_fail2_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="replacing",
                 max_fail=5,
                 description="Test of replacing method of reassignment, max_fail increased",
                 folder="replf2",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def reconstruction_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="reconstruction",
                 description="Test of reconstruction method of reassignment",
                 folder="recons",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def reconstruction_fail1_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="reconstruction",
                 max_fail=1,
                 description="Test of reconstruction method of reassignment, max_fail reduced",
                 folder="reconsf1",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def reconstruction_fail2_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="reconstruction",
                 max_fail=5,
                 description="Test of reconstruction method of reassignment, max_fail increased",
                 folder="reconsf2",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def reconstruction_step1_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="reconstruction",
                 step=3,
                 description="Test of reconstruction method of reassignment, step reduced",
                 folder="reconss1",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def reconstruction_step2_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="reconstruction",
                 step=30,
                 description="Test of reconstruction method of reassignment, step increased",
                 folder="reconss2",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def backtracking_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 description="Test of backtracking method of reassignment",
                 folder="back",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def backtracking_fail1_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="backtracking",
                 max_fail=1,
                 description="Test of backtracking method of reassignment, max_fail reduced",
                 folder="backf1",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def backtracking_fail2_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="backtracking",
                 max_fail=5,
                 description="Test of backtracking method of reassignment, max_fail increased",
                 folder="backf2",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def backtracking_step1_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="backtracking",
                 step=3,
                 description="Test of backtracking method of reassignment, step reduced",
                 folder="backs1",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def backtracking_step2_test():
    change_param(rooms="sample data/sale_reassign.csv",
                 groups="sample data/grupy_reassign.csv",
                 lecturers="sample data/prowadzacy_reassign.csv",
                 classes="sample data/sale_reassign.csv",
                 reassign="backtracking",
                 step=30,
                 description="Test of backtracking method of reassignment, step increased",
                 folder="backs2",
                 report=1)
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def sections1():
    change_param(sections=1, folder="section1", report=1, description="Test of section parameter (reduced)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def sections2():
    change_param(sections=200, folder="section2", report=1, description="Test of section parameter (increased)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FO_domination_test():
    change_param(fun_weight=(2, 1, 1, 1), folder="domFO", report=1, description="Test of effect of domination of FO part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FP_domination_test():
    change_param(fun_weight=(1, 1, 2, 1), folder="domFP", report=1, description="Test of effect of domination of FP part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FD_domination_test():
    change_param(fun_weight=(1, 2, 1, 1), folder="domFD", report=1, description="Test of effect of domination of FD part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FR_domination_test():
    change_param(fun_weight=(1, 1, 1, 2), folder="domFR", report=1, description="Test of effect of domination of FR part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def utime1():
    change_param(utime=5, folder="utime1", report=1, description="Test of time unit parameter (reduced)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def utime2():
    change_param(utime=20, folder="utime2", report=1, description="Test of time unit parameter (increased)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data1():
    change_param(rooms="sample data/sale_test411.csv",
                 groups="sample data/grupy_test411.csv",
                 lecturers="sample data/prowadzacy_test411.csv",
                 classes="sample data/zajecia_test411.csv",
                 description="Problem prosty test 4.1.1",
                 folder="input_data1")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data2():
    change_param(rooms="sample data/sale_test412.csv",
                 groups="sample data/grupy_test412.csv",
                 lecturers="sample data/prowadzacy_test412.csv",
                 classes="sample data/zajecia_test412.csv",
                 description="Problem prosty test 4.1.2",
                 folder="input_data2")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data3():
    change_param(description="Problem rzeczywisty test 4.1.3",
                 folder="input_data3")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data4():
    change_param(rooms="sample data/sale_test414.csv",
                 groups="sample data/grupy_test414.csv",
                 lecturers="sample data/prowadzacy_test414.csv",
                 classes="sample data/zajecia_test414.csv",
                 description="Problem zlozony test 4.1.4",
                 folder="input_data4")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


if __name__ == "__main__":
    run_test()
