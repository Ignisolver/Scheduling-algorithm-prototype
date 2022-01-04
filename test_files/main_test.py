from main import main  # TODO sprawdzić czy nie trzeba importować osobno w każdym teście
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
    change_param(reassign="replace")
    main()


def reconstruction_test():
    change_param(reassign="reconstruction")
    main()


def sections1():
    change_param(sections=1)
    main()


def sections2():
    change_param(sections=200)
    main()


def iterations1():
    change_param(max_iter=10)
    main()


def iterations2():
    change_param(max_iter=10000)
    main()


def FO_domination_test():
    change_param(fun_weight=(2, 1, 1, 1))
    main()


def FP_domination_test():
    change_param(fun_weight=(1, 1, 2, 1))
    main()


def FD_domination_test():
    change_param(fun_weight=(1, 2, 1, 1))
    main()


def FR_domination_test():
    change_param(fun_weight=(1, 1, 1, 2))
    main()


def utime1():
    change_param(utime=5)
    main()


def utime2():
    change_param(utime=20)
    main()


def input_data1():
    pass


def input_data2():
    pass


def input_data3():
    pass


def input_data4():
    pass


def input_data5():
    pass


if __name__ == "__main__":
    run_test()
