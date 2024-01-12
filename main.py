from automata_models.wolfram_automata import WolframBinaryAutomata
from automata_models.binary_rule import BinaryLin3Rule, EDGE_CASE_RANDOM, EDGE_CASE_PERIODIC
if __name__ == '__main__':
    print('Starting main.py')

    my_custom_rule = BinaryLin3Rule(edge_case=EDGE_CASE_PERIODIC)
    my_custom_rule.set_rule_from_int(30)

    my_automata = WolframBinaryAutomata(23, update_rule=my_custom_rule)
    my_automata.populate_cells_from_int(2**5)
    my_automata.update_cells_by_rule(iterations=100)
    for x in my_automata.previous_states:
        print(x)

    print(my_automata.rule.rules_dictionary)

