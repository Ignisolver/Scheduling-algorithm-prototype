from test_files.set_parameters import change_param
from importlib import reload
import main as main_module


# całość
def run_test():
    base_test()
    # reassign_test()
    # sections_test()
    # iterations_test()
    # fun_weights_test()
    # utime_test()
    #input_data_test()


def base_test():
    change_param()
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


# grupy testów
def reassign_test():
    reconstruction_test()
    backtracking_test()
    replacing_test()


def sections_test():
    sections1()
    sections2()


def iterations_test():
    iterations_back()
    iterations_recon()
    iterations_repl()


def step_test():
    step1_back()
    step2_back()
    step1_rec()
    step2_rec()


def fun_weights_test():
    FD_domination_test()
    FO_domination_test()
    FP_domination_test()
    FR_domination_test()


def utime_test():
    utime1()
    utime2()


def input_data_test():
    input_data1()
    input_data2()
    input_data3()
    input_data4()
    input_data5()


# pojedyncze testy
def replacing_test():
    change_param(reassign="replace", folder="replace", description="Test of replacing method of reassignment")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def reconstruction_test():
    change_param(reassign="reconstruction", folder="reconst", description="Test of reconstruction method of reassignment")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def backtracking_test():
    change_param(reassign="backtracking", folder="backtr", description="Test of backtracking method of reassignment")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def sections1():
    change_param(sections=1, folder="section1", description="Test of section parameter (reduced)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def sections2():
    change_param(sections=200, folder="section2", description="Test of section parameter (increased)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def iterations_back():
    change_param(max_fail=1, folder="iterback", description="Test of reduced failure counter in backtracking")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def iterations_recon():
    change_param(max_fail=1, folder="iterrec", description="Test of reduced failure counter in reconstruction")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def iterations_repl():
    change_param(max_fail=10, folder="iterrepl", description="Test of reduced failure counter in replacing")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FO_domination_test():
    change_param(fun_weight=(2, 1, 1, 1), folder="domFO", description="Test of effect of domination of FO part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FP_domination_test():
    change_param(fun_weight=(1, 1, 2, 1), folder="domFP", description="Test of effect of domination of FP part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FD_domination_test():
    change_param(fun_weight=(1, 2, 1, 1), folder="domFD", description="Test of effect of domination of FD part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def FR_domination_test():
    change_param(fun_weight=(1, 1, 1, 2), folder="domFR", description="Test of effect of domination of FR part")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def utime1():
    change_param(utime=5, folder="utime1", description="Test of time unit parameter (reduced)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def utime2():
    change_param(utime=20, folder="utime2", description="Test of time unit parameter (increased)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def step1_back():
    change_param(utime=20, folder="step1b", description="Test of step parameter in backtracking (increased)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def step2_back():
    change_param(utime=20, folder="step2b", description="Test of step parameter in backtracking (reduced)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def step1_rec():
    change_param(utime=20, folder="step1r", description="Test of step parameter in reconstruction (increased)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def step2_rec():
    change_param(utime=20, folder="step2r", description="Test of step parameter in reconstruction (reduced)")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


# TODO zastanowić się jakie dane wejściowe chcemy przetestować
def input_data1():
    change_param(rooms="sample data/sale_1.csv", folder="input_data1")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data2():
    change_param(lecturers="sample data/prowadzacy_1.csv", folder="input_data2")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data3():
    change_param(groups="sample data/grupy_1.csv", folder="input_data3")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data4():
    change_param(classes="sample data/zajecia_1.csv", folder="input_data4")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


def input_data5():
    change_param(classes="sample data/zajecia_2.csv", folder="input_data5")
    global main_module
    main_module = reload(main_module)
    main_func = main_module.main
    main_func()


if __name__ == "__main__":
    base_test()
