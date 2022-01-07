from test_files.set_parameters import change_param


# całość
def run_test():
    base_test()
    reassign_test()
    sections_test()
    iterations_test()
    fun_weights_test()
    utime_test()
    input_data_test()


def base_test():
    from main import main
    change_param()
    main()


# grupy testów
def reassign_test():
    reconstruction_test()
    replacing_test()


def sections_test():
    sections1()
    sections2()


def iterations_test():
    iterations1()
    iterations2()


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
    from main import main
    change_param(reassign="replace", folder="replace", description="Test of replacing method of reassignment")
    main()


def reconstruction_test():
    from main import main
    change_param(reassign="reconstruction", folder="reconst", description="Test of reconstruction"
                                                                          " method of reassignment")
    main()


def sections1():
    from main import main
    change_param(sections=1, folder="section1", description="Test of section parameter (reduced)")
    main()


def sections2():
    from main import main
    change_param(sections=200, folder="section1", description="Test of section parameter (increased)")
    main()


def iterations1():
    from main import main
    change_param(max_iter=10, folder="iter1", description="Test of maximum iterations parameter (reduced)")
    main()


def iterations2():
    from main import main
    change_param(max_iter=10000, folder="iter2", description="Test of maximum iterations parameter (increased)")
    main()


def FO_domination_test():
    from main import main
    change_param(fun_weight=(2, 1, 1, 1), folder="domFO", description="Test of effect of domination of FO part")
    main()


def FP_domination_test():
    from main import main
    change_param(fun_weight=(1, 1, 2, 1), folder="domFP", description="Test of effect of domination of FP part")
    main()


def FD_domination_test():
    from main import main
    change_param(fun_weight=(1, 2, 1, 1), folder="domFD", description="Test of effect of domination of FD part")
    main()


def FR_domination_test():
    from main import main
    change_param(fun_weight=(1, 1, 1, 2), folder="domFR", description="Test of effect of domination of FR part")
    main()


def utime1():
    from main import main
    change_param(utime=5, folder="utime1", description="Test of section parameter (reduced)")
    main()


def utime2():
    from main import main
    change_param(utime=20, folder="utime2", description="Test of section parameter (increased)")
    main()


# TODO zastanowić się jakie dane wejściowe chcemy przetestować
def input_data1():
    from main import main
    change_param(rooms="sample data/sale_1.csv")
    main()


def input_data2():
    from main import main
    change_param(lecturers="sample data/prowadzacy_1.csv")
    main()


def input_data3():
    from main import main
    change_param(groups="sample data/grupy_1.csv")
    main()


def input_data4():
    from main import main
    change_param(classes="sample data/zajecia_1.csv")
    main()


def input_data5():
    from main import main
    change_param(classes="sample data/zajecia_2.csv")
    main()


if __name__ == "__main__":
    change_param(description="jakis opis")
