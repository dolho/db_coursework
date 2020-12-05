import matplotlib.pyplot as plt


def print_action(action: str, instanse: str, result: str):
    print(f'Action {action} on {instanse}. Result: {result}')

def print_dot_plot(xaxis, yaxis):
    plt.plot(xaxis, yaxis) #'ro' for dotted plot
    plt.show()