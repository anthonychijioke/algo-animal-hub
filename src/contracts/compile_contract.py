from pyteal import *

from animalhub_contract import AnimalHub

if __name__ == "__main__":
    approval_program = AnimalHub().approval_program()
    clear_program = AnimalHub().clear_program()

    # Mode.Application specifies that this is a smart contract
    compiled_approval = compileTeal(approval_program, Mode.Application, version=6)
    print(compiled_approval)
    with open("animalhub_approval.teal", "w") as teal:
        teal.write(compiled_approval)
        teal.close()

    # Mode.Application specifies that this is a smart contract
    compiled_clear = compileTeal(clear_program, Mode.Application, version=6)
    print(compiled_clear)
    with open("animalhub_clear.teal", "w") as teal:
        teal.write(compiled_clear)
        teal.close()